# VOD Studio - Clipping Tool
# This is the tool that extracts and creates clips from VODs

import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLIPS_DIR = PROJECT_ROOT / "data" / "clips"

# Extracts the clips from the video path
def extract_clip(video_path, start_time, end_time, project_id):
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    if start_time < 0  or end_time <= start_time:
        raise ValueError("Invalid clip timestamps.")

    CLIPS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = CLIPS_DIR / f"project{project_id}_clip.mp4"

    duration = end_time - start_time

    command = [
        "ffmpeg",
        "-y",
        "-ss", str(start_time),
        "-i", str(video_path),
        "-t", str(duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "fast",
        str(output_path)
    ]

    subprocess.run(command, check=True)

    return output_path