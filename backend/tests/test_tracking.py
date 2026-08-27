from app.api.deps import get_cached_detections
from app.tracking.sort import build_tracks


def test_tracks_have_persistent_ids():
    tracks = build_tracks(list(get_cached_detections()))
    assert len(tracks) >= 3
    assert max(track.continuity for track in tracks) >= 8
