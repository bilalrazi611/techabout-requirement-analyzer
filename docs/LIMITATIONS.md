# Limitations — TechAbout Client Requirement Analyzer

Documented as required by task ZR-26-00717.

## 1. Analysis Quality Depends on Brief Quality

- Extremely short, vague or pure marketing-language briefs produce shallow or generic output.
- The tool cannot invent missing business context (budget, timeline, compliance, volume, existing systems).
- Non-English briefs are only partially handled (keyword matching is English-centric; LLM may still extract meaning if the model supports the language).

## 2. LLM vs Keyword Mode

| Mode              | When used                          | Strengths                          | Weaknesses                                      |
|-------------------|------------------------------------|------------------------------------|-------------------------------------------------|
| LLM               | Valid API key present              | Rich requirements, risks, questions| Cost, latency, possible hallucination           |
| Keyword fallback  | No key / LLM failure               | Free, fast, deterministic          | Coarser requirements & risks                    |

Always run a human review before using the output for commercial proposals.

## 3. Service Mapping

- Mapping is based on keyword overlap + LLM understanding against a static catalogue derived from techabout.com (as of late 2025 / early 2026).
- New services added to the live site after the catalogue was frozen will not appear until the catalogue is updated.
- Confidence scores are heuristic, not probabilistic.

## 4. No Pricing or Timeline Estimates

The tool deliberately does **not** produce price or duration estimates. Those require discovery, capacity planning and commercial judgment.

## 5. Security & Privacy

- Briefs are sent to the configured LLM provider (Groq / OpenAI / Ollama).
- Do not paste highly confidential or regulated data unless the chosen provider and contract allow it.
- No briefs are stored by this application (stateless).

## 6. Not a Substitute for Discovery

This is a triage / pre-sales aid. It does not replace:

- Stakeholder interviews
- Technical due diligence
- Written scope of work
- Commercial negotiation

## 7. Test Coverage

- 27 sample briefs covering enterprise, Express, AI, cloud, security, IoT, blockchain, edge cases.
- Unit + API tests.
- Not an exhaustive formal verification suite.

## 8. Deployment & Operational Limits

- Free-tier LLM providers have rate limits.
- Single-process FastAPI is sufficient for demo / internal use; production would need workers, auth, rate-limiting and monitoring.
