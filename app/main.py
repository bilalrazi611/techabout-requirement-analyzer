import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from .models import AnalyzeRequest, AnalysisResult, HealthResponse
from .analyzer import analyze_brief, LLM_PROVIDER, _default_model, _get_client
from .services_catalog import ALL_SERVICES

load_dotenv()

app = FastAPI(
    title="TechAbout Client Requirement Analyzer",
    description="Paste a project brief → get structured requirements, risks, clarifying questions and suggested TechAbout services.",
    version="1.0.0",
)

STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h1>TechAbout Analyzer</h1><p>Frontend not found. API is live at /docs</p>")


@app.get("/health", response_model=HealthResponse)
async def health():
    client = _get_client()
    return HealthResponse(
        status="ok",
        llm_provider=LLM_PROVIDER,
        model=_default_model() if client else None,
    )


@app.get("/services")
async def list_services():
    return {
        "enterprise": [s for s in ALL_SERVICES if s["id"] not in [
            "express-web-migration", "express-ecommerce", "express-wordpress",
            "express-mobile", "express-seo", "express-security"
        ]],
        "express": [s for s in ALL_SERVICES if s["id"].startswith("express-")],
    }


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(req: AnalyzeRequest):
    if not req.brief or len(req.brief.strip()) < 10:
        raise HTTPException(status_code=400, detail="Brief must be at least 10 characters.")
    result = analyze_brief(req.brief)
    return result
