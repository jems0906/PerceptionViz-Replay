from __future__ import annotations

from app.schemas import Detection, FrameMetrics, FrameRecord, GroundTruthBox


def iou(box_a, box_b) -> float:
    left = max(box_a.x1, box_b.x1)
    top = max(box_a.y1, box_b.y1)
    right = min(box_a.x2, box_b.x2)
    bottom = min(box_a.y2, box_b.y2)
    intersection = max(0.0, right - left) * max(0.0, bottom - top)
    area_a = max(0.0, box_a.x2 - box_a.x1) * max(0.0, box_a.y2 - box_a.y1)
    area_b = max(0.0, box_b.x2 - box_b.x1) * max(0.0, box_b.y2 - box_b.y1)
    union = area_a + area_b - intersection
    return intersection / union if union else 0.0


def match_detections(frame: FrameRecord, detections: list[Detection], iou_threshold: float = 0.5) -> list[Detection]:
    unmatched_gt: list[GroundTruthBox] = list(frame.ground_truth)
    matched: list[Detection] = []
    for detection in sorted(detections, key=lambda item: item.confidence, reverse=True):
        candidates = [(gt, iou(detection.bbox, gt.bbox)) for gt in unmatched_gt if gt.class_name == detection.class_name]
        best_gt, best_iou = max(candidates, key=lambda item: item[1], default=(None, 0.0))
        if best_gt and best_iou >= iou_threshold:
            unmatched_gt.remove(best_gt)
            detection = detection.model_copy(update={"matched_gt_id": best_gt.id, "iou": round(best_iou, 4)})
        else:
            detection = detection.model_copy(update={"matched_gt_id": None, "iou": 0.0})
        matched.append(detection)
    return matched


def frame_metrics(frame: FrameRecord, detections: list[Detection], iou_threshold: float = 0.5) -> FrameMetrics:
    matched = match_detections(frame, detections, iou_threshold)
    true_positives = sum(1 for detection in matched if detection.matched_gt_id)
    false_positives = len(matched) - true_positives
    false_negatives = len(frame.ground_truth) - true_positives
    precision = true_positives / len(matched) if matched else 0.0
    recall = true_positives / len(frame.ground_truth) if frame.ground_truth else 0.0
    ious = [detection.iou or 0.0 for detection in matched if detection.matched_gt_id]
    mean_iou = sum(ious) / len(ious) if ious else 0.0
    return FrameMetrics(
        frame_id=frame.id,
        precision=round(precision, 4),
        recall=round(recall, 4),
        mean_iou=round(mean_iou, 4),
        false_positives=false_positives,
        false_negatives=false_negatives,
        true_positives=true_positives,
    )
