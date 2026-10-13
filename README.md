# TechAbout Client Requirement Analyzer

**Task ID:** ZR-26-00717  
**Source:** TechAbout parent company site (https://www.techabout.com)

A lightweight tool that accepts a free-text project brief and returns structured analysis:

- **Requirements** – extracted functional & non-functional needs
- **Risks** – technical, scope, timeline, compliance, data, and delivery risks
- **Clarifying Questions** – open questions that must be answered before accurate scoping
- **Suggested TechAbout Service Areas** – mapped to the live service catalogue with short justifications

## Features

- Clean web UI (paste brief → instant structured result)
- Structured JSON output (ready for CRM / Notion / Slack)
- Keyword + LLM hybrid analysis (works offline with keyword fallback)
- 25+ curated test briefs covering enterprise, Express, edge cases
- Documented limitations
- Ready for GitHub + live deployment

## Tech Stack

| Layer       | Choice                          | Why                                      |
|-------------|---------------------------------|------------------------------------------|
| Backend     | FastAPI + Pydantic              | Fast, typed, easy OpenAPI                |
| LLM         | OpenAI-compatible (Groq / OpenAI / Ollama) | Structured JSON, low cost / free tier   |
| Frontend    | Vanilla HTML + Tailwind CDN     | Zero build step, instant deploy          |
| Deployment  | Railway / Render + Vercel or single container | Simple, free tiers available           |

## Quick Start (Local)

```bash
# 1. Clone / open this folder in VS Code
cd techabout-requirement-analyzer

# 2. Create virtualenv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env → add GROQ_API_KEY or OPENAI_API_KEY (or leave empty for keyword-only mode)

# 5. Run
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000

## Environment Variables

See `.env.example`.

| Variable          | Required | Description                                      |
|-------------------|----------|--------------------------------------------------|
| `LLM_PROVIDER`    | No       | `groq` (default), `openai`, `ollama`, `none`     |
| `GROQ_API_KEY`    | If groq  | Free tier: https://console.groq.com              |
| `OPENAI_API_KEY`  | If openai| Optional                                         |
| `OLLAMA_BASE_URL` | If ollama| Default http://localhost:11434                   |
| `MODEL_NAME`      | No       | Override model (e.g. `llama-3.3-70b-versatile`)  |

## API

### `POST /analyze`

```json
{
  "brief": "We need a multi-tenant SaaS for inventory management with offline mobile app for warehouse staff..."
}
```

Response (structured):

```json
{
  "requirements": ["...", "..."],
  "risks": ["...", "..."],
  "clarifying_questions": ["...", "..."],
  "suggested_services": [
    {
      "service": "SaaS & Digital Platforms",
      "explanation": "Multi-tenant architecture and subscription billing are core to this brief.",
      "confidence": "high"
    }
  ],
  "summary": "Short executive summary...",
  "mode": "llm"   // or "keyword_fallback"
}
```

### `GET /health`

Simple health check.

### `GET /services`

Returns the full TechAbout service catalogue used for mapping.

## Test Suite

```bash
pytest tests/ -v
```

- 25+ sample briefs in `data/sample_briefs.json`
- Unit tests for parser, service mapper, and end-to-end analysis
- Edge cases: empty brief, non-English, pure marketing fluff, pure technical, Express-scale vs enterprise-scale

## Project Structure

```
techabout-requirement-analyzer/
├── app/
│   ├── main.py              # FastAPI app + routes
│   ├── analyzer.py          # Core analysis logic (LLM + keyword)
│   ├── services_catalog.py  # TechAbout services (scraped from site)
│   ├── models.py            # Pydantic schemas
│   └── static/              # Frontend (index.html)
├── data/
│   └── sample_briefs.json   # 25+ test cases
├── tests/
│   ├── test_analyzer.py
│   └── test_api.py
├── docs/
│   └── LIMITATIONS.md
├── .env.example
├── requirements.txt
├── README.md
└── Dockerfile               # Optional single-container deploy
```

## Deployment (Recommended)

### Option A – Railway (easiest)

1. Push to GitHub
2. New Project → Deploy from GitHub
3. Add environment variables
4. Railway gives you a public URL

### Option B – Render

Same as above. Free tier works for demo.

### Option C – Vercel (frontend) + Railway (API)

Split if you prefer pure static frontend.

## Commit History Recommendation

Make meaningful commits:

1. `feat: initial FastAPI skeleton + service catalogue`
2. `feat: keyword-based analyzer + service mapper`
3. `feat: LLM structured analysis (Groq/OpenAI)`
4. `feat: web UI`
5. `test: add 25 sample briefs + pytest suite`
6. `docs: README, limitations, .env.example`
7. `chore: Dockerfile + deployment notes`

## Limitations

See `docs/LIMITATIONS.md`.

## License

MIT (or as required by the task sheet).
