# PerceptionViz Replay

A web app that replays driving scenes, runs or loads perception model outputs, compares predictions against ground truth, and visualizes model behavior with 2D overlays, Three.js 3D rendering, metrics, tracks, Parquet storage, and MCAP export.

## Features

- FastAPI backend with `/frames`, `/detections`, `/detect/{frame_id}`, `/tracks`, `/metrics`, and `/health` endpoints.
- Synthetic driving sample generator with camera frames and ground truth labels.
- YOLOv8n-compatible detector wrapper plus deterministic precomputed detections for quick Railway startup.
- SORT-style tracker with persistent IDs, continuity metrics, and ID switch reporting.
- Detection precision, recall, IoU, false positive, and false negative metrics.
- PyArrow Parquet output at `data_samples/predictions/precomputed_detections.parquet`.
- MCAP export script at `scripts/export_mcap.py`.
- React + Vite dashboard with 2D camera overlays, Three.js scene view, metrics charts, track timeline, and frame inspector.

## Run locally

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ..\scripts\prepare_dataset.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Useful commands

```powershell
pytest backend/tests
python scripts/run_inference.py
python scripts/evaluate_tracks.py
python scripts/export_mcap.py
npm run build --prefix frontend
```

## Deployment

`railway.json` defines one Railway service built from the root `Dockerfile`. The image builds the React frontend and serves it from FastAPI alongside the API on the same public port. The backend uses precomputed detections by default for fast page loads while keeping `POST /detect/{frame_id}` available for on-demand sample-frame inference.
