# Repository Structure

## Current structure

```text
jp-game-miner/
├─ app/
│  ├─ core/
│  ├─ integrations/
│  │  ├─ anki/
│  │  ├─ dictionary/
│  │  └─ ocr/
│  ├─ ui/
│  ├─ __init__.py
│  └─ main.py
├─ docs/
├─ tests/
│  ├─ ocr_benchmark/
│  ├─ test_ankiconnect_client.py
│  ├─ test_card.py
│  ├─ test_jisho_client.py
│  ├─ test_text_normalizer.py
│  └─ test_tokenization.py
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
- card draft model
- tokenization service
- text normalization

### `app/integrations/anki/`

AnkiConnect integration used to add reviewed text-only notes to Anki.

Current example:

- AnkiConnect client

### `app/integrations/ocr/`

OCR backend implementations used by the app.

Current example:

- EasyOCR backend

### `app/integrations/dictionary/`

Dictionary lookup integrations used by token and kanji candidate workflows.

Current example:

- Jisho-style dictionary client

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

#### `tests/test_card.py`

Unit tests for card draft validation, tag parsing, and Anki field mapping.

#### `tests/test_ankiconnect_client.py`

Unit tests for AnkiConnect payload construction and error handling.

#### `tests/test_jisho_client.py`

Unit tests for dictionary candidate parsing and lookup failure handling.

#### `tests/test_tokenization.py`

Unit tests for reviewed sentence tokenization and dictionary candidate lookup.

## Structure principles

1. Keep benchmark code separate from app code.
2. Keep OCR backends behind small integration modules.
3. Keep core logic outside the UI when practical.
4. Add structure gradually instead of creating empty folders too early.

## Near-future expected additions

Likely next additions:

- settings/config handling once backend switching is added
- storage for drafts, history, and queue state
- media handling for screenshot export to Anki

## Notes

Earlier planning docs described a larger proposed structure with folders such as `application/`, `storage/`, `scripts/`, and `assets/`.

The current repo intentionally stays smaller and only adds structure once it is needed.
