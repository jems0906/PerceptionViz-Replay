from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import detect, frames, health, metrics, track

app = FastAPI(title="PerceptionViz Replay", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(frames.router)
app.include_router(detect.router)
app.include_router(track.router)
app.include_router(metrics.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "PerceptionViz Replay", "docs": "/docs"}
