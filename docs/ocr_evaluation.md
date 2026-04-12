# OCR Evaluation

## Evaluation goal

Find the best OCR option for local OCR and potential external (API call) OCR.

## Planned benchmark

```mermaid
flowchart TD

bm_data["Benchmark Data"]
lm1["MangaOCR"]
lm2["EasyOCR"]
lm3["TesseractOCR"]
em1["OCR.space"]
em1["Google Cloud Vision"]

bm_output["Output data"]

    subgraph Models
        direction LR
        lm1 --- lm2 --- lm3 --- em1 --- em2
    end

bm_data -->|for each| Models

Models -->|for each| bm_output
```

Manual evaluation with input vs expected output.

## Reports
