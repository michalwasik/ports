from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from database import parse_csv_and_store

app = FastAPI()

parse_csv_and_store('../data/web_challenge.csv', '../db/routes.db')


class Route(BaseModel):
    route_id: int
    from_port: str
    to_port: str
    leg_duration: int


class GeoJSON(BaseModel):
    type: str
    coordinates: list

@app.get("/routes")
async def get_routes():
    conn = sqlite3.connect('../db/routes.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT route_id, from_port, to_port, leg_duration FROM routes''')
    routes = cursor.fetchall()
    conn.close()
    return routes

@app.get("/routes/{route_id}")
async def get_route_points(route_id: int):
    conn = sqlite3.connect('../db/routes.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT longitude, latitude FROM points WHERE route_id = ?''', (route_id,))
    points = cursor.fetchall()
    conn.close()

    if not points:
        raise HTTPException(status_code=404, detail="Route points not found")

    geojson = {
        "type": "LineString",
        "coordinates": points
    }
    return geojson
