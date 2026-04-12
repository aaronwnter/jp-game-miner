import pytesseract

from tests.ocr_benchmark.backends.base import OCRBackend


class TesseractBackend(OCRBackend):
    name = "tesseract"

    def __init__(self) -> None:
        # Optional fallback if PATH ever fails on Windows:
        # pytesseract.pytesseract.tesseract_cmd = (
        #     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # )
        pass

    def _extract_text(self, image_path: str) -> str:
        text = pytesseract.image_to_string(
            image_path,
            lang="jpn",
            config="--psm 6"
        )
        return text.strip()
