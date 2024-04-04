# import sqlite3
# import pytest
#
#
# # Fixture to create and populate the test database
# @pytest.fixture(scope="module")
# def test_db():
#     db_name = "test_routes.db"
#
#     # Connect to the test database
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#
#     # Create the routes table if it doesn't exist
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS routes (
#             route_id INTEGER PRIMARY KEY,
#             from_port TEXT NOT NULL,
#             to_port TEXT NOT NULL,
#             leg_duration INTEGER NOT NULL
#         )
#     """
#     )
#
#     # Insert test data into the routes table if it's empty
#     cursor.execute("SELECT COUNT(*) FROM routes")
#     count = cursor.fetchone()[0]
#     if count == 0:
#         cursor.execute(
#             """
#             INSERT INTO routes (route_id, from_port, to_port, leg_duration)
#             VALUES (1, 'DEWVN', 'DEBRV', 61904204)
#         """
#         )
#
#     # Commit the changes
#     conn.commit()
#
#     # Provide the fixture value
#     yield conn
#
#     # Cleanup: Delete test data from the routes table
#     # cursor.execute("DELETE FROM routes")
#
#     conn.commit()
#     conn.close()
