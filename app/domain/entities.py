# app/domain/entities.py
from dataclasses import dataclass
from typing import List


@dataclass
class DocumentChunks:
    document_id: str
    org_id: str
    chunks: List[str]
