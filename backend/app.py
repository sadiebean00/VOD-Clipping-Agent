### VOD Clipping Agent - Backend
### The file starts the web server that will power the dashboard.

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from urllib.parse import urlparse
from contextlib import asynccontextmanager
from backend.database import (
    initialise_database,
    create_project,
    get_projects,
    get_project,
    update_project_status,
    update_download_progress,
    delete_project,
    clean_all_projects
)
from video_processing.downloader import download_vod

# Create the application.
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_database()
    yield

app = FastAPI (
    title="VOD Clipping Agent",
    description="A local tool for finding and creating gaming VOD highlights.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    # Return a welcome message when we visit the homepage.
    return {
        "message": "VOD clipping agent is running!",
        "status": "ready",
    }

@app.get("/api/health")
def health_check():
    # Check the backend is working as intended.
    return {
        "status": "healthy",
        "message": "Backend is working correctly."
    }

@app.get("/api/projects")
def list_projects():
    return get_projects()

@app.get("/api/projects/{project_id}")
def project_details(project_id: int):
    project = get_project(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    return project

@app.patch("/api/projects/{project_id}/status")
def change_project_status(
    project_id: int,
    status: str,
    processing_message: str,
):
    updated = update_project_status(
        project_id,
        status,
        processing_message,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    return{"message:" "Project status updated successfully."}

@app.delete("/api/projects/{project_id}")
def remove_project(project_id: int):
    deleted = delete_project(project_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    return {"message": "Project deleted successfully."}

@app.delete("/api/projects")
def clean_projects():
    clean_all_projects()
    return {"message:" "All projects and downloaded files have been deleted."}


class VODRequest(BaseModel):
    url: str
    title: str

def process_vod_download(project_id, url):
    def progress_callback(percentage):
        update_download_progress(project_id, percentage)

    update_project_status(
        project_id,
        "downloading",
        "Downloading your VOD...",
    )

    try:
        download_vod(url, project_id, progress_callback)

        update_project_status(
            project_id,
            "downloaded",
            "VOD downloaded successfully!",
        )

    except Exception as error:
        update_project_status(
            project_id,
            "failed",
            f"Download failed: {error}", 
        )

@app.post("/api/vod")
def receive_vod(
    request: VODRequest, background_tasks: BackgroundTasks):
    url = request.url

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if not hostname:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid video URL."
        )

    if not url.startswith("https://"):
        raise HTTPException(
            status_code=400,
            detail="Please use a secure HTTPS video link."
        )
        

    if hostname in ["youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"]:
        platform = "YouTube"
    elif hostname in ["twitch.tv", "www.twitch.tv", "m.twitch.tv"]:
        platform = "Twitch"
    else:
        platform = "Unknown"

    if platform == "Unknown":
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid YouTube or Twitch link.",
        )

    project_id = create_project(request.title, url, platform)

    background_tasks.add_task(
        process_vod_download,
        project_id,
        url,
    )

    return {
        "message": "VOD project saved successfully!",
        "project_id": project_id,
        "title": request.title,
        "url": url,
        "platform": platform,
    }