from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.api.deps import get_cached_detections  # noqa: E402


if __name__ == "__main__":
    detections = get_cached_detections()
    print(f"Wrote {len(detections)} precomputed detections to data_samples/predictions/precomputed_detections.parquet")
