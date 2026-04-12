import json
from pathlib import Path

from tests.ocr_benchmark.backends.mangaocr_backend import MangaOCRBackend
from tests.ocr_benchmark.backends.ocrspace_backend import OCRSpaceBackend
from tests.ocr_benchmark.backends.easyocr_backend import EasyOCRBackend
from tests.ocr_benchmark.backends.google_vision_backend import GoogleVisionBackend
from tests.ocr_benchmark.preprocess import preprocess_image

BASE_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = BASE_DIR / "samples"
OUTPUTS_DIR = BASE_DIR / "outputs"
MANIFEST_PATH = BASE_DIR / "manifest.json"

def load_manifest() -> list[dict]:
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def run() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    backend = GoogleVisionBackend() # Change OCR model here
    manifest = load_manifest()

    results = []

    for sample in manifest:
        sample_id = sample["id"]
        file_name = sample["file_name"]
        expected_text = sample["expected_text"]

        image_path = SAMPLES_DIR / file_name
        preprocessed_path = OUTPUTS_DIR / f"{sample_id}_preprocessed.png"

        raw_text = backend._extract_text(str(image_path))

        preprocess_image(
            image_path=str(image_path),
            output_path=str(preprocessed_path),
            scale_factor=4,
        )
        preprocessed_text = backend._extract_text(str(preprocessed_path))

        results.append(
            {
                "sample_id": sample_id,
                "file_name": file_name,
                "expected_text": expected_text,
                "backend": backend.name,
                "raw_text": raw_text,
                "preprocessed_text": preprocessed_text,
                "raw_exact_match": raw_text == expected_text,
                "preprocessed_exact_match": preprocessed_text == expected_text,
            }
        )

        print(f"[{sample_id}] done.")

    output_file = OUTPUTS_DIR / "google_vision_result.json" #change to OCR ran in test
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Saved results to: {output_file}")

if __name__ == "__main__":
    run()
