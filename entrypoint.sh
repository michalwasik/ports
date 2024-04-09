#!/bin/bash
# Initialize the database, if needed
python database.py

# Start Uvicorn with live auto-reload enabled
uvicorn main:app --host 0.0.0.0 --port 8080 --reload