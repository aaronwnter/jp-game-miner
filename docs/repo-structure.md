# Repository Structure

## Current structure

```text
jp-game-miner/
├─ app/
│  ├─ core/
│  ├─ integrations/
│  │  └─ ocr/
│  ├─ ui/
│  ├─ __init__.py
│  └─ main.py
├─ docs/
├─ tests/
│  ├─ ocr_benchmark/
│  └─ test_text_normalizer.py
├─ .gitignore
├─ LICENSE
├─ README.md
└─ requirements.txt
```

## Folder intent

### `app/`

Main application code.

### `app/core/`

Pure app logic that should stay independent from the GUI where possible.

Current examples:

- OCR service
- text normalization

### `app/integrations/ocr/`

OCR backend implementations used by the app.

Current example:

- EasyOCR backend

### `app/ui/`

PySide6 window and interface code.

This layer should be responsible for:

- user interactions
- wiring buttons to app services
- updating the visible UI

It should avoid holding core business logic directly.

### `docs/`

Planning notes, roadmap, architecture, workflow notes, and OCR evaluation documentation.

### `tests/`

Automated tests and OCR benchmark code.

#### `tests/ocr_benchmark/`

Benchmark dataset, preprocessing, backend wrappers, and output files for OCR comparison work.

#### `tests/test_text_normalizer.py`

Unit tests for normalization rules used by the app.

## Structure principles

1. Keep benchmark code separate from app code.
2. Keep OCR backends behind small integration modules.
3. Keep core logic outside the UI when practical.
4. Add structure gradually instead of creating empty folders too early.

## Near-future expected additions

Likely next additions:

- tokenization service in `app/core/`
- tokenizer integration folder or module
- more unit tests for app logic
- settings/config handling once backend switching is added

## Notes

Earlier planning docs described a larger proposed structure with folders such as `application/`, `storage/`, `scripts/`, and `assets/`.

The current repo intentionally stays smaller and only adds structure once it is needed.
