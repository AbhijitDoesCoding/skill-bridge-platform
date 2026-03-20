from backend.core.gap_analyzer import SkillGapAnalyzer


def test_gap_analysis_basics():
    analyzer = SkillGapAnalyzer()
    resume = [
        {"name": "Python", "level": "advanced"},
        {"name": "Aws", "level": "beginner"},
    ]
    required = [
        {"name": "Python", "level": "advanced", "priority": "must-have"},
        {"name": "Aws", "level": "intermediate", "priority": "must-have"},
        {"name": "Machine Learning", "level": "intermediate", "priority": "must-have"},
    ]

    result = analyzer.analyze_gap(resume, required)
    assert result["readiness_percentage"] < 100
    assert any(item["skill"] == "Machine Learning" for item in result["gaps"])
    assert any(item["skill"] == "Aws" for item in result["gaps"])
