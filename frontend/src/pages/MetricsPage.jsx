import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export default function MetricsPage({ metrics, detections, tracks }) {
  const iouRows = detections.filter((item) => item.iou !== null).map((item) => ({ name: `F${item.frame_id}-${item.class_name}`, iou: item.iou }))
  const classRows = metrics
    ? Object.entries(metrics.per_class).map(([className, values]) => ({ className, ...values }))
    : []

  return (
    <main className="metrics-page">
      <section className="chart-panel">
        <div className="panel-title">
          <span>IoU distribution</span>
          <strong>{detections.length} detections</strong>
        </div>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={iouRows}>
            <CartesianGrid strokeDasharray="3 3" stroke="#d6dee6" />
            <XAxis dataKey="name" hide />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Bar dataKey="iou" fill="#2563eb" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </section>
      <section className="chart-panel">
        <div className="panel-title">
          <span>Per-class validation</span>
          <strong>{tracks.length} tracks</strong>
        </div>
        <table className="data-table">
          <thead>
            <tr><th>Class</th><th>Precision</th><th>Recall</th><th>Mean IoU</th></tr>
          </thead>
          <tbody>
            {classRows.map((row) => (
              <tr key={row.className}>
                <td>{row.className}</td>
                <td>{row.precision.toFixed(2)}</td>
                <td>{row.recall.toFixed(2)}</td>
                <td>{row.mean_iou.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  )
}
