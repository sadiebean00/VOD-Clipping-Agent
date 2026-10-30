# VOD Studio - Highlight Detector
# Groups unusually loud audio frames into potential highlights.

import numpy as np


def detect_highlights(
    audio_results,
    sensitivity=2.0,
    minimum_gap=1.0,
    minimum_duration=0.1
):
    energy = audio_results["energy"]
    timestamps = audio_results["timestamps"]

    average_energy = np.mean(energy)
    energy_deviation = np.std(energy)

    threshold = average_energy + (sensitivity * energy_deviation)

    highlight_indices = np.where(energy > threshold)[0]

    if len(highlight_indices) == 0:
        return []

    highlights = []

    start_time = timestamps[highlight_indices[0]]
    last_time = start_time
    peak_energy = energy[highlight_indices[0]]

    for index in highlight_indices[1:]:
        current_time = timestamps[index]

        peak_energy = max(peak_energy, energy[index])

        if current_time - last_time > minimum_gap:
            duration = last_time - start_time

            if duration >= minimum_duration:
                highlights.append({
                    "start_time": float(start_time),
                    "end_time": float(last_time),
                    "peak_energy": float(peak_energy)
                })

            start_time = current_time
            peak_energy = energy[index]

        last_time = current_time

    duration = last_time - start_time

    if duration >= minimum_duration:
        highlights.append({
            "start_time": float(start_time),
            "end_time": float(last_time),
            "peak_energy": float(peak_energy)
        })

    return highlights
