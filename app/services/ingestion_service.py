# from app.core.logging import logger
# from app.infrastructure.s3_service import download_file_from_s3
# from app.infrastructure.loader.pdf_loader import load_pdf
# from app.infrastructure.loader.docx_loader import load_docx
# from app.infrastructure.loader.text_loader import load_text
# from app.utils.chunk_utils import chunk_pages
# from app.utils.semantic_grouper import group_resume_chunks
# from app.infrastructure.embedding_service import embed_texts
# from app.infrastructure.vector_store.pinecone_service import upsert_vectors
# from app.domain.entities import DocumentChunks
# from app.utils.file_utils import guess_file_type, extract_file_name
# from app.utils.text_cleaner import clean_text
# from app.infrastructure.node_usage_logger import log_usage_to_node


# def ingest_document(document_id: str, file_key: str, url: str, org_id: str) -> DocumentChunks:
#     local_path = download_file_from_s3(file_key)
#     file_type = guess_file_type(local_path)
#     file_name = extract_file_name(file_key)    # NEW: capture real filename

#     logger.info(f"Ingesting document={document_id}, org={org_id}, type={file_type}")

#     # Load structured text (page-aware)
#     if file_type == "pdf":
#         pages = load_pdf(local_path)   
#     elif file_type == "docx":
#         pages = load_docx(local_path)  
#     else:
#         pages = load_text(local_path)  

#     # Clean before chunking
#     for p in pages:
#         p["text"] = clean_text(p["text"])
#         p["source"] = file_name  

#     # grouped_entries = group_resume_chunks(pages)

#     # Split into real chunks with metadata
#     processed_chunks = chunk_pages(pages)  # << replaces chunk_text()

#     logger.info(f"Generated {len(processed_chunks)} structured chunks")

#     # Prepare embeddings
#     vectors = embed_texts([chunk["text"] for chunk in processed_chunks])

#     # Upsert with metadata
#     upsert_vectors(
#     chunks=processed_chunks,     # pass original chunk dicts
#     vectors=vectors,            # same length, same order
#     org_id=org_id,
#     document_id=document_id
#     )

#     # ✅ TODO: Log VECTOR_UPSERT back to Node
#     log_usage_to_node(
#         org_id=org_id,
#         usage_type="VECTOR_UPSERT",
#         count=len(processed_chunks),
#         meta={"documentId": document_id}
#     )

#     return DocumentChunks(
#         document_id=document_id,
#         org_id=org_id,
#         chunks=processed_chunks
#     )


from app.core.logging import logger
from app.infrastructure.s3_service import download_file_from_s3
from app.infrastructure.loader.pdf_loader import load_pdf
from app.infrastructure.loader.docx_loader import load_docx
from app.infrastructure.loader.text_loader import load_text
from app.utils.chunk_utils import chunk_pages
from app.infrastructure.embedding_service import embed_texts
from app.infrastructure.vector_store.pinecone_service import upsert_vectors
from app.domain.entities import DocumentChunks
from app.utils.file_utils import guess_file_type, extract_file_name
from app.utils.text_cleaner import clean_text
# from app.infrastructure.node_usage_logger import log_usage_to_node
from app.infrastructure.node_status_notifier import notify_node_status


def ingest_document(document_id: str, file_key: str, url: str, org_id: str) -> DocumentChunks:
    try:
        logger.info(f"[{document_id}] Starting ingestion")

        # ---------------- STEP 1: DOWNLOAD ----------------
        notify_node_status(document_id, "DOWNLOADING", "processing")
        local_path = download_file_from_s3(file_key)

        # ---------------- STEP 2: EXTRACT ----------------
        notify_node_status(document_id, "EXTRACTING", "processing")
        file_type = guess_file_type(local_path)
        file_name = extract_file_name(file_key)

        if file_type == "pdf":
            pages = load_pdf(local_path)
        elif file_type == "docx":
            pages = load_docx(local_path)
        else:
            pages = load_text(local_path)

        # ---------------- STEP 3: CLEAN + CHUNK ----------------
        notify_node_status(document_id, "CHUNKING", "processing")

        for p in pages:
            p["text"] = clean_text(p["text"])
            p["source"] = file_name

        processed_chunks = chunk_pages(pages)

        if not processed_chunks:
            raise ValueError("No chunks generated from document")

        logger.info(f"[{document_id}] Generated {len(processed_chunks)} chunks")

        # ---------------- STEP 4: EMBEDDING ----------------
        notify_node_status(document_id, "EMBEDDING", "processing")

        vectors = embed_texts([c["text"] for c in processed_chunks])

        if len(vectors) != len(processed_chunks):
            raise ValueError("Embedding count mismatch")

        # ---------------- STEP 5: UPSERT ----------------
        notify_node_status(document_id, "UPSERTING", "processing")

        upsert_vectors(
            chunks=processed_chunks,
            vectors=vectors,
            org_id=org_id,
            document_id=document_id
        )

        # ---------------- SUCCESS ----------------
        notify_node_status(
            document_id,
            "COMPLETED",
            "completed",
            vector_count=len(processed_chunks)
        )

        # log_usage_to_node(
        #     org_id=org_id,
        #     usage_type="VECTOR_UPSERT",
        #     count=len(processed_chunks),
        #     meta={"documentId": document_id}
        # )

        logger.info(f"[{document_id}] Ingestion completed")

        return DocumentChunks(
            document_id=document_id,
            org_id=org_id,
            chunks=processed_chunks
        )

    except Exception as e:
        logger.exception(f"[{document_id}] Ingestion failed")

        notify_node_status(
            document_id,
            "FAILED",
            "failed",
            error=str(e)
        )

        raise