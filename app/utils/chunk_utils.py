from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Blocklist for section-only chunks
JUNK_SECTIONS = {
    "WORK EXPERIENCE", "EDUCATION", "OBJECTIVE", "SUMMARY",
    "SKILLS", "CONTACT", "ADDRESS", "LANGUAGES",
    "CERTIFICATIONS", "PROFILE", "EXPERIENCE",
    "DECLARATION", "PERSONAL DETAILS"
}

def chunk_pages(pages: List[Dict]) -> List[Dict]:
    """Improved structure-aware chunking with strict content filtering."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n", "\n- ", "\n• ", "\n### ", "\n## ", "\n# ",
            "\n", ". ", "? ", "! ", " ", ""
        ]
    )

    final_chunks = []

    for item in pages:
        text = item.get("text", "").strip()
        if not text:
            continue

        section = item.get("section") or "Unknown"
        page = item.get("page") if item.get("page") is not None else 0
        source = item.get("source") or "Unknown"

        chunks = splitter.split_text(text)

        for chunk_index, chunk in enumerate(chunks):
            cleaned_chunk = chunk.strip()

            # 🚫 Filter garbage & useless chunks
            if len(cleaned_chunk) < 40:
                  continue
            if cleaned_chunk.isupper() and len(cleaned_chunk.split()) <= 4:
                  continue
            if cleaned_chunk.strip().upper() in JUNK_SECTIONS:
                  continue

            deterministic_id = f"{page}_{chunk_index}"

            final_chunks.append({
                "chunk_id": deterministic_id,
                "text": cleaned_chunk,
                "page": page,
                "section": section,
                "source": source
            })

    return final_chunks
