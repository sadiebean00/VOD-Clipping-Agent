### VOD Clipping Agent - Backend
### The file starts the web server that will power the dashboard.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from urllib.parse import urlparse

# Create the application.
app = FastAPI (
    title="VOD Clipping Agent",
    description="A local tool for finding and creating gaming VOD highlights.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
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

class VODRequest(BaseModel):
    url: str

@app.post("/api/vod")
def receive_vod(request: VODRequest):
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

    return {
        "message": "VOD link received by the backend!",
        "url": url,
        "platform": platform,
    }