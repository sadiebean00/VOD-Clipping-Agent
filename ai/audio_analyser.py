
# VOD Studio - Audio Analyser
# Analyses audio energy to identify potential highlight moments.

import librosa
import numpy as np
import subprocess
import tempfile
from pathlib import Path

# Analyses the audio
def analyse_audio(video_path):
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    print("Extracting audio from VOD...")

    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = Path(temp_dir) / "audio.wav"

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", str(video_path),
                "-vn",
                "-ac", "1",
                "-ar", "22050",
                str(audio_path)
            ],
            check=True,
            capture_output=True,
            text=True
        )

        print("Loading audio into analyser...")

        audio, sample_rate = librosa.load(
            str(audio_path),
            sr=22050,
            mono=True
        )

    print("Analysing audio energy...")

    rms_energy = librosa.feature.rms(
        y=audio,
        frame_length=2048,
        hop_length=512
    )[0]

    timestamps = librosa.frames_to_time(
        np.arange(len(rms_energy)),
        sr=sample_rate,
        hop_length=512
    )

    return {
        "timestamps": timestamps,
        "energy": rms_energy
    }
