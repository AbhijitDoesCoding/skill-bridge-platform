# Architecture Overview

## Data Flow
1. Frontend uploads resume and job description files.
2. Backend extracts text from PDF/TXT and runs skill extraction.
3. Extracted skills are normalized against taxonomy.
4. Gap analyzer compares current and target competency requirements.
5. Pathway generator maps gaps to curated course catalog and resolves prerequisites with a DAG.
6. Reasoning trace generator produces human-readable decision explanations.
7. Frontend renders skill-gap chart, learning pathway graph, and reasoning panels.

## Core Components
- `backend/core/skill_extractor.py`: LLM-first extraction with deterministic fallback.
- `backend/core/gap_analyzer.py`: prioritizes and scores missing competencies.
- `backend/core/pathway_generator.py`: prerequisite-safe adaptive path generation.
- `backend/core/reasoning_trace.py`: transparency outputs for judging criteria.

## Reliability Guarantees
- Course recommendations are catalog-grounded only.
- Skill labels are normalized through a local taxonomy.
- Prerequisite cycles are rejected at startup.
