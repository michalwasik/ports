from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import sqlite3

from db_utils import get_db_connection
from models import GeoJSON, RouteInDB

app = FastAPI()


@app.get("/routes", response_model=List[RouteInDB])
async def get_routes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM routes")
    column_names = [column[0] for column in cursor.description]
    routes_data = cursor.fetchall()
    conn.close()
    return [RouteInDB(**dict(zip(column_names, route))) for route in routes_data]


@app.get("/routes/{route_id}", response_model=GeoJSON)
async def get_route_points(route_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT longitude, latitude FROM points WHERE route_id = ?", (route_id,)
    )
    points = cursor.fetchall()
    conn.close()

    if not points:
        raise HTTPException(status_code=404, detail="Route points not found")

    return GeoJSON(coordinates=points)
