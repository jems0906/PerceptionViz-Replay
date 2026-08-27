from __future__ import annotations

import json
import time
from pathlib import Path

from mcap.writer import Writer

from app.data.parquet_store import detections_to_rows
from app.schemas import Detection, Track


def export_results(path: Path, detections: list[Detection], tracks: list[Track]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as stream:
        writer = Writer(stream)
        writer.start()
        schema_id = writer.register_schema(name="perceptionviz.PerceptionFrame", encoding="jsonschema", data=b"{}")
        channel_id = writer.register_channel(topic="/perceptionviz/replay", message_encoding="json", schema_id=schema_id)
        now = time.time_ns()
        frame_ids = sorted({detection.frame_id for detection in detections})
        for frame_id in frame_ids:
            payload = {
                "frame_id": frame_id,
                "detections": [row for row in detections_to_rows(detections) if row["frame_id"] == frame_id],
                "tracks": [track.model_dump() for track in tracks if any(point.frame_id == frame_id for point in track.points)],
            }
            writer.add_message(channel_id=channel_id, log_time=now + frame_id, publish_time=now + frame_id, data=json.dumps(payload).encode())
        writer.finish()
    return path
