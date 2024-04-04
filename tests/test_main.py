from fastapi.testclient import TestClient
import pytest
import sqlite3
import sys

sys.path.append("/mnt/c/Users/michal.wasik/PycharmProjects/ports/src")
from main import app

client = TestClient(app)


# Fixture to provide the test database connection
@pytest.fixture(scope="module")
def test_db():
    # Connect to the test database
    conn = sqlite3.connect("test_routes.db")
    cursor = conn.cursor()

    # Ensure that the routes table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            route_id INTEGER PRIMARY KEY,
            from_port TEXT NOT NULL,
            to_port TEXT NOT NULL,
            leg_duration INTEGER NOT NULL
        )
    """)

    # Insert test data into the routes table if it's empty
    cursor.execute("SELECT COUNT(*) FROM routes")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("""
            INSERT INTO routes (route_id, from_port, to_port, leg_duration)
            VALUES (1, 'DEWVN', 'DEBRV', 61904204)
        """)

    # Commit the changes
    conn.commit()

    # Provide the fixture value
    yield conn

    # Close the connection after the test finishes
    conn.close()


def test_get_routes(test_db):
    response = client.get("/routes")

    # Print response details
    print("Response status code:", response.status_code)
    print("Response headers:", response.headers)
    print("Response text:", response.text)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert len(response.json()) > 0


def test_get_routes_by_id(test_db):
    response = client.get("/routes/1")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    response_data = response.json()
    assert response_data["type"] == "LineString"
    assert "coordinates" in response_data
    assert len(response_data["coordinates"]) > 0


def test_get_routes_by_invalid_id(test_db):
    response = client.get("/routes/999")
    assert response.status_code == 404


def test_get_routes_by_invalid_format(test_db):
    response = client.get("/routes/invalid")
    assert response.status_code == 422
