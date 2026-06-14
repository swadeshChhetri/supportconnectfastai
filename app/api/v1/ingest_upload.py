from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import time, os

router = APIRouter()

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_FILE_SIZE_MB = 10

@router.post("/ingest/upload")
async def upload_document(
    orgId: str = Form(...),
    file: UploadFile = File(...)
):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    timestamp = int(time.time())
    file_name = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "documentId": f"doc_{timestamp}",
        "fileName": file.filename,
        "storagePath": file_path,
        "status": "uploaded"
    }

