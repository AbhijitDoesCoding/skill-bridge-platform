# AI-Adaptive Onboarding Engine

An AI-driven onboarding system that analyzes skill gaps between a candidate profile and a target role, then generates a personalized learning pathway.

## Features
- Resume and job description parsing (PDF/text)
- LLM extraction via Groq API with deterministic fallback
- Skill normalization against a grounded taxonomy
- Gap analysis with readiness score
- DAG-based adaptive learning pathway generation
- Reasoning trace for transparent recommendations
- React UI for uploads, charts, and pathway visualization

## Project Structure
```
backend/
  api/
  core/
  data/
  utils/
frontend/
tests/
docs/
```

## Local Setup

### 1) Backend
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate

pip install -r backend/requirements.txt
cp .env.example .env  # use copy on Windows
# Add GROQ_API_KEY in .env for LLM extraction
uvicorn backend.api.main:app --reload
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`  
Backend URL: `http://localhost:8000`

## Docker
```bash
docker-compose up --build
```

## Tests
```bash
pytest tests -v
```

## API Endpoints
- `POST /api/upload/resume`
- `POST /api/upload/job-description`
- `POST /api/analyze/pathway`

## Environment Variables
- `GROQ_API_KEY`: API key for Groq LLM extraction
- `GROQ_MODEL`: defaults to `llama-3.3-70b-versatile`

## Compliance Notes
- Adaptive logic is implemented in-house (`backend/core/pathway_generator.py`).
- Grounding is enforced through `backend/data/course_catalog.json` and `backend/data/skill_taxonomy.json`.
- Reasoning trace is included in pathway responses.
