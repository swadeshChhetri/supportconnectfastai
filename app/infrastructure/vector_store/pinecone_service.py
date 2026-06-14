from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any
from app.core.config import settings
from app.core.logging import logger

# Initialize Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index_name = settings.PINECONE_INDEX

# Ensure index exists
if index_name not in pc.list_indexes().names():
    logger.info(f"Creating Pinecone index: {index_name}")
    pc.create_index(
        name=index_name,
        dimension=384,  # For MiniLM embedding model
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=settings.PINECONE_ENV
        )
    )

# Connect to index
index = pc.Index(index_name)


def upsert_vectors(
    chunks: List[Dict],         # each chunk has chunk_id, text, page, section, source
    vectors: List[List[float]], # embedded vectors, same order
    org_id: str,
    document_id: str
):
    """
    Insert vector embeddings into Pinecone.
    Each record must link vector + chunk metadata.
    """
    if not chunks or not vectors:
        logger.warning("No vectors or chunks to upsert.")
        return

    logger.info(f"Upserting {len(chunks)} chunks for document={document_id}")

    items = []
    for chunk, vector in zip(chunks, vectors):
        items.append({
            "id": f"{org_id}:{document_id}:{chunk['chunk_id']}",  # stable traceable ID
            "values": vector,
            "metadata": {
              "orgId": org_id,
              "documentId": document_id,
              "chunkId": chunk["chunk_id"],
              "text": chunk["text"],
              "section": chunk.get("section") or "Unknown",
              "page": chunk.get("page") or 0,
              "source": chunk.get("source") or "Unknown"
            }
        })

    try:
        response = index.upsert(
            vectors=items,
            namespace=org_id  # Ensures tenant isolation
        )
        logger.info(f"Pinecone upsert response: {response}")
        return response

    except Exception as e:
        logger.error(f"Pinecone Upsert FAILED: {str(e)}", exc_info=True)
        raise


def query_pinecone(
    query_vector: List[float],
    org_id: str,
    top_k: int = 5,
    document_id: str | None = None
) -> List[Dict[str, Any]]:
    """
    Query Pinecone using vector similarity.
    Enforces orgId isolation, optional document-level filtering.
    """

    logger.info(f"Querying Pinecone: orgId={org_id}, top_k={top_k}")

    filter_clause = {"documentId": document_id} if document_id else None

    res = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=org_id,
        filter=filter_clause,
    )

    return res.matches or []
