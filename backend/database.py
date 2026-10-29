# VOD Studio - Database
# This file will manage saved VOD projects

from pathlib import Path
import sqlite3

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Store the database inside the data folder
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "vod_studio.db"

def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection

def initialise_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            platform TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

def create_project(title, url, platform):
    connection = get_connection()

    cursor = connection.execute(
      """
        INSERT INTO projects (title, url, platform)
        VALUES (?, ?, ?)
        """,
        (title, url, platform),  
    )

    connection.commit()
    project_id = cursor.lastrowid
    connection.close()

    return project_id

def get_projects():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, title, url, platform, status, created_at
        FROM projects
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()

    projects = [dict(row) for row in rows]
    connection.close()

    return projects

def delete_project(project_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,),
    )

    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()

    return deleted