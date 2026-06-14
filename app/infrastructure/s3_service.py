# app/infrastructure/s3_service.py
import os
from pathlib import Path
import boto3
from app.core.config import settings
from app.core.logging import logger

s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
)

BUCKET = settings.S3_BUCKET

TMP_DIR = "tmp_downloads"
os.makedirs(TMP_DIR, exist_ok=True)


def download_file_from_s3(file_key: str) -> str:
    """
    Download a file from S3 to a temporary local directory and return the local path.
    """

    filename = file_key.replace("/", "_")   # Avoid nested folders locally
    local_path = os.path.join(TMP_DIR, filename)

    logger.info(f"Downloading from S3 → bucket={BUCKET}, key={file_key}, local={local_path}")

    try:
        s3_client.download_file(BUCKET, file_key, local_path)
        return local_path

    except Exception as e:
        logger.error(f"S3 download failed for key={file_key}: {str(e)}")
        raise FileNotFoundError(f"S3 download failed. Key not found or access denied: {file_key}")
