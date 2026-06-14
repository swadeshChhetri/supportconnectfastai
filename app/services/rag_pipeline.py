# app/services/rag_pipeline.py
from typing import List
from app.infrastructure.embedding_service import embed_query
from app.infrastructure.vector_store.pinecone_service import query_pinecone
from app.infrastructure.groq_service import generate_llm_answer
from app.schemas.chat import AnswerResponse, AnswerSource
from app.core.logging import logger
import re


def answer_question(org_id: str, question: str, history=None, top_k: int = 5) -> AnswerResponse:
    # 1) Embed query
    query_vector = embed_query(question)

    # 2) Retrieve from Pinecone
    matches = query_pinecone(query_vector, org_id=org_id, top_k=top_k)

    if not matches:
        logger.info("No matches from Pinecone")
        answer = generate_llm_answer(
            question,
            context="(No relevant documents were found for this organization.)",
        )
        return AnswerResponse(
            success=True,
            answer=answer,
            sources=[],
        )

    # 3) Build context from top chunks
    context_parts: List[str] = []
    sources: List[AnswerSource] = []

    for m in matches[:3]:
        meta = m.get("metadata") or {}
        text = meta.get("text", "")
        document_id = meta.get("documentId", "unknown")
        score = float(m.get("score") or 0.0)

        if text:
            context_parts.append(text)
            sources.append(
                AnswerSource(
                    text=text,
                    documentId=document_id,
                    score=score,
                )
            )

    # Limit context length a bit
    context = "\n\n---\n\n".join(context_parts[:3])

    # 4) Call LLM (Groq)
    answer = generate_llm_answer(question=question, context=context)

    return AnswerResponse(
        success=True,
        answer=answer,
        sources=sources,
    )


def extract_experience(text: str):
    experiences = re.findall(r"(\d+)\s*(year|month)", text.lower())
    total_months = 0
    for num, unit in experiences:
        total_months += int(num) * (12 if unit == "year" else 1)
    return total_months // 12, total_months % 12