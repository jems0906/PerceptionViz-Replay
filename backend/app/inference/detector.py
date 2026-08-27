from __future__ import annotations

from importlib import import_module
from pathlib import Path

from app.schemas import Box, Detection, FrameRecord


YOLO_CLASS_MAP = {0: "person", 2: "car", 5: "bus", 7: "truck"}


class YoloDetector:
    def __init__(self, model_path: Path, confidence_threshold: float = 0.25):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self._model = None

    def _load(self):
        if self._model is None:
            YOLO = import_module("ultralytics").YOLO
            self._model = YOLO(str(self.model_path) if self.model_path.exists() else "yolov8n.pt")
        return self._model

    def detect(self, image_path: Path, frame: FrameRecord) -> list[Detection]:
        model = self._load()
        results = model(str(image_path), conf=self.confidence_threshold, verbose=False)
        detections: list[Detection] = []
        for result in results:
            for index, box in enumerate(result.boxes):
                class_id = int(box.cls[0])
                class_name = YOLO_CLASS_MAP.get(class_id)
                if class_name is None:
                    class_name = result.names.get(class_id)
                if class_name is None:
                    class_name = str(class_id)
                xyxy = [float(value) for value in box.xyxy[0].tolist()]
                center_x = ((xyxy[0] + xyxy[2]) / 2 / frame.width) * 60
                lateral = ((xyxy[0] + xyxy[2]) / 2 / frame.width - 0.5) * 8
                detections.append(
                    Detection(
                        id=f"yolo-{frame.id}-{index}",
                        frame_id=frame.id,
                        class_name=class_name,
                        confidence=float(box.conf[0]),
                        bbox=Box(x1=xyxy[0], y1=xyxy[1], x2=xyxy[2], y2=xyxy[3]),
                        position=(center_x, lateral, 0.0),
                    )
                )
        return detections


def deterministic_detections(frame: FrameRecord) -> list[Detection]:
    detections: list[Detection] = []
    for index, gt in enumerate(frame.ground_truth):
        drift = ((frame.id + index) % 3 - 1) * 4
        missed_person = gt.class_name == "person" and frame.id in {4, 9}
        if missed_person:
            continue
        detections.append(
            Detection(
                id=f"det-{frame.id}-{index}",
                frame_id=frame.id,
                class_name=gt.class_name,
                confidence=round(0.91 - index * 0.08 - frame.id * 0.004, 3),
                bbox=Box(
                    x1=gt.bbox.x1 + drift,
                    y1=gt.bbox.y1 + drift * 0.25,
                    x2=gt.bbox.x2 + drift,
                    y2=gt.bbox.y2 + drift * 0.25,
                ),
                position=(gt.position[0] + drift * 0.03, gt.position[1], gt.position[2]),
            )
        )
    if frame.id in {3, 7, 11}:
        detections.append(
            Detection(
                id=f"det-{frame.id}-fp",
                frame_id=frame.id,
                class_name="car",
                confidence=0.38,
                bbox=Box(x1=760, y1=286, x2=836, y2=344),
                position=(34 + frame.id, 5.6, 0.0),
            )
        )
    return detections
