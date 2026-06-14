from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.ingest import IngestRequest
from app.services.ingestion_service import ingest_document
from app.core.logging import logger

router = APIRouter()

@router.post("/ingest/document")
def ingest_document_endpoint(payload: IngestRequest, bg: BackgroundTasks):
    try:
        # Run ingestion asynchronously in background
        bg.add_task(
            ingest_document,
            document_id=payload.documentId,
            file_key=payload.fileKey,
            org_id=payload.orgId,
            url=payload.url
        )

        # Return immediately
        return {
            "success": True,
            "status": "accepted"
        }

    except Exception as e:
        logger.error("🔥 INGESTION TRIGGER FAILED")
        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Ingestion trigger failed: {str(e)}"
        )