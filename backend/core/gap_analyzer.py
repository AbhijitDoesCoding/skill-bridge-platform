from __future__ import annotations

from typing import Dict, List


LEVEL_ORDER = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3}


class SkillGapAnalyzer:
    def analyze_gap(self, resume_skills: List[Dict], required_skills: List[Dict]) -> Dict:
        current_map = {item["name"]: item for item in resume_skills}
        gaps = []
        strengths = []
        over_qualified = []

        for req in required_skills:
            skill_name = req["name"]
            required_level = req.get("level", "beginner")
            required_n = self.level_to_numeric(required_level)

            if skill_name not in current_map:
                must_have = req.get("priority", "nice-to-have") == "must-have"
                gaps.append(
                    {
                        "skill": skill_name,
                        "current_level": "none",
                        "required_level": required_level,
                        "gap_severity": "critical" if must_have else "moderate",
                        "priority": 1 if must_have else 2,
                    }
                )
                continue

            current_level = current_map[skill_name].get("level", "beginner")
            current_n = self.level_to_numeric(current_level)
            if current_n < required_n:
                severity = "critical" if required_n - current_n >= 2 else "moderate"
                gaps.append(
                    {
                        "skill": skill_name,
                        "current_level": current_level,
                        "required_level": required_level,
                        "gap_severity": severity,
                        "priority": 1 if req.get("priority") == "must-have" else 2,
                    }
                )
            elif current_n == required_n:
                strengths.append(skill_name)
            else:
                over_qualified.append(skill_name)

        gaps.sort(key=lambda item: (item["priority"], self._severity_rank(item["gap_severity"])))

        return {
            "gaps": gaps,
            "strengths": sorted(strengths),
            "over_qualified": sorted(over_qualified),
            "gap_score": self.calculate_gap_score(gaps),
            "readiness_percentage": self.calculate_readiness(resume_skills, required_skills),
        }

    def level_to_numeric(self, level: str) -> int:
        return LEVEL_ORDER.get(level, 0)

    def calculate_gap_score(self, gaps: List[Dict]) -> float:
        if not gaps:
            return 0.0
        weight = {"critical": 1.0, "moderate": 0.6, "low": 0.3}
        total = sum(weight.get(item["gap_severity"], 0.5) for item in gaps)
        return round(total / len(gaps), 2)

    def calculate_readiness(self, resume_skills: List[Dict], required_skills: List[Dict]) -> float:
        if not required_skills:
            return 100.0
        current = {item["name"]: item for item in resume_skills}
        met = 0
        for req in required_skills:
            name = req["name"]
            if name in current and self.level_to_numeric(current[name].get("level", "none")) >= self.level_to_numeric(req.get("level", "beginner")):
                met += 1
        return round((met / len(required_skills)) * 100, 2)

    def _severity_rank(self, value: str) -> int:
        return {"critical": 0, "moderate": 1, "low": 2}.get(value, 1)
