from __future__ import annotations

from collections import defaultdict

from app.schemas import Detection


def track_continuity(detections: list[Detection]) -> dict[str, int]:
    continuity: dict[str, set[int]] = defaultdict(set)
    for detection in detections:
        if detection.track_id is not None:
            continuity[str(detection.track_id)].add(detection.frame_id)
    return {track_id: len(frames) for track_id, frames in continuity.items()}


def id_switch_count(detections: list[Detection]) -> int:
    gt_to_track: dict[str, int] = {}
    switches = 0
    for detection in sorted(detections, key=lambda item: (item.frame_id, item.id)):
        if not detection.matched_gt_id or detection.track_id is None:
            continue
        previous = gt_to_track.get(detection.matched_gt_id)
        if previous is not None and previous != detection.track_id:
            switches += 1
        gt_to_track[detection.matched_gt_id] = detection.track_id
    return switches
