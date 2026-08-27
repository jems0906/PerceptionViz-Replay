from __future__ import annotations

from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from app.schemas import Detection


def detections_to_rows(detections: list[Detection]) -> list[dict]:
    rows = []
    for detection in detections:
        rows.append(
            {
                "id": detection.id,
                "frame_id": detection.frame_id,
                "class_name": detection.class_name,
                "confidence": detection.confidence,
                "x1": detection.bbox.x1,
                "y1": detection.bbox.y1,
                "x2": detection.bbox.x2,
                "y2": detection.bbox.y2,
                "position_x": detection.position[0],
                "position_y": detection.position[1],
                "position_z": detection.position[2],
                "matched_gt_id": detection.matched_gt_id,
                "iou": detection.iou,
                "track_id": detection.track_id,
            }
        )
    return rows


def write_detections(path: Path, detections: list[Detection]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(detections_to_rows(detections))
    pq.write_table(table, path)


def read_detections(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return pd.read_parquet(path).to_dict(orient="records")
