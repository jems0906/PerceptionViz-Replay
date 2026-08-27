"""Load the real YOLOv8n model and verify one valid inference result."""

from pathlib import Path
import sys
from math import isfinite

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.api.deps import get_loader  # noqa: E402
from app.inference.detector import YoloDetector  # noqa: E402


def main() -> None:
    loader = get_loader()
    frame = loader.frame(1)
    detector = YoloDetector(ROOT / "backend" / "models" / "yolov8n.pt")
    detections = detector.detect(loader.image_path(frame.id), frame)
    for detection in detections:
        coordinates = (detection.bbox.x1, detection.bbox.y1, detection.bbox.x2, detection.bbox.y2)
        if not detection.class_name or not 0 <= detection.confidence <= 1:
            raise RuntimeError("YOLOv8n returned a prediction with invalid class or confidence data")
        if not all(isfinite(value) for value in coordinates) or detection.bbox.x2 <= detection.bbox.x1 or detection.bbox.y2 <= detection.bbox.y1:
            raise RuntimeError("YOLOv8n returned an invalid bounding box")
    print(f"YOLOv8n verified: inference completed with {len(detections)} valid predictions on frame {frame.id}")


if __name__ == "__main__":
    main()
