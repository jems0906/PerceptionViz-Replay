# PerceptionViz Replay Architecture

PerceptionViz Replay is a two-service web application. The FastAPI backend owns dataset loading, optional YOLOv8n inference, precomputed detection loading, SORT-style tracking, metric aggregation, Parquet persistence, and MCAP export. The React frontend owns frame replay, 2D and 3D visualization, per-frame inspection, track timeline analysis, and metric exploration.

```mermaid
flowchart LR
    Frames[Sample camera frames + GT labels] --> Backend[FastAPI backend]
    Backend --> Detector[YOLOv8n or deterministic precompute]
    Detector --> Tracker[SORT tracker]
    Tracker --> Metrics[Validation metrics]
    Tracker --> Parquet[PyArrow Parquet]
    Tracker --> MCAP[MCAP export]
    Backend --> UI[React dashboard]
    UI --> Camera[2D camera overlay]
    UI --> Three[Three.js scene viewer]
    UI --> Timeline[Track timeline]
```

The default runtime path uses precomputed detections to keep Railway page loads quick. The `POST /detect/{frame_id}` endpoint remains available to run frame-level inference behavior from the dashboard.
