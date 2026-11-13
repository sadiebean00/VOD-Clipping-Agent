from ai.audio_analyser import analyse_audio
from ai.highlight_detector import detect_highlights, format_timestamp
from ai.intro_detector import analyse_visual_activity
from ai.gameplay_detector import detect_gameplay_start

video_path = "data/downloads/project_3.mp4"

from pathlib import Path

video_file = Path(video_path).resolve()

print(f"Video being analysed: {video_file}")
print(f"File exists: {video_file.exists()}")

if video_file.exists():
    print(f"File size: {video_file.stat().st_size / (1024 * 1024):.2f} MB")

print("Analysing VOD audio...")

audio_results = analyse_audio(video_path)

print("\nAnalysing VOD visuals..")

visual_results = analyse_visual_activity(video_path)

print("\nDetecting gameplay start...")

gameplay_start = detect_gameplay_start(visual_results)

if gameplay_start is None:
    print("Could not detect gameplay start.")
    exit()

print(f"Gameplay begins at: {gameplay_start:.2f}s")

print("\nDetecting potential highlights...")

highlights = detect_highlights(
    audio_results,
    gameplay_start=gameplay_start,
    padding_before=5.0,
    padding_after=5.0
    )

print(f"\nPotential highlights found: {len(highlights)}")

if highlights:
    earliest_highlight = highlights[0]["start_time"]
    print(f"Earliest Highlight: {earliest_highlight:.2f}s")

    if earliest_highlight < gameplay_start:
        print("WARNING: A highlight was detected before gameplay!")
    else:
        print("All detected highlights occur after gameplay starts.")

print("\nFirst highlight's raw timestamps:")
print(highlights[1])

for highlight in highlights[:30]:
    print(
        f"Start: {format_timestamp(highlight['start_time'])} | "
        f"End: {format_timestamp(highlight['end_time'])} | "
        f"Peak energy: {highlight['peak_energy']:.4f}"
    )
