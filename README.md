# AI Support Service

A FastAPI-based microservice that handles document parsing (PDF/DOCX), text chunking, embedding generation using SentenceTransformers, vector indexing/queries in Pinecone, and LLM answer generation using the Groq API.

## Features

- **Document Ingestion**: Extract pages from PDF/DOCX files, split text into semantic chunks, and upload to Pinecone.
- **RAG-based Q&A**: Perform vector similarity search on Pinecone indices to retrieve relevant contexts and generate answers using Groq's LLM (`llama-3.3-70b-versatile`).
- **S3 Integration**: Download documents directly from AWS S3 for parsing and chunking.
- **Tenant Isolation**: Multi-tenant support with tenant-isolated namespaces in Pinecone.

---

## Deployment & Packaging

To prepare the project for deployment and package only the necessary, non-credential parts, run the packaging utility:

```bash
python package_service.py
```

This creates a clean `deploy_package.zip` in the root folder, containing only the runtime code, requirements, configuration templates, and documentation. It automatically excludes:
- Sensitive credentials (`.env`)
- Virtual environments (`venv/`, `env/`, etc.)
- Temporary download directories (`tmp_downloads/`)
- User file uploads (`uploads/`)
- Local test/debug scripts (`test_pinecone_query.py`, `delete_index.py`, etc.)
- Python cache files (`__pycache__/`, `*.pyc`)

---

## Installation & Local Setup

1. **Extract/Clone the Project**:
   Ensure you have the clean files in your deployment workspace.

2. **Set Up Python Virtual Environment**:
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows (Command Prompt):
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables Configuration**:
   Copy the example environment file and fill in your actual credentials:
   ```bash
   # On macOS/Linux:
   cp .env.example .env
   # On Windows (Command Prompt):
   copy .env.example .env
   ```
   Modify `.env` with your correct API keys:
   - AWS S3 bucket details & credentials.
   - Groq API Key.
   - Pinecone API Key, environment, and index.

---

## Running in Production

To run the application in a production environment:

### Using Uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using a Process Manager (PM2):
If you use PM2 to manage processes, you can run the service with:
```bash
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name "ai-support-service"
```
