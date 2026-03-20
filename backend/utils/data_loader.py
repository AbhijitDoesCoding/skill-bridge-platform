from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "backend" / "data"


def load_json(file_name: str) -> Dict[str, Any]:
    with (DATA_DIR / file_name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_course_catalog() -> List[Dict[str, Any]]:
    payload = load_json("course_catalog.json")
    return payload.get("courses", [])


def load_skill_taxonomy() -> Dict[str, Any]:
    return load_json("skill_taxonomy.json")
