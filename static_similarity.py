from frame import Frame


def angle_similarity(frame_x: Frame, frame_standard: Frame):
    weights = frame_standard.angle_weights
    thresholds = frame_standard.angle_thresholds
    standard_angles = frame_standard.get_angles()
    angles = frame_x.get_angles()

    diffs = {key: abs(standard_angles[key] - angles[key]) for key in angles if key in standard_angles}
    matched = all(diffs[key] < thresholds[key] for key in diffs)
    score = None
    if matched:
        values = {key: (1 - diffs[key] / thresholds[key]) * weights[key] for key in diffs}
        score = sum(values.values())
    return matched, score

def angle_similarity_almost(frame_x: Frame, frame_standard: Frame):
    weights = frame_standard.angle_weights
    thresholds = frame_standard.angle_thresholds
    standard_angles = frame_standard.get_angles()
    angles = frame_x.get_angles()
    eta = 0.8

    diffs = {key: abs(standard_angles[key] - angles[key]) for key in angles if key in standard_angles}
    matched = sum(diffs[key] < thresholds[key] for key in diffs) > len(diffs) * eta
    score = None
    if matched:
        values = {key: (1 - min(diffs[key], thresholds[key]) / thresholds[key]) * weights[key] for key in diffs}
        score = sum(values.values())
    return matched, score
