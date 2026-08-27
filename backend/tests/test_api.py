from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_and_replay_endpoints():
    assert client.get("/health").json()["status"] == "ok"
    frames = client.get("/frames").json()
    assert len(frames) == 12
    assert client.get("/frames/1/image").status_code == 200
    assert client.post("/detect/1").status_code == 200
    assert client.get("/metrics").json()["precision"] > 0
