### VOD Clipping Agent - Backend
### The file starts the web server that will power the dashboard.

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from urllib.parse import urlparse
from pathlib import Path
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
from video_processing.clipper import extract_clips

# Create the application.
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_database()
    yield

# Initialises the FastAPI
app = FastAPI (
    title="VOD Clipping Agent",
    description="A local tool for finding and creating gaming VOD highlights.",
    version="0.1.0",
    lifespan=lifespan,
)

# Adds the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Everything to do with the homepage
@app.get("/")
def home():
    # Return a welcome message when we visit the homepage.
    return {
        "message": "VOD clipping agent is running!",
        "status": "ready",
    }

# Check the backend is working as intended.
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Backend is working correctly."
    }

# Returns a list of projects
@app.get("/api/projects")
def list_projects():
    return get_projects()

# Returns the project details
@app.get("/api/projects/{project_id}")
def project_details(project_id: int):
    project = get_project(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    return project

# Manages the changes in the project status
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

# Manages removing the projects
@app.delete("/api/projects/{project_id}")
def remove_project(project_id: int):
    deleted = delete_project(project_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    return {"message": "Project deleted successfully."}

# Manages cleanups of all the projects, i.e. mass removal
@app.delete("/api/projects")
def clean_projects():
    clean_all_projects()
    return {"message:" "All projects and downloaded files have been deleted."}

# Class for the VODRequest where URL and title are stored
class VODRequest(BaseModel):
    url: str
    title: str

# Class for the ClipRequest where the start time and end time are stored
class ClipRequest(BaseModel):
    start_time: float
    end_time: float

# Class for managing more than one clip
class ClipsRequest(BaseModel):
    clips: list[ClipRequest]

# Process for downloading the VOD from the link to the backend
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

# Process to check whether the links are correct
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

# Process to clip the VODs
def process_vod_clipping(project_id, video_path, clips):
    results = extract_clips(
        video_path=video_path,
        clips=clips,
        project_id=project_id
    )

    return results

# Creates the project clips in the app
@app.post("/api/projects/{project_id}/clips")
def create_project_clips(
    project_id: int,
    request: ClipsRequest
):
    project = get_project(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    project_root = Path(__file__).resolve().parent.parent
    downloads_dir = project_root / "data" / "downloads"

    video_files = list(
        downloads_dir.glob(f"project_{project_id}.*")
    )

    if not video_files:
        raise HTTPException(
            status_code=404,
            detail="Downloaded VOD not found."
        )

    clips = [
        (clip.start_time, clip.end_time)
        for clip in request.clips
    ]

    results = process_vod_clipping(
        project_id,
        video_files[0],
        clips
    )

    return results

# Lists the project clips
@app.get("/api/projects/{project_id}/clips")
def list_project_clips(project_id: int):
    project = get_project(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    project_root = Path(__file__).resolve().parent.parent
    clips_dir = project_root / "data" / "clips"

    if not clips_dir.exists():
        return {"clips": []}

    clip_files = sorted(
        clips_dir.glob(f"project{project_id}_clip_*.mp4")
    )

    clips = [
        {
            "filename": clip_file.name,
            "size_bytes": clip_file.stat().st_size
        }
        for clip_file in clip_files
    ]

    return {"clips": clips}

# Check whether the project exists and if it's mp4 etc
@app.get("/api/projects/{project_id}/clips/{filename}")
def serve_project_clip(project_id: int, filename:str):
    project = get_project(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    clips_dir = Path(__file__).resolve().parent.parent / "data" / "clips"

    clip_path = clips_dir / filename

    if (
        clip_path.parent != clips_dir
        or not filename.startswith(f"project{project_id}_clip_")
        or clip_path.suffix.lower() != ".mp4"
        or not clip_path.is_file()
    ):
        raise HTTPException(
            status_code=404,
            detail="Clip not found."
        )

    from fastapi.responses import FileResponse

    return FileResponse(
        path=clip_path,
        media_type="video/mp4",
        filename=filename
    )