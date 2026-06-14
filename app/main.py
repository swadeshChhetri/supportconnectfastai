# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.api.v1 import ingest as ingest_router
from app.api.v1.ingest import router as ingest_router
from app.api.v1 import ingest_upload as ingest_upload_router
from app.api.v1 import health as health_router
from app.api.v1 import answer as answer_router
from app.api.v1.pinecone_debug import router as pinecone_debug_router
from app.core.logging import logger


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
    )

    # Routers
    app.include_router(health_router.router, prefix="/v1", tags=["health"])
    app.include_router(ingest_upload_router.router, prefix="/v1", tags=["upload"])
    app.include_router(ingest_router, prefix="/v1", tags=["ingest"])
    app.include_router(answer_router.router, prefix="/v1", tags=["answer"])
    app.include_router(pinecone_debug_router, prefix="/v1", tags=["debug"])

    # Exceptions
    register_exception_handlers(app)

    logger.info("AI Service started.")
    return app


app = create_app()

