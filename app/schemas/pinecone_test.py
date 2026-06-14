from pydantic import BaseModel
from typing import Optional

class PineconeTestRequest(BaseModel):
    orgId: str
    query: str
    documentId: Optional[str] = None
