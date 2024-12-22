from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class FusionBrainError(Exception):
    def __init__(self, status: int, response_data: dict):
        self.status = status
        self.response_data = response_data


class Status(str, Enum):
    INITIAL = "INITIAL"
    DONE = "DONE"


class AIStyle(BaseModel):
    name: str
    title: str
    title_en: str = Field(alias="titleEn")
    image: str


class AIModel(BaseModel):
    id: int
    name: str
    version: float
    type: str


class GenerateResponse(BaseModel):
    status: Status
    uuid: str
    status_time: int


class StatusGenerationResponse(BaseModel):
    uuid: str
    status: Status
    images: list[str]
    error_description: Optional[str] = Field(None, alias="errorDescription")
    generation_time: int = Field(alias="generationTime")
    censored: bool
    