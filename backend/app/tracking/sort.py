from __future__ import annotations

from dataclasses import dataclass, field

from app.metrics.detection import iou
from app.schemas import Detection, Track, TrackPoint
from app.tracking.kalman import ConstantVelocityState


@dataclass
class _ActiveTrack:
    track_id: int
    class_name: str
    last_detection: Detection
    missed: int = 0
    state: ConstantVelocityState = field(default_factory=lambda: ConstantVelocityState(0.0, 0.0))


class SortTracker:
    def __init__(self, iou_threshold: float = 0.25, max_age: int = 2):
        self.iou_threshold = iou_threshold
        self.max_age = max_age
        self._next_id = 1
        self._active: list[_ActiveTrack] = []

    def update(self, detections: list[Detection]) -> list[Detection]:
        assigned: set[int] = set()
        updated: list[Detection] = []
        for detection in detections:
            best_index = None
            best_score = 0.0
            for index, track in enumerate(self._active):
                if index in assigned or track.class_name != detection.class_name:
                    continue
                score = iou(track.last_detection.bbox, detection.bbox)
                if score > best_score:
                    best_index = index
                    best_score = score
            if best_index is not None and best_score >= self.iou_threshold:
                track = self._active[best_index]
                assigned.add(best_index)
                track.missed = 0
                track.state.update(detection.position[0], detection.position[1])
                detection = detection.model_copy(update={"track_id": track.track_id})
                track.last_detection = detection
            else:
                track = _ActiveTrack(
                    track_id=self._next_id,
                    class_name=detection.class_name,
                    last_detection=detection,
                    state=ConstantVelocityState(detection.position[0], detection.position[1]),
                )
                self._next_id += 1
                self._active.append(track)
                detection = detection.model_copy(update={"track_id": track.track_id})
            updated.append(detection)

        for index, track in enumerate(self._active):
            if index not in assigned and all(item.track_id != track.track_id for item in updated):
                track.missed += 1
                track.state.predict()
        self._active = [track for track in self._active if track.missed <= self.max_age]
        return updated


def build_tracks(detections: list[Detection]) -> list[Track]:
    grouped: dict[int, list[Detection]] = {}
    for detection in detections:
        if detection.track_id is not None:
            grouped.setdefault(detection.track_id, []).append(detection)
    tracks = []
    for track_id, items in sorted(grouped.items()):
        ordered = sorted(items, key=lambda item: item.frame_id)
        matched_gt_ids = {item.matched_gt_id for item in ordered if item.matched_gt_id}
        tracks.append(
            Track(
                track_id=track_id,
                class_name=ordered[0].class_name,
                continuity=len({item.frame_id for item in ordered}),
                id_switch=len(matched_gt_ids) > 1,
                points=[
                    TrackPoint(
                        frame_id=item.frame_id,
                        bbox=(item.bbox.x1, item.bbox.y1, item.bbox.x2, item.bbox.y2),
                        position=item.position,
                        confidence=item.confidence,
                        matched_gt_id=item.matched_gt_id,
                    )
                    for item in ordered
                ],
            )
        )
    return tracks
