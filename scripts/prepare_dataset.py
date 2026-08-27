from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.data.loader import ensure_sample_dataset  # noqa: E402


if __name__ == "__main__":
    ensure_sample_dataset(ROOT / "data_samples")
    print("Synthetic sample dataset is ready in data_samples/.")
