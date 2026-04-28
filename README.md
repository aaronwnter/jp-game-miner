# jp-game-miner

A desktop tool for turning Japanese game text into high-quality Anki cards while keeping the learner in control of what gets learned.

## What the project does

`jp-game-miner` is a Python desktop app for mining Japanese from games in a human-in-the-loop workflow.

Current flow:

1. Load a screenshot from a game
2. Display the screenshot in the desktop app
3. Run OCR on the screenshot
4. Normalize the extracted text for display
5. Review and edit the sentence manually
6. Tokenize the reviewed sentence
7. Select a token and choose a kanji candidate
8. Review editable enrichment/card fields
9. Preview the card
10. Send a text-only note to Anki through AnkiConnect

The project is built around one core idea:
**automation should support the learning decision, not replace it**

The app should handle repetitive steps like OCR and cleanup, while the learner stays in control of what is worth learning.

---

## Current status

The project is no longer planning-only.

### Implemented

- PySide6 desktop shell
- screenshot loading and display
- local OCR integration with EasyOCR
- OCR-to-text flow wired into the GUI
- OCR display normalization
- reviewed sentence tokenization
- Jisho-style kanji candidate lookup for selected kana tokens
- editable enrichment/card fields populated from the selected candidate
- live card preview based on editable fields
- text-only AnkiConnect export for a fixed v1 deck/note type
- normalization unit tests
- card model and Anki payload unit tests
- OCR benchmark suite with sample screenshots and backend comparisons

### OCR benchmark conclusion

The benchmark work currently supports this OCR strategy:

- **Primary local OCR:** EasyOCR
- **Primary external OCR:** Google Vision
- **Fallback external OCR:** OCR.space

### Not implemented yet

- backend switching in the GUI
- queue/history workflow
- configurable Anki deck, note type, or field mapping
- screenshot/media export to Anki
- Save Draft, Skip, Clear, Paste, Settings, and Help button behavior

---

## Repository structure

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

### Main folders

- `app/`
  Main application code for the desktop app

- `app/core/`
  Core application logic such as OCR service, text normalization, tokenization, and card drafts

- `app/integrations/anki/`
  AnkiConnect client used to add text-only notes to Anki

- `app/integrations/ocr/`
  OCR backend implementations used by the app

- `app/integrations/dictionary/`
  Dictionary lookup client used for kanji candidates

- `app/ui/`
  PySide6 window and UI logic

- `tests/ocr_benchmark/`
  OCR benchmark dataset, scripts, preprocessing, backend wrappers, and outputs

- `tests/test_text_normalizer.py`
  Unit tests for normalization behavior

- `tests/test_card.py`
  Unit tests for card draft validation, field mapping, and tag parsing

- `tests/test_ankiconnect_client.py`
  Unit tests for AnkiConnect payload construction and error handling

- `docs/`
  Planning, architecture, benchmark notes, and project workflow documentation

---

## Current OCR approach

The app currently uses **EasyOCR** as the local OCR backend.

This was chosen after benchmarking multiple OCR options on Pokémon-style Japanese game screenshots:

- MangaOCR
- EasyOCR
- Tesseract
- OCR.space
- Google Vision

At the moment, the GUI is wired only to the local EasyOCR path. External OCR support is planned for later.

---

## Running the app locally

### 1. Create and activate a virtual environment

#### Windows (PowerShell)

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows (cmd)

```bat
py -3.13 -m venv .venv
.\.venv\Scripts\activate.bat
```

#### Linux / macOS

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python -m app.main
```

### 4. Add notes to Anki

The `Add to Anki` button uses AnkiConnect at `http://127.0.0.1:8765`.

For the current v1 export, Anki must be running with the AnkiConnect add-on installed, and the target profile must contain:

- deck: `Japanese Mining`
- note type: `JP Vocab`
- fields: `Expression`, `Reading`, `Meaning`, `Sentence`, `Source`, `Tags`

Export is text-only for now. Screenshot/media export is planned for later.

---

## Running tests

If `pytest` is installed in your environment:

```bash
python -m pytest
```

---

## OCR benchmark

The OCR benchmark lives in:

```text
tests/ocr_benchmark/
```

It is used to compare OCR quality across different local and external OCR backends on real Japanese game screenshot samples.

The benchmark exists to answer questions like:

- which OCR backend works best on game text
- whether preprocessing helps
- which local OCR option is strongest
- which external OCR option is worth supporting

This benchmark directly informed the current OCR strategy.

---

## Project direction

The intended long-term workflow is:

```text
Screenshot
→ OCR
→ normalization
→ tokenization
→ learner selects useful token
→ card fields are prepared
→ note is added to Anki
```

The project is intentionally designed to avoid low-quality full automation by keeping the user in the review loop.

---

## Documentation

Project docs live in `docs/`.

Suggested reading order:

- [`docs/vision.md`](docs/vision.md)
- [`docs/product-flow.md`](docs/product-flow.md)
- [`docs/gui-layout.md`](docs/gui-layout.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/mvp-scope.md`](docs/mvp-scope.md)
- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/ocr_evaluation.md`](docs/ocr_evaluation.md)
- [`docs/github-workflow.md`](docs/github-workflow.md)

---

## License

This project is licensed under the GNU GPL v3.

You are free to use, modify, and distribute this software as long as distributed versions remain open-source under the same license.
