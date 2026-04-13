import re

def normalize_for_display(text: str) -> str:
    """
    Light normalization for OCR output before showing it in the editable UI.

    Goals:
        - keep text readable
        - remove OCR formatting noise
        - avoid agressive rewriting
    """

    if not text:
        return ""

    normalized = text

    # Normalize Windows/macOS line endings to \n

    normalized = normalized.replace("\r\n", "\n"). replace("\r", "\n")

    # Trim leading/trailing whitespace on each line
    lines = [line.strip() for line in normalized.split("\n")]

    # Drop fully empty lines
    lines = [line for line in lines if line]

    # Join lines into one readable sentence
    normalized = "".join(lines)

    # Remove spaces around common Japanese punctuation
    normalized = re.sub(r"\s*([、。！？])\s*", r"\1",  normalized)

    # Trim final outer whitespaces
    normalized = normalized.strip()

    return normalized
