# VOD Studio - Intro Detector
# Efficiently identifies visual activity in a VOD.

import cv2
import numpy as np


def analyse_visual_activity(video_path, sample_interval=2.0):
    video = cv2.VideoCapture(str(video_path))

    if not video.isOpened():
        raise FileNotFoundError(f"Could not open video: {video_path}")

    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

    if fps <= 0:
        video.release()
        raise ValueError("Could not determine the video's frame rate.")

    duration = total_frames / fps
    frame_interval = max(1, int(fps * sample_interval))

    results = []
    previous_frame = None
    frame_number = 0
    last_reported_percentage = -1

    print("Analysing visual activity...")

    while True:
        success = video.grab()

        if not success:
            break

        if frame_number % frame_interval == 0:
            success, frame = video.retrieve()

            if not success:
                break

            frame = cv2.resize(frame, (160, 90))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if previous_frame is not None:
                difference = cv2.absdiff(previous_frame, frame)
                activity = float(np.mean(difference))

                results.append({
                    "timestamp": frame_number / fps,
                    "activity": activity
                })

            previous_frame = frame

        frame_number += 1

        progress = (frame_number / total_frames) * 100
        percentage = int(progress)

        if percentage > last_reported_percentage:
            print(f"Analysis progress: {percentage}%")
            last_reported_percentage = percentage

    video.release()

    return {
        "duration": duration,
        "activity": results
    }
