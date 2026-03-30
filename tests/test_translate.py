from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_translate() -> None:
    resp = client.post(
        "/translate",
        json={"text": "hello", "target_lang": "ja"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["target_lang"] == "ja"
    assert data["source_lang"] == "auto"
    assert data["translated_text"] == "hello"


def test_translate_missing_text() -> None:
    resp = client.post("/translate", json={"target_lang": "ja"})
    assert resp.status_code == 422
