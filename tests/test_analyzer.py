import json
from pathlib import Path

import pytest

from app.analyzer import analyze_brief, _keyword_service_match
from app.models import AnalysisResult

DATA_PATH = Path(__file__).parent.parent / "data" / "sample_briefs.json"


@pytest.fixture
def sample_briefs():
    with open(DATA_PATH) as f:
        return json.load(f)


def test_sample_count(sample_briefs):
    assert len(sample_briefs) >= 25, "Must have at least 25 sample briefs"


def test_analyze_returns_structure():
    result = analyze_brief(
        "We need a React Native mobile app with offline support and SAP integration."
    )
    assert isinstance(result, AnalysisResult)
    assert isinstance(result.requirements, list)
    assert isinstance(result.risks, list)
    assert isinstance(result.clarifying_questions, list)
    assert isinstance(result.suggested_services, list)
    assert result.brief_length > 0
    assert result.mode in ("llm", "keyword_fallback")


def test_too_short_brief():
    result = analyze_brief("hi")
    assert len(result.risks) >= 1
    assert "short" in result.risks[0].lower() or "insufficient" in result.summary.lower()


def test_keyword_match_ai():
    suggestions = _keyword_service_match(
        "Build a RAG system with LLMs and vector embeddings for internal docs"
    )
    names = [s.service.lower() for s in suggestions]
    assert any("ai" in n or "machine learning" in n for n in names)


def test_keyword_match_saas():
    suggestions = _keyword_service_match(
        "Multi-tenant SaaS platform with subscription billing and RBAC"
    )
    names = [s.service.lower() for s in suggestions]
    assert any("saas" in n for n in names)


def test_all_samples_produce_output(sample_briefs):
    """Every sample brief should produce a valid AnalysisResult without crashing."""
    for item in sample_briefs:
        result = analyze_brief(item["brief"])
        assert isinstance(result, AnalysisResult)
        # Even edge cases should return something
        assert result.mode in ("llm", "keyword_fallback")


def test_enterprise_brief_has_services(sample_briefs):
    enterprise = next(b for b in sample_briefs if b["id"] == 1)
    result = analyze_brief(enterprise["brief"])
    assert len(result.suggested_services) >= 1
    # Should surface SaaS or mobile or enterprise software
    service_names = " ".join(s.service.lower() for s in result.suggested_services)
    assert any(
        kw in service_names
        for kw in ["saas", "mobile", "enterprise", "web"]
    )
