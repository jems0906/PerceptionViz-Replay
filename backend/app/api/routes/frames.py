from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.api.deps import get_loader
from app.schemas import FrameRecord

router = APIRouter(prefix="/frames", tags=["frames"])


@router.get("", response_model=list[FrameRecord])
def list_frames() -> list[FrameRecord]:
    return get_loader().frames()


@router.get("/{frame_id}", response_model=FrameRecord)
def get_frame(frame_id: int) -> FrameRecord:
    try:
        return get_loader().frame(frame_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{frame_id}/image")
def get_frame_image(frame_id: int) -> FileResponse:
    try:
        return FileResponse(get_loader().image_path(frame_id), media_type="image/jpeg")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
