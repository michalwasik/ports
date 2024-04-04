import csv
import sqlite3
import json
import os
import sys

csv.field_size_limit(sys.maxsize)

def parse_csv_and_store(filename, db_filename):
    if os.path.exists(db_filename):
        os.remove(db_filename)
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create routes table
    cursor.execute('''CREATE TABLE IF NOT EXISTS routes (
                        route_id INTEGER PRIMARY KEY,
                        from_port TEXT,
                        to_port TEXT,
                        leg_duration INTEGER
                    )''')

    # Create points table
    cursor.execute('''CREATE TABLE IF NOT EXISTS points (
                        id INTEGER PRIMARY KEY,
                        route_id INTEGER,
                        longitude REAL,
                        latitude REAL,
                        timestamp INTEGER,
                        speed REAL
                    )''')

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            route_id = int(row[0])
            from_port = row[1]
            to_port = row[2]
            leg_duration = int(row[3])

            points_str = row[4]
            points = json.loads(points_str)

            cursor.execute('''INSERT INTO routes (route_id, from_port, to_port, leg_duration)
                            VALUES (?, ?, ?, ?)''', (route_id, from_port, to_port, leg_duration))

            for point in points:
                longitude, latitude, timestamp, speed = point
                cursor.execute('''INSERT INTO points (route_id, longitude, latitude, timestamp, speed)
                                VALUES (?, ?, ?, ?, ?)''', (route_id, longitude, latitude, timestamp, speed))

    conn.commit()
    conn.close()
