# app/utils/file_utils.py
from pathlib import Path


def guess_file_type(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return "pdf"
    if ext in [".docx", ".doc"]:
        return "docx"
    return "text"


def extract_file_name(path: str) -> str:
    return Path(path).name
