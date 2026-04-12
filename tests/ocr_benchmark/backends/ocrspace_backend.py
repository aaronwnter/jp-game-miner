import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from tests.ocr_benchmark.backends.base import OCRBackend


class OCRSpaceBackend(OCRBackend):
    name = "ocrspace"

    def __init__(self) -> None:
        load_dotenv(Path(__file__).resolve().parents[1] / ".env")

        self.api_key = os.getenv("OCR_SPACE_API_KEY")
        if not self.api_key:
            raise ValueError("OCR_SPACE_API_KEY is not set in tests/ocr_benchmark/.env")

        self.api_url = "https://api.ocr.space/parse/image"

    def _extract_text(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            response = requests.post(
                self.api_url,
                files={"file": image_file},
                data={
                    "apikey": self.api_key,
                    "language": "jpn",
                    "isOverlayRequired": False,
                },
                timeout=60,
            )

        response.raise_for_status()
        data = response.json()

        if data.get("IsErroredOnProcessing"):
            error_messages = data.get("ErrorMessage") or data.get("ErrorDetails") or "Unknown OCR.space error"
            raise RuntimeError(f"OCR.space processing error: {error_messages}")

        parsed_results = data.get("ParsedResults", [])
        if not parsed_results:
            return ""

        extracted_text = "\n".join(
            result.get("ParsedText", "") for result in parsed_results
        )

        return extracted_text.strip()
