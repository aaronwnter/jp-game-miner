import base64
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from tests.ocr_benchmark.backends.base import OCRBackend

class GoogleVisionBackend(OCRBackend):
    name = "google_vision"

    def __init__(self) -> None:
        load_dotenv(Path(__file__).resolve().parents[1] / ".env")

        self.api_key = os.getenv("GOOGLE_VISION_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GOOGLE_VISION_API_KEY is not set in tests/ocr_benchmark/.env"
            )

        self.api_url = (
            "https://vision.googleapis.com/v1/images:annotate"
            f"?key={self.api_key}"
        )

    def _extract_text(self, image_path: str) -> str:
        image_bytes = Path(image_path).read_bytes()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        payload = {
            "requests": [
                {
                    "image": {"content": image_base64},
                    "features": [
                        {
                            "type": "DOCUMENT_TEXT_DETECTION",
                        }
                    ],
                }
            ]
        }

        response = requests.post(
            self.api_url,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()

        data = response.json()

        if "error" in data:
            raise RuntimeError(f"Google Vision API error: {data['error']}")

        responses = data.get("responses", [])
        if not responses:
            return ""

        first_response = responses[0]

        full_text = first_response.get("fullTextAnnotation", {}).get("text", "")
        if full_text:
            return full_text.strip()

        text_annotations = first_response.get("textAnnotations", [])
        if text_annotations:
            return str(text_annotations[0].get("description", "")).strip()

        return ""
