from __future__ import annotations

import json
import re
from typing import Dict, List, Optional

from groq import Groq

from backend.utils.config import settings
from backend.utils.data_loader import load_skill_taxonomy


LEVEL_ORDER = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3}


class SkillExtractor:
    def __init__(self) -> None:
        self.taxonomy = load_skill_taxonomy()
        self.synonym_map = self._build_synonym_map()
        self.groq_client: Optional[Groq] = None

        if settings.groq_api_key:
            self.groq_client = Groq(api_key=settings.groq_api_key)

    def extract_from_resume(self, resume_text: str) -> Dict:
        prompt = self._resume_prompt(resume_text)
        result = self._extract_with_llm(prompt, kind="resume")
        if result is None:
            result = self._extract_resume_rule_based(resume_text)
        result["skills"] = self.normalize_skills(result.get("skills", []), key="name")
        return result

    def extract_from_job_description(self, jd_text: str) -> Dict:
        prompt = self._jd_prompt(jd_text)
        result = self._extract_with_llm(prompt, kind="jd")
        if result is None:
            result = self._extract_jd_rule_based(jd_text)
        result["required_skills"] = self.normalize_skills(result.get("required_skills", []), key="name")
        return result

    def _extract_with_llm(self, prompt: str, kind: str) -> Optional[Dict]:
        if self.groq_client is not None:
            try:
                response = self.groq_client.chat.completions.create(
                    model=settings.groq_model,
                    temperature=0,
                    response_format={"type": "json_object"},
                    messages=[
                        {
                            "role": "system",
                            "content": "Return only valid JSON matching the requested schema.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                )
                text = response.choices[0].message.content or ""
                return self._safe_json(text)
            except Exception:
                pass

        return None

    def normalize_skills(self, skills: List[Dict], key: str = "name") -> List[Dict]:
        normalized = []
        for skill in skills:
            label = str(skill.get(key, "")).strip()
            if not label:
                continue
            canonical = self.find_canonical_skill(label)
            item = dict(skill)
            item[key] = canonical
            item["level"] = self._normalize_level(str(item.get("level", "beginner")))
            normalized.append(item)
        deduped: Dict[str, Dict] = {}
        for item in normalized:
            existing = deduped.get(item[key])
            if not existing or LEVEL_ORDER[item["level"]] > LEVEL_ORDER[existing["level"]]:
                deduped[item[key]] = item
        return list(deduped.values())

    def find_canonical_skill(self, value: str) -> str:
        key = value.lower().strip()
        return self.synonym_map.get(key, value.strip().title())

    def _build_synonym_map(self) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        taxonomy = self.taxonomy.get("skill_taxonomy", {})
        for _, group in taxonomy.items():
            for canonical, synonyms in group.items():
                canonical_title = canonical.replace("_", " ").title()
                mapping[canonical.lower()] = canonical_title
                mapping[canonical_title.lower()] = canonical_title
                for synonym in synonyms:
                    mapping[str(synonym).lower()] = canonical_title
        return mapping

    def _extract_resume_rule_based(self, text: str) -> Dict:
        skills = self._extract_skills_from_text(text)
        years = self._extract_years(text)
        return {"skills": skills, "education": [], "total_experience_years": years}

    def _extract_jd_rule_based(self, text: str) -> Dict:
        skills = self._extract_skills_from_text(text, for_required=True)
        title = self._extract_role_title(text)
        category = "technical" if any(s["name"] in {"Python", "Java", "Aws", "Machine Learning"} for s in skills) else "hybrid"
        return {"required_skills": skills, "role_title": title, "role_category": category}

    def _extract_skills_from_text(self, text: str, for_required: bool = False) -> List[Dict]:
        lowered = text.lower()
        found = []
        for synonym, canonical in self.synonym_map.items():
            if re.search(rf"\b{re.escape(synonym)}\b", lowered):
                if for_required:
                    found.append({"name": canonical, "level": "intermediate", "priority": "must-have"})
                else:
                    found.append({"name": canonical, "level": "intermediate", "years": None})
        unique = {}
        for item in found:
            unique[item["name"]] = item
        return list(unique.values())

    def _extract_years(self, text: str) -> float:
        matches = re.findall(r"(\d+)\+?\s+years", text.lower())
        nums = [int(m) for m in matches]
        return float(max(nums)) if nums else 0.0

    def _extract_role_title(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return lines[0][:80] if lines else "Unknown Role"

    def _normalize_level(self, level: str) -> str:
        value = level.lower().strip()
        if value in LEVEL_ORDER:
            return value
        if "expert" in value or "advanced" in value:
            return "advanced"
        if "inter" in value or "proficient" in value:
            return "intermediate"
        if "basic" in value:
            return "beginner"
        return "beginner"

    def _safe_json(self, text: str) -> Optional[Dict]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            block = re.search(r"\{[\s\S]*\}", text)
            if not block:
                return None
            try:
                return json.loads(block.group(0))
            except json.JSONDecodeError:
                return None

    def _resume_prompt(self, resume_text: str) -> str:
        return (
            "Extract resume skills and experience. Return only JSON with keys: "
            "skills (name, level, years), education, total_experience_years.\n"
            f"Resume:\n{resume_text}"
        )

    def _jd_prompt(self, jd_text: str) -> str:
        return (
            "Extract job requirements. Return only JSON with keys: "
            "required_skills (name, level, priority), role_title, role_category.\n"
            f"Job description:\n{jd_text}"
        )
