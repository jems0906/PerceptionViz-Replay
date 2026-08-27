export default function DetectionTable({ detections }) {
  return (
    <div className="table-panel">
      <div className="panel-title"><span>Detection details</span><strong>{detections.length} rows</strong></div>
      <table className="data-table">
        <thead>
          <tr><th>ID</th><th>Class</th><th>Conf</th><th>Track</th><th>IoU</th><th>Match</th></tr>
        </thead>
        <tbody>
          {detections.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.class_name}</td>
              <td>{item.confidence.toFixed(2)}</td>
              <td>T{item.track_id}</td>
              <td>{item.iou?.toFixed(2) ?? '-'}</td>
              <td>{item.matched_gt_id ?? 'FP'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
