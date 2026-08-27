# UI Feedback Backlog

| Priority | Request | Product translation | Acceptance signal |
| --- | --- | --- | --- |
| P0 | Show exactly where false positives happen. | Add per-frame FP/FN filters and jump controls. | Engineer can jump to every FP frame in under 2 clicks. |
| P0 | Make track ID switches obvious during replay. | Highlight timeline segments where matched GT changes track ID. | ID switch frames are visually marked in the timeline. |
| P1 | Compare two model versions. | Add model-run selector and metric delta panel. | User can compare precision, recall, and IoU deltas by class. |
| P1 | Export a review artifact for model owners. | Add MCAP download and validation markdown export. | Review package includes detections, tracks, metrics, and notes. |
| P2 | Debug 3D alignment issues. | Add camera calibration and projected-box overlay controls. | User can toggle 2D/3D projection aids. |
| P2 | Support longer drives. | Add frame virtualization and Parquet-backed pagination. | 1,000-frame replay remains responsive. |
