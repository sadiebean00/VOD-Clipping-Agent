# VOD Studio - Highlight Detector
# Groups unusually loud audio frames into potential highlights.

import numpy as np

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"


def detect_highlights(
    audio_results,
    sensitivity=2.0,
    minimum_gap=1.0,
    minimum_duration=0.1,
    gameplay_start=0.0,
    padding_before=5.0,
    padding_after=5.0
):
    energy = audio_results["energy"]
    timestamps = audio_results["timestamps"]

    average_energy = np.mean(energy)
    energy_deviation = np.std(energy)

    threshold = average_energy + (sensitivity * energy_deviation)

    highlight_indices = np.where(
        (energy > threshold) & (timestamps >= gameplay_start)
    )[0]

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
                    "start_time": max(gameplay_start, float(start_time) - padding_before),
                    "end_time": float(last_time) + padding_after,
                    "peak_energy": float(peak_energy)
                })

            start_time = current_time
            peak_energy = energy[index]

        last_time = current_time

    duration = last_time - start_time

    if duration >= minimum_duration:
        highlights.append({
            "start_time": max(gameplay_start, float(start_time) - padding_before),
            "end_time": float(last_time) + padding_after,
            "peak_energy": float(peak_energy)
        })


    highlights.sort(
        key=lambda highlight: highlight["peak_energy"],
        reverse=True
    )

    return highlights
