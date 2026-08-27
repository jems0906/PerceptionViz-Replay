from pydantic import BaseModel, Field


class Box(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class GroundTruthBox(BaseModel):
    id: str
    class_name: str
    bbox: Box
    position: tuple[float, float, float]


class Detection(BaseModel):
    id: str
    frame_id: int
    class_name: str
    confidence: float = Field(ge=0, le=1)
    bbox: Box
    position: tuple[float, float, float]
    matched_gt_id: str | None = None
    iou: float | None = None
    track_id: int | None = None


class FrameRecord(BaseModel):
    id: int
    timestamp: float
    image_url: str
    width: int
    height: int
    ego_pose: tuple[float, float, float]
    ground_truth: list[GroundTruthBox]
