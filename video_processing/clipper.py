# VOD Studio - Clipping Tool
# This is the tool that extracts and creates clips from VODs

import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLIPS_DIR = PROJECT_ROOT / "data" / "clips"

# Formatting the timestamps
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}m{remaining_seconds:02d}s"

# Extracts the clips from the video path
def extract_clip(video_path, start_time, end_time, project_id):
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    if start_time < 0  or end_time <= start_time:
        raise ValueError("Invalid clip timestamps.")

    CLIPS_DIR.mkdir(parents=True, exist_ok=True)

    start_label = format_timestamp(start_time)
    end_label = format_timestamp(end_time)
    
    clip_number = 1
    
    while True:
        output_path = CLIPS_DIR / f"project{project_id}_clip_{start_label}-{end_label}_{clip_number}.mp4"

        if not output_path.exists():
            break

        clip_number += 1

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

# Extract multiple clips from the same VOD
def extract_clips(video_path, clips, project_id):
    created_clips = []
    failed_clips = []

    for start_time, end_time in clips:
        try:
            clip_path = extract_clip(
                video_path=video_path,
                start_time=start_time,
                end_time=end_time,
                project_id=project_id
            )

            created_clips.append(clip_path)

        except Exception as error:
            failed_clips.append({
                "start_time": start_time,
                "end_time": end_time,
                "error": str(error)
            })

    return {
        "created": created_clips,
        "failed": failed_clips
    }