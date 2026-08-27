from app.api.deps import get_loader
from app.inference.detector import deterministic_detections


def test_deterministic_detector_returns_valid_boxes():
    frame = get_loader().frame(1)
    detections = deterministic_detections(frame)
    assert detections
    assert all(detection.bbox.x2 > detection.bbox.x1 for detection in detections)
    assert all(detection.confidence > 0 for detection in detections)
