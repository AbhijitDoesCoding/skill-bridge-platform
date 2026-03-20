from backend.core.skill_extractor import SkillExtractor


def test_rule_based_resume_extraction():
    extractor = SkillExtractor()
    payload = extractor.extract_from_resume(
        "Software Engineer with 5 years Python and 2 years AWS. Skills include machine learning."
    )
    names = {item["name"] for item in payload["skills"]}
    assert "Python" in names
    assert "Aws" in names


def test_normalization_maps_synonyms():
    extractor = SkillExtractor()
    normalized = extractor.normalize_skills(
        [{"name": "Py", "level": "advanced"}, {"name": "Python 3", "level": "beginner"}]
    )
    assert len(normalized) == 1
    assert normalized[0]["name"] == "Python"
