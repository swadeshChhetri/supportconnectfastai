import httpx
from typing import List
from app.core.config import settings
from app.core.logging import logger

# Hugging Face serverless feature extraction endpoint for the exact all-MiniLM-L6-v2 model (384 dimensions)
HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
HF_TOKEN = settings.HF_TOKEN

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Embed list of texts via Hugging Face API for Pinecone storage.
    """
    if not texts:
        return []

    logger.info(f"Embedding {len(texts)} chunks via Hugging Face API")
    
    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    try:
        with httpx.Client() as client:
            response = client.post(
                HF_API_URL,
                headers=headers,
                json={"inputs": texts, "options": {"wait_for_model": True}},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()  # Returns List[List[float]]
            
    except Exception as e:
        logger.error(f"Hugging Face embedding failed: {str(e)}")
        raise RuntimeError(f"Embedding service unavailable: {str(e)}")


def embed_query(query: str) -> List[float]:
    """
    Embed a single user query into a 384-dimensional vector.
    """
    logger.info("Embedding user query via Hugging Face API")
    embeddings = embed_texts([query])
    return embeddings[0]
