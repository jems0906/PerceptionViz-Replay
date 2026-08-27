const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

async function getJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`)
  if (!response.ok) throw new Error(`Request failed: ${path}`)
  return response.json()
}

export function frameImageUrl(frame) {
  if (!frame) return ''
  return `${API_BASE_URL}${frame.image_url}`
}

export async function fetchReplayBundle() {
  const [frames, detections, tracks, metrics] = await Promise.all([
    getJson('/frames'),
    getJson('/detections'),
    getJson('/tracks'),
    getJson('/metrics'),
  ])
  return { frames, detections, tracks, metrics }
}

export async function runInference(frameId) {
  const response = await fetch(`${API_BASE_URL}/detect/${frameId}`, { method: 'POST' })
  if (!response.ok) throw new Error('Inference request failed')
  return response.json()
}
