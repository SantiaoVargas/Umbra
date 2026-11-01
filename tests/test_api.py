"""Tests de la capa API (sin levantar un servidor real: TestClient en memoria)."""

from fastapi.testclient import TestClient

from umbra.api.main import app

client = TestClient(app)


def test_health_responde_ok():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body
