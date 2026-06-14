import re
import unicodedata

def clean_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""

    # Normalize Unicode (preserves accents, symbols, currencies, etc.)
    text = unicodedata.normalize("NFKC", text)

    # Replace fancy quotes, dashes, bullets with plain equivalents
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    text = text.replace("–", "-").replace("—", "-").replace("•", "\n- ")

    # Keep useful characters: letters, numbers, common punctuation
    text = re.sub(r"[^a-zA-Z0-9.,!?%:/\n\-\s()']", " ", text)

    # Fix glued words after PDF extraction (e.g., ManagerExperience → Manager Experience)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    # Fix missing space between numbers and words (e.g., 5years → 5 years)
    text = re.sub(r"(\d)([A-Za-z])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z])(\d)", r"\1 \2", text)

    # Preserve paragraph separations
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove extra spaces
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n\s+", "\n", text)

    return text.strip()


