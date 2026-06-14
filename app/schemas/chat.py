# app/schemas/chat.py
from pydantic import BaseModel
from typing import List, Optional


class AnswerSource(BaseModel):
    text: str
    documentId: str
    score: float


class AnswerRequest(BaseModel):
    orgId: str
    question: str
    topK: int = 5


class AnswerResponse(BaseModel):
    success: bool
    answer: str
    sources: List[AnswerSource]
