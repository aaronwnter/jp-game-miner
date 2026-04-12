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

### MangaOCR

Initial MangaOCR results on Pokémon-style Japanese game text show consistent partial recognition, but no exact matches across the first benchmark batch. Errors include kana substitution, punctuation hallucination, spacing collapse, and named-entity distortion. Current preprocessing does not consistently improve results. MangaOCR may still be useful as a human-assist OCR layer, but is not currently reliable enough for an automated pipeline.
