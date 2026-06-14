import re

def group_resume_chunks(page_chunks):
    grouped = []
    current_section = None
    current_entry = {}

    for item in page_chunks:
        text = item["text"].strip()
        section = item.get("section", None)

        # Track latest section (EXPERIENCE, EDUCATION, SKILLS)
        if section:
            current_section = section.upper()
            continue

        # Detect date ranges
        if re.search(r"\b(19|20)\d{2}\b.*\b(19|20)\d{2}\b", text):
            current_entry["dates"] = text
            current_entry["section"] = current_section
            continue

        # Detect company
        if any(keyword in text.lower() for keyword in ["hotel", "company", "technologies", "solutions", "services", "pvt", "ltd"]):
            current_entry["company"] = text
            continue

        # Detect bullet points (responsibilities, achievements)
        if text.startswith(("-", "•", "*")):
            current_entry.setdefault("bullet_points", []).append(text)
            continue

        # Detect job roles
        if any(job in text.lower() for job in ["manager", "supervisor", "executive", "engineer", "representative"]):
            current_entry["role"] = text
            continue

    if current_entry:
        grouped.append(current_entry)

    return grouped
