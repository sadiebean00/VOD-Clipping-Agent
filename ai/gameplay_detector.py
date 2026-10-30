# VOD Studio - Gameplay Detector
# Detects gameplay changes

def detect_gameplay_start(
        visual_results,
        transition_threshold=40.0,
        gameplay_activity_threshold=15.0,
        sustained_readings=4
):
    activity = visual_results["activity"]

    for index, reading in enumerate(activity):
        # Look for a large visual change.
        if reading["activity"] < transition_threshold:
            continue

        # Check whether activity stays elevated afterwards.
        following_readings = activity[
            index +1:index + 1 + sustained_readings
        ]

        if len(following_readings) < sustained_readings:
            continue

        active_readings = sum(
            item["activity"] >= gameplay_activity_threshold
            for item in following_readings
        )

        if active_readings >= sustained_readings -1:
            return float(reading["timestamp"])

    return None