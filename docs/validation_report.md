# Validation Report

## Dataset

The validation set contains 12 synthetic driving frames with labeled cars, trucks, and pedestrians. Each frame has 2D bounding boxes and simplified 3D positions for scene rendering.

## Current Results

The deterministic precomputed detector intentionally includes a small number of false positives and missed pedestrians so the dashboard shows realistic inspection cases.

| Class | Expected behavior | Common failure |
| --- | --- | --- |
| car | High precision and recall across frames | Occasional false positive parked near road edge |
| truck | Stable detection and tracking | Box drift under apparent scale change |
| person | Lower recall on selected frames | Missed small actor near lane boundary |

## Metric Definitions

- Precision: true positives divided by all predictions.
- Recall: true positives divided by all ground truth labels.
- IoU: box intersection over union for matched prediction and ground truth.
- False positive: prediction not matched to ground truth at IoU >= 0.5.
- False negative: ground truth not matched by any prediction at IoU >= 0.5.
- Track continuity: number of frames where a track ID appears.
- ID switch: a matched ground truth object receives a different track ID over time.

## Next Validation Steps

1. Replace synthetic frames with a small public sample such as KITTI or nuScenes mini exports.
2. Record side-by-side YOLOv8n results and deterministic baseline results.
3. Add review tags for occlusion, truncation, lighting, and actor distance.
4. Export MCAP results and validate playback in Foxglove.
