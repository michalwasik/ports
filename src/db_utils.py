from sqlite3 import connect
from pathlib import Path


def get_db_connection():
    # This obtains the base directory of the project first to construct the path regardless of execution location
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "db" / "routes.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure that db directory exists
    return connect(str(db_path))
