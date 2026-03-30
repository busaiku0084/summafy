from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_languages_returns_list() -> None:
    resp = client.get("/translate/languages")
    assert resp.status_code == 200
    data = resp.json()
    assert "languages" in data
    assert len(data["languages"]) > 0
    lang = data["languages"][0]
    assert "code" in lang
    assert "name" in lang


def test_languages_contains_common() -> None:
    resp = client.get("/translate/languages")
    codes = {lang["code"] for lang in resp.json()["languages"]}
    assert {"en", "ja", "es", "fr", "zh"}.issubset(codes)
