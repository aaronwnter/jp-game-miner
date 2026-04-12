# OCR Benchmark

This folder contains benchmark scripts and sample data for comparing OCR backends on Japanese game screenshots.

## Current scope

- MangaOCR
- raw images
- one preprocessing recipe:
  - nearest-neighbor upscale
  - grayscale
  - threshold

## Run

```bash
python -m tests.ocr_benchmark.run_benchmark
```

## Output

Results are written to:

- `test/ocr_benchmark/outputs`
