from __future__ import annotations

from typing import Dict, List, Set

import networkx as nx


LEVEL_ORDER = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3}


class AdaptivePathwayGenerator:
    def __init__(self, course_catalog: List[Dict]) -> None:
        self.catalog = course_catalog
        self.catalog_map = {course["id"]: course for course in course_catalog}
        self.course_graph = self.build_course_graph()

    def build_course_graph(self) -> nx.DiGraph:
        graph = nx.DiGraph()
        for course in self.catalog:
            graph.add_node(course["id"], **course)
        for course in self.catalog:
            for prereq in course.get("prerequisites", []):
                if prereq in self.catalog_map:
                    graph.add_edge(prereq, course["id"])
        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError("Course catalog contains cyclic prerequisites")
        return graph

    def generate_pathway(self, skill_gaps: List[Dict], current_skills: List[Dict], time_budget_hours: int | None = None) -> Dict:
        gap_courses = self.map_gaps_to_courses(skill_gaps)
        required_courses = self.resolve_prerequisites(gap_courses, current_skills)
        ordered = self.topological_sort_courses(required_courses)
        pathway = self.optimize_pathway(ordered, skill_gaps, time_budget_hours)
        reasoning = self.generate_reasoning_trace(skill_gaps, gap_courses, required_courses, pathway)

        total_duration = sum(week["estimated_hours"] for week in pathway)
        total_courses = sum(len(week["courses"]) for week in pathway)
        return {
            "pathway": pathway,
            "total_duration_hours": total_duration,
            "total_courses": total_courses,
            "reasoning_trace": reasoning,
            "estimated_completion_weeks": len(pathway),
        }

    def map_gaps_to_courses(self, skill_gaps: List[Dict]) -> List[str]:
        selected: List[str] = []
        for gap in skill_gaps:
            skill = gap["skill"]
            required_level = gap.get("required_level", "beginner")
            candidates = [
                course
                for course in self.catalog
                if skill in course.get("skills_covered", []) and self._is_appropriate_level(required_level, course.get("difficulty", "beginner"))
            ]
            if not candidates:
                continue
            best = sorted(candidates, key=lambda c: (self._difficulty_rank(c["difficulty"]), c["duration_hours"]))[0]
            if best["id"] not in selected:
                selected.append(best["id"])
        return selected

    def resolve_prerequisites(self, course_ids: List[str], current_skills: List[Dict]) -> List[str]:
        all_required: Set[str] = set(course_ids)
        for course_id in course_ids:
            for prereq in nx.ancestors(self.course_graph, course_id):
                if not self.has_prerequisite_skills(prereq, current_skills):
                    all_required.add(prereq)
        return list(all_required)

    def topological_sort_courses(self, course_ids: List[str]) -> List[str]:
        if not course_ids:
            return []
        subgraph = self.course_graph.subgraph(course_ids).copy()
        return list(nx.topological_sort(subgraph))

    def optimize_pathway(self, ordered_courses: List[str], skill_gaps: List[Dict], time_budget_hours: int | None) -> List[Dict]:
        if not ordered_courses:
            return []
        gap_priority = {item["skill"]: item.get("priority", 3) for item in skill_gaps}
        remaining = ordered_courses.copy()
        completed: Set[str] = set()
        week = 1
        pathway = []
        consumed_hours = 0

        while remaining:
            available = [c for c in remaining if all(p in completed for p in self.course_graph.predecessors(c))]
            if not available:
                break
            available.sort(key=lambda c: self._course_priority_score(c, gap_priority))

            week_courses = []
            for course_id in available:
                if len(week_courses) >= 2:
                    break
                course = self.catalog_map[course_id]
                next_total = consumed_hours + course["duration_hours"]
                if time_budget_hours is not None and next_total > time_budget_hours:
                    continue
                week_courses.append(course_id)

            if not week_courses:
                break

            payload_courses = [self.catalog_map[cid] for cid in week_courses]
            estimated = sum(c["duration_hours"] for c in payload_courses)
            consumed_hours += estimated
            pathway.append(
                {
                    "week": week,
                    "courses": payload_courses,
                    "skills_addressed": sorted({s for c in payload_courses for s in c.get("skills_covered", [])}),
                    "estimated_hours": estimated,
                }
            )

            for cid in week_courses:
                remaining.remove(cid)
                completed.add(cid)
            week += 1

        return pathway

    def generate_reasoning_trace(self, skill_gaps: List[Dict], gap_courses: List[str], required_courses: List[str], pathway: List[Dict]) -> List[str]:
        trace = [f"Identified {len(skill_gaps)} skill gaps"]
        if gap_courses:
            trace.append(f"Mapped gaps to core courses: {', '.join(gap_courses)}")
        prereq_count = max(0, len(required_courses) - len(gap_courses))
        if prereq_count:
            trace.append(f"Added {prereq_count} prerequisite courses")
        trace.append(f"Built a {len(pathway)}-week learning plan")
        for week in pathway:
            titles = ", ".join(course["title"] for course in week["courses"])
            trace.append(f"Week {week['week']}: {titles} ({week['estimated_hours']}h)")
        return trace

    def has_prerequisite_skills(self, course_id: str, current_skills: List[Dict]) -> bool:
        course = self.catalog_map.get(course_id)
        if not course:
            return True
        current = {item["name"] for item in current_skills}
        required = set(course.get("skills_covered", []))
        return bool(required and required.intersection(current))

    def _difficulty_rank(self, difficulty: str) -> int:
        return {"beginner": 1, "intermediate": 2, "advanced": 3}.get(difficulty, 2)

    def _is_appropriate_level(self, required_level: str, difficulty: str) -> bool:
        return self._difficulty_rank(difficulty) <= LEVEL_ORDER.get(required_level, 2) + 1

    def _course_priority_score(self, course_id: str, gap_priority: Dict[str, int]) -> tuple[int, int]:
        course = self.catalog_map[course_id]
        priorities = [gap_priority.get(skill, 3) for skill in course.get("skills_covered", [])]
        top = min(priorities) if priorities else 3
        return (top, course["duration_hours"])
