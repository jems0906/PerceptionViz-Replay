from pydantic import BaseModel


class FrameMetrics(BaseModel):
    frame_id: int
    precision: float
    recall: float
    mean_iou: float
    false_positives: int
    false_negatives: int
    true_positives: int


class AggregateMetrics(BaseModel):
    frames: list[FrameMetrics]
    precision: float
    recall: float
    mean_iou: float
    id_switches: int
    track_continuity: dict[str, int]
    per_class: dict[str, dict[str, float]]
