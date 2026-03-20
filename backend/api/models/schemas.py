from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


Level = Literal["none", "beginner", "intermediate", "advanced"]
Priority = Literal["must-have", "nice-to-have"]


def _normalize_level(value: str) -> str:
    normalized = (value or "").strip().lower()
    if normalized in {"none", "beginner", "intermediate", "advanced"}:
        return normalized
    if "expert" in normalized or "advanced" in normalized or "senior" in normalized:
        return "advanced"
    if "inter" in normalized or "proficient" in normalized:
        return "intermediate"
    if "basic" in normalized or "junior" in normalized:
        return "beginner"
    return "beginner"


def _normalize_priority(value: str) -> str:
    normalized = (value or "").strip().lower().replace("_", "-").replace(" ", "-")
    if normalized in {"must-have", "must", "required"}:
        return "must-have"
    return "nice-to-have"


def _to_float(value: object, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().lower()
    if not text or text in {"none", "null", "n/a", "na", "unknown"}:
        return default
    text = text.replace("years", "").replace("year", "").strip()
    try:
        return float(text)
    except ValueError:
        return default


def _to_optional_float(value: object) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().lower()
    if not text or text in {"none", "null", "n/a", "na", "unknown"}:
        return None
    text = text.replace("years", "").replace("year", "").strip()
    try:
        return float(text)
    except ValueError:
        return None


class SkillEvidence(BaseModel):
    model_config = {"extra": "ignore"}

    name: str
    level: Level = "beginner"
    years: Optional[float] = None

    @field_validator("level", mode="before")
    @classmethod
    def normalize_level(cls, value: object) -> str:
        return _normalize_level(str(value))

    @field_validator("years", mode="before")
    @classmethod
    def normalize_years(cls, value: object) -> Optional[float]:
        return _to_optional_float(value)


class RequiredSkill(BaseModel):
    model_config = {"extra": "ignore"}

    name: str
    level: Level = "beginner"
    priority: Priority = "nice-to-have"

    @field_validator("level", mode="before")
    @classmethod
    def normalize_level(cls, value: object) -> str:
        return _normalize_level(str(value))

    @field_validator("priority", mode="before")
    @classmethod
    def normalize_priority(cls, value: object) -> str:
        return _normalize_priority(str(value))


class EducationItem(BaseModel):
    model_config = {"extra": "ignore"}

    degree: str = "Unknown"
    field: Optional[str] = None
    institution: Optional[str] = None


class ResumeData(BaseModel):
    model_config = {"extra": "ignore"}

    skills: List[SkillEvidence] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    total_experience_years: float = 0

    @field_validator("total_experience_years", mode="before")
    @classmethod
    def normalize_total_years(cls, value: object) -> float:
        return _to_float(value, 0.0)


class JobDescriptionData(BaseModel):
    model_config = {"extra": "ignore"}

    required_skills: List[RequiredSkill] = Field(default_factory=list)
    role_title: str = "Unknown Role"
    role_category: str = "hybrid"

    @field_validator("role_category", mode="before")
    @classmethod
    def normalize_role_category(cls, value: object) -> str:
        normalized = str(value or "").strip().lower()
        if normalized in {"technical", "operational", "managerial", "hybrid"}:
            return normalized
        if "tech" in normalized or "engineer" in normalized:
            return "technical"
        if "operat" in normalized:
            return "operational"
        if "manag" in normalized or "lead" in normalized:
            return "managerial"
        return "hybrid"


class GapItem(BaseModel):
    skill: str
    current_level: Level
    required_level: Level
    gap_severity: Literal["critical", "moderate", "low"]
    priority: int


class GapAnalysisResult(BaseModel):
    gaps: List[GapItem] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    over_qualified: List[str] = Field(default_factory=list)
    gap_score: float = 0
    readiness_percentage: float = 0


class Course(BaseModel):
    id: str
    title: str
    category: str
    difficulty: Literal["beginner", "intermediate", "advanced"]
    duration_hours: int
    prerequisites: List[str] = Field(default_factory=list)
    skills_covered: List[str] = Field(default_factory=list)
    competency_level: str = "intermediate"
    description: str = ""


class WeekPlan(BaseModel):
    week: int
    courses: List[Course]
    skills_addressed: List[str]
    estimated_hours: int

    @field_validator("estimated_hours", mode="before")
    @classmethod
    def normalize_estimated_hours(cls, value: object) -> int:
        return int(_to_float(value, 0.0))


class PathwayResult(BaseModel):
    pathway: List[WeekPlan] = Field(default_factory=list)
    total_duration_hours: int = 0
    total_courses: int = 0
    reasoning_trace: List[str] = Field(default_factory=list)
    estimated_completion_weeks: int = 0

    @field_validator("total_duration_hours", "total_courses", "estimated_completion_weeks", mode="before")
    @classmethod
    def normalize_int_fields(cls, value: object) -> int:
        return int(_to_float(value, 0.0))


class GenerationPreferences(BaseModel):
    time_budget_hours: Optional[int] = None


class PathwayRequest(BaseModel):
    resume_data: ResumeData
    jd_data: JobDescriptionData
    preferences: GenerationPreferences = Field(default_factory=GenerationPreferences)


class AnalyzeResponse(BaseModel):
    status: Literal["success"]
    gap_analysis: GapAnalysisResult
    pathway: PathwayResult
    reasoning_trace: Dict[str, object]
