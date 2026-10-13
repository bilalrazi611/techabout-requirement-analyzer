from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "llm_provider" in data


def test_services():
    r = client.get("/services")
    assert r.status_code == 200
    data = r.json()
    assert "enterprise" in data
    assert "express" in data
    assert len(data["enterprise"]) >= 8


def test_analyze_ok():
    r = client.post(
        "/analyze",
        json={
            "brief": "We need a multi-tenant SaaS for inventory with offline mobile apps and SAP integration."
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "requirements" in data
    assert "risks" in data
    assert "clarifying_questions" in data
    assert "suggested_services" in data
    assert data["mode"] in ("llm", "keyword_fallback")


def test_analyze_too_short():
    # FastAPI/Pydantic rejects input that fails validation with 422
    r = client.post("/analyze", json={"brief": "hi"})
    assert r.status_code == 422


def test_index_returns_html():
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]