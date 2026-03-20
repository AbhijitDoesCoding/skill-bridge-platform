from __future__ import annotations

from typing import Dict, List


class ReasoningTraceGenerator:
    def generate_complete_trace(self, resume_data: Dict, jd_data: Dict, gap_analysis: Dict, pathway: Dict) -> Dict:
        return {
            "extraction_reasoning": self.explain_extraction(resume_data, jd_data),
            "gap_analysis_reasoning": self.explain_gap_analysis(gap_analysis),
            "pathway_reasoning": self.explain_pathway(pathway),
            "decision_tree": self.build_decision_tree(resume_data, jd_data, gap_analysis, pathway),
        }

    def explain_extraction(self, resume_data: Dict, jd_data: Dict) -> List[str]:
        return [
            f"Extracted {len(resume_data.get('skills', []))} skills from resume",
            f"Extracted {len(jd_data.get('required_skills', []))} required skills from job description",
        ]

    def explain_gap_analysis(self, gap_analysis: Dict) -> List[str]:
        return [
            f"Detected {len(gap_analysis.get('gaps', []))} gaps",
            f"Readiness score computed as {gap_analysis.get('readiness_percentage', 0)}%",
            "Prioritized must-have skills before nice-to-have skills",
        ]

    def explain_pathway(self, pathway: Dict) -> List[str]:
        return [
            f"Selected {pathway.get('total_courses', 0)} courses from grounded catalog",
            f"Organized courses into {pathway.get('estimated_completion_weeks', 0)} weekly blocks",
            "Kept prerequisite order valid via DAG topological sort",
        ]

    def build_decision_tree(self, resume_data: Dict, jd_data: Dict, gap_analysis: Dict, pathway: Dict) -> Dict:
        return {
            "inputs": {
                "resume_skills": len(resume_data.get("skills", [])),
                "required_skills": len(jd_data.get("required_skills", [])),
            },
            "analysis": {
                "gaps": len(gap_analysis.get("gaps", [])),
                "readiness_percentage": gap_analysis.get("readiness_percentage", 0),
            },
            "output": {
                "weeks": pathway.get("estimated_completion_weeks", 0),
                "courses": pathway.get("total_courses", 0),
            },
        }
