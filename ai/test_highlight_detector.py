from ai.audio_analyser import analyse_audio
from ai.highlight_detector import detect_highlights

video_path = "data/downloads/project_1.mkv"

print("Analysing VOD audio...")

audio_results = analyse_audio(video_path)

print("\nDetecting potential highlights...")

highlights = detect_highlights(audio_results)

print(f"\nPotential highlights found: {len(highlights)}")

for highlight in highlights[:30]:
    print(
        f"Start: {highlight['start_time']:.2f}s | "
        f"End: {highlight['end_time']:.2f}s | "
        f"Peak energy: {highlight['peak_energy']:.4f}"
    )
