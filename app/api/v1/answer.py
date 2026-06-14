from fastapi import APIRouter, HTTPException
from app.schemas.chat import AnswerRequest, AnswerResponse
from app.services.rag_pipeline import answer_question

router = APIRouter()


@router.post("/answer", response_model=AnswerResponse)
async def get_answer(payload: AnswerRequest):
    """
    RAG: Uses orgId for tenant vectors,
    and Groq for final response.
    """
    try:
        result = answer_question(
            org_id=payload.orgId,
            question=payload.question,
            top_k=payload.topK,
        )

        return AnswerResponse(
    success=True,
    answer=result.answer,
    sources=result.sources,
    sessionId=getattr(result, "sessionId", None)
)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG processing error: {str(e)}")


