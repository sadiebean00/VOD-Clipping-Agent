#VOD Studio - TEST CLIPPING

from video_processing.clipper import extract_clip

clip_path = extract_clip(
    video_path="data/downloads/project_1.mkv",
    start_time=30,
    end_time=60,
    project_id=1
)

print(f"Clip created successfully: {clip_path}")