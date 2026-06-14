from sentence_transformers import SentenceTransformer
from typing import List
from app.core.logging import logger

# Load embedding model (Fast, accurate, free)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Embed list of texts for Pinecone storage.
    Used for document chunks.
    """
    if not texts:
        return []

    logger.info(f"Embedding {len(texts)} chunks")
    return model.encode(texts, convert_to_numpy=True).tolist()


def embed_query(query: str) -> List[float]:
    """
    Embed a single user query (str) into vector.
    Used when answering a question.
    """
    logger.info("Embedding user query for search")
    return model.encode([query], convert_to_numpy=True).tolist()[0]
