from app.api.deps import get_cached_detections, get_loader
from app.metrics.aggregate import aggregate_metrics


def test_aggregate_metrics_are_bounded():
    metrics = aggregate_metrics(get_loader().frames(), list(get_cached_detections()))
    assert 0 <= metrics.precision <= 1
    assert 0 <= metrics.recall <= 1
    assert metrics.frames[0].true_positives > 0
    assert "car" in metrics.per_class
