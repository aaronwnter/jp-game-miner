from abc import ABC, abstractmethod

class OCRBackend(ABC):
    @abstractmethod
    def _extract_text(self, image_path: str) -> str:
        raise NotImplemented
