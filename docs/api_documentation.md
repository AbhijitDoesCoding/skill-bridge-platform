# API Documentation

Base URL: `http://localhost:8000`

## Health Check
- `GET /health`

## Upload Resume
- `POST /api/upload/resume`
- Multipart form field: `file`
- Supports PDF and plain text files.

## Upload Job Description
- `POST /api/upload/job-description`
- Multipart form field: `file`
- Supports PDF and plain text files.

## Generate Pathway
- `POST /api/analyze/pathway`
- JSON body:

```json
{
  "resume_data": {
    "skills": [{"name": "Python", "level": "intermediate", "years": 2}],
    "education": [],
    "total_experience_years": 2
  },
  "jd_data": {
    "required_skills": [{"name": "Machine Learning", "level": "intermediate", "priority": "must-have"}],
    "role_title": "ML Engineer",
    "role_category": "technical"
  },
  "preferences": {
    "time_budget_hours": 120
  }
}
```
