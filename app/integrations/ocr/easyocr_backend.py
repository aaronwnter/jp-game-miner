from app.integrations.ocr.base import OCRBackend

class EasyOCRBackend(OCRBackend):
    def __init__(self) -> None:
        import easyocr

        # Create once and reuse
        # 'en' is used for punctuation, gpu=False -> only CPU
        self.reader = easyocr.Reader(["ja", "en"], gpu=False)

    def _extract_text(self, image_path: str) -> str:
        results = self.reader.readtext(image_path, detail=0)
        lines = [str(item) for item in results]
        return " ".join(lines).strip()
