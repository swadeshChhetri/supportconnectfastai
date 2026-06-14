import requests
import os
from app.core.config import settings
from app.core.logging import logger


def notify_node_status(document_id: str, step: str, status: str,
                       vector_count: int | None = None,
                       error: str | None = None):

    payload = {
        "documentId": document_id,
        "step": step,
        "status": status,
        "vectorCount": vector_count,
        "error": error
    }

    url = f"{settings.NODE_API_URL}/api/documents/internal/document-ingestion-status"

    try:
        res = requests.post(
            url,
            json=payload,
            timeout=15
        )
        if res.status_code != 200:
            logger.error(f"[{document_id}] Callback failed: {res.status_code} {res.text}")
    except Exception as e:
        logger.error(f"[{document_id}] Could not notify Node: {str(e)}")