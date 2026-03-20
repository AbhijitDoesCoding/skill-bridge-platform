from __future__ import annotations

import logging

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api.models.schemas import AnalyzeResponse, PathwayRequest
from backend.core.gap_analyzer import SkillGapAnalyzer
from backend.core.pathway_generator import AdaptivePathwayGenerator
from backend.core.reasoning_trace import ReasoningTraceGenerator
from backend.core.skill_extractor import SkillExtractor
from backend.utils.config import settings
from backend.utils.data_loader import load_course_catalog
from backend.utils.pdf_parser import extract_text_from_pdf

logger = logging.getLogger(__name__)


app = FastAPI(title="AI-Adaptive Onboarding Engine", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list() or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Log full validation error details for easier debugging."""
    body = None
    try:
        body = await request.json()
    except Exception:
        pass
    logger.error("Validation error on %s %s", request.method, request.url.path)
    logger.error("Errors: %s", exc.errors())
    if body:
        logger.error("Request body: %s", body)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": body},
    )

skill_extractor = SkillExtractor()
gap_analyzer = SkillGapAnalyzer()
pathway_generator = AdaptivePathwayGenerator(load_course_catalog())
reasoning_trace_generator = ReasoningTraceGenerator()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


async def _read_upload_text(file: UploadFile) -> str:
    payload = await file.read()
    if file.filename and file.filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(payload)
    return payload.decode("utf-8", errors="ignore")


@app.post("/api/upload/resume")
async def upload_resume(file: UploadFile = File(...)) -> dict:
    try:
        text = await _read_upload_text(file)
        resume_data = skill_extractor.extract_from_resume(text)
        return {"status": "success", "data": resume_data, "raw_text": text}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/upload/job-description")
async def upload_job_description(file: UploadFile = File(...)) -> dict:
    try:
        text = await _read_upload_text(file)
        jd_data = skill_extractor.extract_from_job_description(text)
        return {"status": "success", "data": jd_data, "raw_text": text}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/analyze/pathway", response_model=AnalyzeResponse)
async def analyze_pathway(request: PathwayRequest) -> AnalyzeResponse:
    try:
        resume_data = request.resume_data.model_dump()
        jd_data = request.jd_data.model_dump()

        gap_analysis = gap_analyzer.analyze_gap(resume_data["skills"], jd_data["required_skills"])
        pathway = pathway_generator.generate_pathway(
            gap_analysis["gaps"],
            resume_data["skills"],
            request.preferences.time_budget_hours,
        )
        reasoning_trace = reasoning_trace_generator.generate_complete_trace(
            resume_data,
            jd_data,
            gap_analysis,
            pathway,
        )
        return AnalyzeResponse(
            status="success",
            gap_analysis=gap_analysis,
            pathway=pathway,
            reasoning_trace=reasoning_trace,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
