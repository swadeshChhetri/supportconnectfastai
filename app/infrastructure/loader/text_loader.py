# app/infrastructure/loader/text_loader.py
def load_text(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    return [
        {"text": text, "page": None}  # No pages in text
    ]

