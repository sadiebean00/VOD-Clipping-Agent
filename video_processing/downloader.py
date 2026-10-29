## VOD Clipping Agent - Video Processing
## Downloads the processed videos 

from pathlib import Path
import yt_dlp

# Sets up the path for the downloads
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOWNLOAD_DIR = PROJECT_ROOT / "data" / "downloads"

# Download the VOD
def download_vod(url, project_id):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    output_template = str(
        DOWNLOAD_DIR / f"project_{project_id}.%(ext)s"
    )

    options = {
        "outtmpl": output_template,
        "format": "bestvideo+bestaudio/best",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(options) as downloader:
        downloader.download([url])

    return True