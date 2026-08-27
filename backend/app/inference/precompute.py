from __future__ import annotations

from app.data.parquet_store import write_detections
from app.metrics.detection import match_detections
from app.schemas import Detection, FrameRecord
from app.tracking.sort import SortTracker


def precompute(frames: list[FrameRecord], detect_frame, output_path) -> list[Detection]:
    tracker = SortTracker()
    all_detections: list[Detection] = []
    for frame in frames:
        detections = match_detections(frame, detect_frame(frame))
        tracked = tracker.update(detections)
        all_detections.extend(tracked)
    write_detections(output_path, all_detections)
    return all_detections
