from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.api.deps import get_cached_detections  # noqa: E402
from app.mcap.export import export_results  # noqa: E402
from app.tracking.sort import build_tracks  # noqa: E402


if __name__ == "__main__":
    detections = list(get_cached_detections())
    output = export_results(ROOT / "data_samples" / "predictions" / "perception_replay.mcap", detections, build_tracks(detections))
    print(f"Exported {output}")
