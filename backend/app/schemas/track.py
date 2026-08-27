from pydantic import BaseModel


class TrackPoint(BaseModel):
    frame_id: int
    bbox: tuple[float, float, float, float]
    position: tuple[float, float, float]
    confidence: float
    matched_gt_id: str | None = None


class Track(BaseModel):
    track_id: int
    class_name: str
    points: list[TrackPoint]
    continuity: int
    id_switch: bool = False
