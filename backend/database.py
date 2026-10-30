# VOD Studio - Database
# This file will manage saved VOD projects

from pathlib import Path
import sqlite3

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Store the database inside the data folder
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "vod_studio.db"

# Gets the connection of the database
def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection

# Initialises the database
def initialise_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            platform TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            processing_message TEXT DEFAULT 'Waiting to be processed',
            download_progress REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    columns = connection.execute(
        "PRAGMA table_info(projects)"
    ).fetchall()

    column_names = [column["name"] for column in columns]

    if "processing_message" not in column_names:
        connection.execute("""
        ALTER TABLE projects
        ADD COLUMN processing_message TEXT
        DEFAULT 'Waiting to be processed'
        """)

    if "download_progress" not in column_names:
        connection.execute("""
        ALTER TABLE projects
        ADD COLUMN download_progress REAL DEFAULT 0
        """)

    connection.commit()
    connection.close()

# Creates a project within the database
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

# Gets all the projects in the database
def get_projects():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, title, url, platform, status, processing_message, download_progress, created_at
        FROM projects   
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()

    projects = [dict(row) for row in rows]
    connection.close()

    return projects

# Gets a singular project in the database
def get_project(project_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, title, url, platform, status, processing_message, download_progress, created_at
        FROM projects
        WHERE id = ?
        """,
        (project_id,),
    ).fetchone()

    project = dict(row) if row else None
    connection.close()

    return project

# Updates the project's status
def update_project_status(project_id, status, processing_message):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE projects
        SET status = ?, processing_message = ?
        WHERE id = ?
        """,
        (status, processing_message, project_id),
    )

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()

    return updated

def update_download_progress(project_id, percentage):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE projects
        SET download_progress = ?
        WHERE id = ?
        """,
        (percentage, project_id)
    )

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()

    return updated

# Deletes the project
def delete_project(project_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,),
    )

    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()

    if deleted:
        project_root = Path(__file__).resolve().parent.parent
        downloads_dir = project_root / "data" / "downloads"

        for file_path in downloads_dir.glob(f"project_{project_id}.*"):
            file_path.unlink()

    return deleted

# Cleans up all the projects
def clean_all_projects():
    connection = get_connection()

    connection.execute("DELETE FROM sqlite_sequence WHERE name = 'projects'")
    connection.execute("DELETE FROM projects")
    connection.commit()
    connection.close()

    project_root = Path(__file__).resolve().parent.parent

    folders = [
        project_root / "data" / "downloads",
        project_root / "data" / "clips",
    ]

    for folder in folders:
        if folder.exists():
            for file_path in folder.iterdir():
                if file_path.is_file():
                    file_path.unlink()


    return True