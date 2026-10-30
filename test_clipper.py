#VOD Studio - TEST CLIPPING

from video_processing.clipper import extract_clips

results = extract_clips(
    video_path="data/downloads/project_1.mkv",
    clips = [
        (0, 15),
        (20, 35),
        (-10,5),
        (40, 55)
    ],
    project_id=1
)

print("\n=============== CLIPPING SUMMARY ===============")

print(f"Successfully created: {len(results['created'])}")
print(f"Failed: {len(results['failed'])}")
print(f"Total Attempted: {len(results['created']) + len(results['failed'])}")

if results["created"]:
    print("\nSuccessfully created clips:")

    for clip_path in results["created"]:
        print(f"- {clip_path}")

if results["failed"]:
    print("\nFailed clips:")

    for failed_clip in results["failed"]:
        print(
            f"- {failed_clip['start_time']}-{failed_clip['end_time']}: "
            f"{failed_clip['error']}"
        )

print("===============")