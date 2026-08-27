"""Load the real YOLOv8n model and verify one valid inference result."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.api.deps import get_loader  # noqa: E402
from app.inference.detector import YoloDetector  # noqa: E402


def main() -> None:
    loader = get_loader()
    frame = loader.frame(1)
    detector = YoloDetector(ROOT / "backend" / "models" / "yolov8n.pt")
    detections = detector.detect(loader.image_path(frame.id), frame)
    if not detections:
        raise RuntimeError("YOLOv8n loaded but returned no predictions for the CI sample frame")
    if any(not 0 <= item.confidence <= 1 for item in detections):
        raise RuntimeError("YOLOv8n returned a prediction with an invalid confidence")
    print(f"YOLOv8n verified: {len(detections)} valid predictions on frame {frame.id}")


if __name__ == "__main__":
    main()
