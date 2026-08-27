from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.api.deps import get_cached_detections, get_loader  # noqa: E402
from app.metrics.aggregate import aggregate_metrics  # noqa: E402


if __name__ == "__main__":
    metrics = aggregate_metrics(get_loader().frames(), list(get_cached_detections()))
    print(metrics.model_dump_json(indent=2))
