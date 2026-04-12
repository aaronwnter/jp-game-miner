from abc import ABC, abstractmethod

class OCRBackend(ABC):
    name: str

    @abstractmethod
    def _extract_text(self, image_path: str) -> str:
        """Run OCR on an image and return extracted text"""
        raise NotImplementedError
