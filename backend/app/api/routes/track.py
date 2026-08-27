from fastapi import APIRouter

from app.api.deps import get_cached_detections
from app.schemas import Track
from app.tracking.sort import build_tracks

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("", response_model=list[Track])
def list_tracks() -> list[Track]:
    return build_tracks(list(get_cached_detections()))
