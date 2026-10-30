## VOD Clipping Agent - Video Processing
## Downloads the processed videos 

from pathlib import Path
import yt_dlp

# Sets up the path for the downloads
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOWNLOAD_DIR = PROJECT_ROOT / "data" / "downloads"

# Creates a percentage hook
def download_progress_hook(data, progress_callback=None):
    if data["status"] == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or data.get("total_bytes_estimate")

        if total:
            percentage = (downloaded / total) * 100
            print(f"Download progress: {percentage:.1f}%")

            if progress_callback:
                progress_callback(percentage)

# Download the VOD
def download_vod(url, project_id, progress_callback=None):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    output_template = str(
        DOWNLOAD_DIR / f"project_{project_id}.%(ext)s"
    )

    options = {
        "outtmpl": output_template,
        "format": "bestvideo+bestaudio/best",
        "noplaylist": True,
        "progress_hooks": [lambda data: download_progress_hook(data, progress_callback)
],
    }

    with yt_dlp.YoutubeDL(options) as downloader:
        downloader.download([url])

    return True