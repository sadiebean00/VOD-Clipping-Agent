from ai.intro_detector import analyse_visual_activity
from ai.gameplay_detector import detect_gameplay_start

video_path = "data/downloads/project_1.mkv"

print("Testing intro detection...")

results = analyse_visual_activity(video_path)

print("\nVisual analysis complete!")
print(f"Video duration: {results['duration']:.2f} seconds")
print(f"Frames analysed: {len(results['activity'])}")


print("\nActivity readings around the 2-minute mark:")

for reading in results["activity"]:
    if 90 <= reading["timestamp"] <= 150:
        print(
            f"Timestamp: {reading['timestamp']:.1f}s | "
            f"Visual activity: {reading['activity']:.2f}"
        )

print("\nActivity readings around the 10-minute mark:")

for reading in results["activity"]:
    if 590 <= reading["timestamp"] <= 610:
        print(
            f"Timestamp: {reading['timestamp']:.1f}s | "
            f"Visual activity: {reading['activity']:.2f}"
        )

print("\nActivity readings around the gameplay transition:")

for reading in results["activity"]:
    if 180 <= reading["timestamp"] <= 210:
        print(
            f"Timestamp: {reading['timestamp']:.1f}s | "
            f"Visual activity: {reading['activity']:.2f}"
        )

gameplay_start = detect_gameplay_start(results)

print("\nGameplay detection result:")

if gameplay_start is not None:
    minutes = int(gameplay_start // 60)
    seconds = int(gameplay_start % 60)
    print(f"Gameplay appears to start at: {minutes:02d}:{seconds:02d}")
else:
    print("Could not detect the gameplay start.")