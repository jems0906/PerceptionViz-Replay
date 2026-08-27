from fastapi import APIRouter, HTTPException

from app.api.deps import get_cached_detections, run_frame_detection
from app.schemas import Detection

router = APIRouter(tags=["detect"])


@router.get("/detections", response_model=list[Detection])
def list_detections() -> list[Detection]:
    return list(get_cached_detections())


@router.post("/detect/{frame_id}", response_model=list[Detection])
def detect_frame(frame_id: int) -> list[Detection]:
    try:
        return run_frame_detection(frame_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
