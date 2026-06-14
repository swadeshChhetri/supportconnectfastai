from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Service"
    APP_ENV: str = "dev"

    # --- ADD THIS LINE HERE ---
    NODE_API_URL: str | None = None  # Using None makes it optional if missing

    # Hugging Face (for Serverless Embeddings)
    HF_TOKEN: str | None = None

    # AWS / S3
    AWS_REGION: str | None = None
    AWS_ACCESS_KEY: str | None = None
    AWS_SECRET_KEY: str | None = None
    S3_BUCKET: str | None = None

    # Groq (replacement for OpenAI)
    GROQ_API_KEY: str

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_ENV: str
    PINECONE_INDEX: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

