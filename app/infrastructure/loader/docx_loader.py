import docx
import re

def load_docx(path: str):
    doc = docx.Document(path)
    extracted = []
    current_section = None  # Track current section/title

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        style = para.style.name if para.style else ""

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        # Detect section headings (Heading 1, Heading 2, etc.)
        if style.startswith("Heading"):
            current_section = text.upper()  # store section title (uppercase for consistency)
            extracted.append({
                "text": text,
                "page": None,
                "section": current_section
            })
            continue

        # Detect bullet points (common Word styles)
        if "List Bullet" in style or "List Paragraph" in style:
            text = f"- {text}"

        # Detect numbered list (list numbering preserved)
        if "List Number" in style:
            text = f"1. {text}"

        # Append final structured output
        extracted.append({
            "text": text,
            "page": None,
            "section": current_section  # Apply current section (context)
        })

    return extracted


