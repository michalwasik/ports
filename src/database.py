import csv
import json
import os
import sys
from pathlib import Path
from sqlite3 import connect


def get_db_connection():
    db_path = Path(__file__).parent.parent / "db" / "routes.db"
    # Ensure the db directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return connect(db_path)


def parse_csv_and_store(filename):
    # Increase the CSV field size limit
    csv.field_size_limit(1_000_000)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Creating tables
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS routes (
            route_id INTEGER PRIMARY KEY,
            from_port TEXT,
            to_port TEXT,
            leg_duration INTEGER
        )"""
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_id INTEGER,
            longitude REAL,
            latitude REAL,
            timestamp INTEGER,
            speed REAL
        )"""
    )

    with open(filename, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            route_id = int(row["route_id"])
            from_port = row["from_port"]
            to_port = row["to_port"]
            leg_duration = int(row["leg_duration"])
            points = json.loads(row["points"])

            cursor.execute(
                "INSERT INTO routes (route_id, from_port, to_port, leg_duration) VALUES (?, ?, ?, ?)",
                (route_id, from_port, to_port, leg_duration),
            )

            for point in points:
                cursor.execute(
                    "INSERT INTO points (route_id, longitude, latitude, timestamp, speed) VALUES (?, ?, ?, ?, ?)",
                    (route_id, *point),
                )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    data_path = Path(__file__).parent.parent / "data" / "web_challenge.csv"
    parse_csv_and_store(data_path)
