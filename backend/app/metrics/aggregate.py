from __future__ import annotations

from collections import defaultdict

from app.metrics.detection import frame_metrics, match_detections
from app.metrics.tracking import id_switch_count, track_continuity
from app.schemas import AggregateMetrics, Detection, FrameRecord


def aggregate_metrics(frames: list[FrameRecord], detections: list[Detection], iou_threshold: float = 0.5) -> AggregateMetrics:
    by_frame: dict[int, list[Detection]] = defaultdict(list)
    for detection in detections:
        by_frame[detection.frame_id].append(detection)

    frame_rows = [frame_metrics(frame, by_frame[frame.id], iou_threshold) for frame in frames]
    true_positives = sum(row.true_positives for row in frame_rows)
    false_positives = sum(row.false_positives for row in frame_rows)
    false_negatives = sum(row.false_negatives for row in frame_rows)
    total_iou = sum(row.mean_iou * row.true_positives for row in frame_rows)
    precision = true_positives / (true_positives + false_positives) if true_positives + false_positives else 0.0
    recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives else 0.0

    per_class_counts: dict[str, dict[str, float]] = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0, "iou_sum": 0.0})
    for frame in frames:
        matched = match_detections(frame, by_frame[frame.id], iou_threshold)
        for gt in frame.ground_truth:
            if not any(item.matched_gt_id == gt.id for item in matched):
                per_class_counts[gt.class_name]["fn"] += 1
        for detection in matched:
            bucket = per_class_counts[detection.class_name]
            if detection.matched_gt_id:
                bucket["tp"] += 1
                bucket["iou_sum"] += detection.iou or 0.0
            else:
                bucket["fp"] += 1

    per_class = {}
    for class_name, counts in per_class_counts.items():
        tp = counts["tp"]
        fp = counts["fp"]
        fn = counts["fn"]
        per_class[class_name] = {
            "precision": round(tp / (tp + fp), 4) if tp + fp else 0.0,
            "recall": round(tp / (tp + fn), 4) if tp + fn else 0.0,
            "mean_iou": round(counts["iou_sum"] / tp, 4) if tp else 0.0,
        }

    return AggregateMetrics(
        frames=frame_rows,
        precision=round(precision, 4),
        recall=round(recall, 4),
        mean_iou=round(total_iou / true_positives, 4) if true_positives else 0.0,
        id_switches=id_switch_count(detections),
        track_continuity=track_continuity(detections),
        per_class=per_class,
    )
