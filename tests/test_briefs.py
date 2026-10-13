import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "sample_briefs.json"
BRIEFS = json.loads(DATA_FILE.read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def force_keyword_mode(monkeypatch):
    # Keep tests offline and free: never call a real LLM from the test suite.
    monkeypatch.setattr("app.analyzer.LLM_PROVIDER", "none")


def test_dataset_has_enough_cases():
    assert len(BRIEFS) >= 25
    assert len({b["id"] for b in BRIEFS}) == len(BRIEFS)


@pytest.mark.parametrize("case", BRIEFS, ids=lambda c: f"{c['id']}-{c['category']}")
def test_every_brief(case):
    r = client.post("/analyze", json={"brief": case["brief"]})

    # Briefs below the API's minimum length are rejected by validation.
    if len(case["brief"].strip()) < 10:
        assert r.status_code == 422
        return

    assert r.status_code == 200, r.text
    data = r.json()

    # Output shape must always be complete.
    for key in ("requirements", "risks", "clarifying_questions", "suggested_services"):
        assert key in data, f"missing {key}"
        assert isinstance(data[key], list)
    assert data["mode"] in ("llm", "keyword_fallback")

    # Real project briefs must produce useful output.
    # Edge cases (vague, fluff, non-English) only need to avoid crashing.
    if case["category"] != "edge":
        assert len(data["requirements"]) > 0
        assert len(data["clarifying_questions"]) > 0
        assert len(data["suggested_services"]) > 0