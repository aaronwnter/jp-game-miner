from manga_ocr import MangaOcr

from tests.ocr_benchmark.backends.base import OCRBackend

class MangaOCRBackend(OCRBackend):
    name = "mangaocr"

    def __init__(self) -> None:
        self._ocr = MangaOcr()

    def _extract_text(self, image_path: str) -> str:
        text = self._ocr(image_path)
        return text.strip()
