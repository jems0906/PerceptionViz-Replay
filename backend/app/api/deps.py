from functools import lru_cache

from app.config import get_settings
from app.data.loader import DatasetLoader
from app.inference.detector import deterministic_detections
from app.inference.precompute import precompute
from app.metrics.detection import match_detections
from app.schemas import Detection
from app.tracking.sort import SortTracker


@lru_cache
def get_loader() -> DatasetLoader:
    return DatasetLoader(get_settings().data_root)


@lru_cache
def get_cached_detections() -> tuple[Detection, ...]:
    settings = get_settings()
    loader = get_loader()
    output_path = settings.data_root / "predictions" / "precomputed_detections.parquet"
    return tuple(precompute(loader.frames(), deterministic_detections, output_path))


def run_frame_detection(frame_id: int) -> list[Detection]:
    loader = get_loader()
    frame = loader.frame(frame_id)
    tracker = SortTracker()
    prior = [item for item in get_cached_detections() if item.frame_id < frame_id]
    for prior_frame_id in sorted({item.frame_id for item in prior}):
        tracker.update([item for item in prior if item.frame_id == prior_frame_id])
    return tracker.update(match_detections(frame, deterministic_detections(frame)))
