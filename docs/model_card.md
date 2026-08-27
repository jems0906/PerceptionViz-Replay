# Model Card

## Model

The project is designed for Ultralytics YOLOv8n, the nano YOLOv8 detector intended for CPU-friendly object detection. The backend lazy-loads `backend/models/yolov8n.pt` when present, or lets Ultralytics resolve `yolov8n.pt`. For offline demos and fast CI, the app also ships deterministic YOLO-style detections generated from synthetic ground truth.

GitHub Actions runs `scripts/verify_model.py` after dependency installation. That check loads the real YOLOv8n weights through Ultralytics, runs inference on generated frame 1, and fails if the model cannot load or produces malformed output. Zero detections are accepted because the generated scene is not guaranteed to contain objects recognizable by YOLOv8n. The weights are intentionally downloaded by the model runtime rather than committed to source control.

## Intended Use

- Validate perception dashboard workflows on small driving scenes.
- Compare predicted boxes against ground truth labels frame by frame.
- Demonstrate tracker continuity, ID switch reporting, and MCAP export workflows.

## Limitations

- The bundled frames are synthetic and do not represent full road-scene domain complexity.
- Deterministic precomputed detections are for repeatable validation, not model quality claims.
- YOLOv8n is lightweight and can miss distant, occluded, or unusual road actors.
- 2D image boxes are projected into a simplified 3D scene using synthetic object positions.

## Failure Modes

- Small pedestrians can be missed, reducing recall.
- Overlapping vehicles can cause tracker ID switches.
- False positives can occur in road-edge regions with vehicle-like shapes.
- Domain shift from synthetic frames to real camera data requires additional validation.
