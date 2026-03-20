from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class UploadResponse(BaseModel):
    status: Literal["success"]
    data: dict
    raw_text: str
