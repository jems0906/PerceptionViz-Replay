from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

from app.schemas import FrameRecord, GroundTruthBox


FRAME_WIDTH = 960
FRAME_HEIGHT = 540


def _box(x1: float, y1: float, x2: float, y2: float) -> dict[str, float]:
    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}


def _synthetic_frames() -> list[dict]:
    frames = []
    for index in range(12):
        car_x = 150 + index * 42
        truck_x = 640 - index * 18
        ped_x = 440 + index * 7
        frames.append(
            {
                "id": index + 1,
                "timestamp": round(index * 0.1, 2),
                "image": f"frame_{index + 1:04d}.jpg",
                "width": FRAME_WIDTH,
                "height": FRAME_HEIGHT,
                "ego_pose": [index * 1.5, 0.0, 0.0],
                "ground_truth": [
                    {
                        "id": "vehicle-a",
                        "class_name": "car",
                        "bbox": _box(car_x, 292, car_x + 112, 372),
                        "position": [index * 3.5 + 8, -1.5, 0.0],
                    },
                    {
                        "id": "vehicle-b",
                        "class_name": "truck",
                        "bbox": _box(truck_x, 270, truck_x + 142, 382),
                        "position": [45 - index * 1.7, 2.2, 0.0],
                    },
                    {
                        "id": "pedestrian-a",
                        "class_name": "person",
                        "bbox": _box(ped_x, 278, ped_x + 38, 374),
                        "position": [24 + index * 0.8, -4.0, 0.0],
                    },
                ],
            }
        )
    return frames


def ensure_sample_dataset(data_root: Path) -> None:
    frames_dir = data_root / "frames"
    labels_dir = data_root / "labels"
    predictions_dir = data_root / "predictions"
    frames_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    predictions_dir.mkdir(parents=True, exist_ok=True)

    frames = _synthetic_frames()
    ground_truth_path = labels_dir / "ground_truth.json"
    if not ground_truth_path.exists():
        ground_truth_path.write_text(json.dumps({"frames": frames}, indent=2), encoding="utf-8")

    for frame in frames:
        image_path = frames_dir / frame["image"]
        if image_path.exists():
            continue
        image = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), "#d8e6ee")
        draw = ImageDraw.Draw(image)
        draw.rectangle([0, 344, FRAME_WIDTH, FRAME_HEIGHT], fill="#4b5563")
        for lane_y in (382, 438):
            for stripe_x in range(-80, FRAME_WIDTH, 170):
                draw.rectangle([stripe_x + frame["id"] * 12, lane_y, stripe_x + 78 + frame["id"] * 12, lane_y + 6], fill="#f8fafc")
        draw.rectangle([0, 250, FRAME_WIDTH, 344], fill="#718096")
        for item in frame["ground_truth"]:
            box = item["bbox"]
            fill = {"car": "#0ea5e9", "truck": "#f97316", "person": "#22c55e"}[item["class_name"]]
            draw.rounded_rectangle([box["x1"], box["y1"], box["x2"], box["y2"]], radius=6, fill=fill, outline="#111827", width=3)
        image.save(image_path, quality=88)


class DatasetLoader:
    def __init__(self, data_root: Path):
        self.data_root = data_root
        ensure_sample_dataset(data_root)

    def frames(self) -> list[FrameRecord]:
        payload = json.loads((self.data_root / "labels" / "ground_truth.json").read_text(encoding="utf-8"))
        return [self._to_frame(frame) for frame in payload["frames"]]

    def frame(self, frame_id: int) -> FrameRecord:
        for frame in self.frames():
            if frame.id == frame_id:
                return frame
        raise KeyError(f"Frame {frame_id} was not found")

    def image_path(self, frame_id: int) -> Path:
        self.frame(frame_id)
        return self.data_root / "frames" / f"frame_{frame_id:04d}.jpg"

    def _to_frame(self, frame: dict) -> FrameRecord:
        return FrameRecord(
            id=frame["id"],
            timestamp=frame["timestamp"],
            image_url=f"/frames/{frame['id']}/image",
            width=frame["width"],
            height=frame["height"],
            ego_pose=tuple(frame["ego_pose"]),
            ground_truth=[GroundTruthBox(**item) for item in frame["ground_truth"]],
        )
