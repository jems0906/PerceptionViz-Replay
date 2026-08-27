from fastapi import APIRouter

from app.api.deps import get_cached_detections, get_loader
from app.metrics.aggregate import aggregate_metrics
from app.schemas import AggregateMetrics

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=AggregateMetrics)
def get_metrics() -> AggregateMetrics:
    return aggregate_metrics(get_loader().frames(), list(get_cached_detections()))
