from backend.core.pathway_generator import AdaptivePathwayGenerator


CATALOG = [
    {
        "id": "A",
        "title": "A",
        "category": "X",
        "difficulty": "beginner",
        "duration_hours": 10,
        "prerequisites": [],
        "skills_covered": ["Python"],
        "competency_level": "beginner",
        "description": "",
    },
    {
        "id": "B",
        "title": "B",
        "category": "X",
        "difficulty": "intermediate",
        "duration_hours": 10,
        "prerequisites": ["A"],
        "skills_covered": ["Machine Learning"],
        "competency_level": "intermediate",
        "description": "",
    },
]


def test_pathway_respects_prerequisites():
    generator = AdaptivePathwayGenerator(CATALOG)
    gaps = [{"skill": "Machine Learning", "required_level": "intermediate", "priority": 1}]
    pathway = generator.generate_pathway(gaps, current_skills=[])
    week_courses = [course["id"] for week in pathway["pathway"] for course in week["courses"]]
    assert week_courses.index("A") < week_courses.index("B")
