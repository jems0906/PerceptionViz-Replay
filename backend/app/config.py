from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    project_root: Path = Path(__file__).resolve().parents[2]
    data_root: Path = project_root / "data_samples"
    model_path: Path = project_root / "backend" / "models" / "yolov8n.pt"
    confidence_threshold: float = 0.25
    iou_threshold: float = 0.5
    use_precomputed: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
