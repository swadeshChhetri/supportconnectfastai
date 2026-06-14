from fastapi import APIRouter, HTTPException
from app.infrastructure.vector_store.pinecone_service import query_pinecone
from app.infrastructure.embedding_service import embed_query
from app.schemas.pinecone_test import PineconeTestRequest

router = APIRouter()

@router.post("/pinecone/test")
def test_pinecone_search(payload: PineconeTestRequest):
    try:
        query_vector = embed_query(payload.query)

        results = query_pinecone(
            query_vector=query_vector,
            org_id=payload.orgId,
            top_k=5,
            document_id=payload.documentId
        )

        return {
            "query": payload.query,
            "results": [
               {
                   "score": match.score,
                   "chunkId": (match.metadata or {}).get("chunkId", "Unknown"),
                   "section": (match.metadata or {}).get("section", "Unknown"),
                   "page": (match.metadata or {}).get("page", 0),
                   "source": (match.metadata or {}).get("source", "Unknown"),
                   "documentId": (match.metadata or {}).get("documentId", "Unknown"),
                   "text": ((match.metadata or {}).get("text") or "")[:200]
               }
               for match in results
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

