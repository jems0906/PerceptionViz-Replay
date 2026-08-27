import { useEffect, useRef } from 'react'
import * as THREE from 'three'

const colors = { car: 0x2563eb, truck: 0xea580c, person: 0x16a34a }

export default function SceneViewer({ frame, detections, tracks }) {
  const mountRef = useRef(null)

  useEffect(() => {
    if (!mountRef.current) return undefined
    const mount = mountRef.current
    const width = mount.clientWidth
    const height = mount.clientHeight
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0xf6f8fb)
    const camera = new THREE.PerspectiveCamera(48, width / height, 0.1, 300)
    camera.position.set(34, 34, 42)
    camera.lookAt(28, 0, 0)
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.setSize(width, height)
    mount.appendChild(renderer.domElement)

    const grid = new THREE.GridHelper(90, 18, 0x9ca3af, 0xd1d5db)
    scene.add(grid)
    const road = new THREE.Mesh(new THREE.BoxGeometry(90, 0.08, 14), new THREE.MeshBasicMaterial({ color: 0x4b5563 }))
    road.position.set(28, -0.05, 0)
    scene.add(road)

    const light = new THREE.DirectionalLight(0xffffff, 1.8)
    light.position.set(10, 22, 14)
    scene.add(light)
    scene.add(new THREE.AmbientLight(0xffffff, 1.2))

    detections.forEach((det) => {
      const size = det.class_name === 'person' ? [0.8, 1.8, 0.8] : det.class_name === 'truck' ? [3.2, 1.8, 1.7] : [2.2, 1.3, 1.4]
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(...size), new THREE.MeshStandardMaterial({ color: colors[det.class_name] ?? 0x334155 }))
      mesh.position.set(det.position[0], size[1] / 2, det.position[1])
      scene.add(mesh)
    })

    tracks.forEach((track) => {
      const points = track.points.map((point) => new THREE.Vector3(point.position[0], 0.08, point.position[1]))
      if (points.length > 1) {
        scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), new THREE.LineBasicMaterial({ color: colors[track.class_name] ?? 0x111827 })))
      }
    })

    let animationId = 0
    const animate = () => {
      animationId = requestAnimationFrame(animate)
      renderer.render(scene, camera)
    }
    animate()
    return () => {
      cancelAnimationFrame(animationId)
      renderer.dispose()
      mount.removeChild(renderer.domElement)
    }
  }, [frame, detections, tracks])

  return <div ref={mountRef} className="scene-viewer" />
}
