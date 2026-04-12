from app.integrations.ocr.base import OCRBackend
from app.integrations.ocr.easyocr_backend import EasyOCRBackend

class OCRService:
    def __init__(self, backend: OCRBackend | None = None) -> None:
        self.backend = backend or EasyOCRBackend()

    def _extract_text(self, image_path: str) -> str:
        return self.backend._extract_text(image_path)
