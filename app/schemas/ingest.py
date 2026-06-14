from pydantic import BaseModel

class IngestRequest(BaseModel):
    documentId: str
    fileKey: str   # storagePath from upload
    orgId: str
    url: str
