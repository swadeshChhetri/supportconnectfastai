import requests
from app.core.config import settings
from app.core.logging import logger

GROQ_API_KEY = settings.GROQ_API_KEY
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

def generate_llm_answer(question: str, context: str) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing in environment or config")

    prompt = f"""
    You are an AI assistant that extracts factual information from documents.

    Use ONLY the context provided. Do not guess or assume anything.
    

    Context:
    {context}

    Question: {question}

    Answer in 1-2 clear factual sentences:
    """

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a concise support assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "CustomerSupport-AI"
    }

    logger.info("Calling Groq LLM")

    try:
        resp = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Groq API error: {str(e)}", exc_info=True)
        raise RuntimeError(f"LLM generation failed: {str(e)}")
