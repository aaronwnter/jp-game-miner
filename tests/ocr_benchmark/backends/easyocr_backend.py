from tests.ocr_benchmark.backends.base import OCRBackend

class EasyOCRBackend(OCRBackend):
    name = "easyocr"

    def __init__(self) -> None:
        import easyocr # local import (important!)

        # Japanese + English (should help with symbols and numbers)
        self.reader = easyocr.Reader(["ja", "en"])

    def _extract_text(self, image_path: str) -> str:
        results = self.reader.readtext(image_path, detail=0)

        # results = list of strings -> join into one text
        text = "\n".join(str(item) for item in results)

        return text.strip()
