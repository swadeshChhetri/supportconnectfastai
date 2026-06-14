# app/infrastructure/loader/pdf_loader.py
import fitz  # PyMuPDF
import re

def load_pdf(path: str):
    pages = []
    doc = fitz.open(path)

    header_footer_keywords = ["confidential", "page", "copyright", "www.", "@"]

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4].strip()

            if not text or len(text) < 15:
                continue

            # Remove common noise (emails, URLs, headers, footers)
            if any(word.lower() in text.lower() for word in header_footer_keywords):
                continue

            # Normalize extra spaces
            text = re.sub(r"\s+", " ", text)

            # Detect headings (basic)
            if text.isupper() and len(text.split()) <= 6:
                section_title = text
            else:
                section_title = None

            pages.append({
                "text": text,
                "page": page_num,
                "section": section_title
            })

    return pages



