from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_translate_success(mock_translate_success: AsyncMock) -> None:
    resp = client.post(
        "/translate",
        json={"text": "hello", "target_lang": "ja"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["translated_text"] == "こんにちは"
    assert data["target_lang"] == "ja"
    assert data["source_lang"] == "auto"


def test_translate_with_source_lang(
    mock_translate_success: AsyncMock,
) -> None:
    resp = client.post(
        "/translate",
        json={"text": "hello", "source_lang": "en", "target_lang": "ja"},
    )
    assert resp.status_code == 200
    mock_translate_success.assert_called_once_with(
        text="hello", target_lang="ja", source_lang="en"
    )


def test_translate_missing_text() -> None:
    resp = client.post("/translate", json={"target_lang": "ja"})
    assert resp.status_code == 422


def test_translate_empty_text() -> None:
    resp = client.post("/translate", json={"text": "", "target_lang": "ja"})
    assert resp.status_code == 422


def test_translate_timeout(mock_translate_timeout: AsyncMock) -> None:
    resp = client.post(
        "/translate",
        json={"text": "hello", "target_lang": "ja"},
    )
    assert resp.status_code == 504
    assert "timed out" in resp.json()["detail"]


def test_translate_api_error(mock_translate_error: AsyncMock) -> None:
    resp = client.post(
        "/translate",
        json={"text": "hello", "target_lang": "ja"},
    )
    assert resp.status_code == 502
    assert "500" in resp.json()["detail"]
