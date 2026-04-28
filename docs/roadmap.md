# Roadmap

## Current state

The project has moved beyond planning and now has a working desktop prototype with real OCR integration.

Implemented so far:

- PySide6 desktop shell
- screenshot loading and display
- EasyOCR integration in the GUI
- OCR display normalization
- reviewed sentence tokenization
- Jisho-style kanji candidate lookup
- editable enrichment/card fields
- live card preview
- text-only AnkiConnect export
- normalization unit tests
- card and AnkiConnect payload unit tests
- OCR benchmark suite with multiple local and external OCR backends

## Phase 0 - Planning and product definition

Goal:
Define the learning workflow, app shape, repository structure, and MVP boundaries.

Completed:

- project vision
- product flow
- GUI layout planning
- architecture notes
- repo structure planning
- MVP scope
- GitHub workflow notes

Status:

- complete

## Phase 1 - Desktop shell

Goal:
Create a runnable PySide6 desktop app with the planned review layout.

Completed:

- main window shell
- main UI sections
- placeholder review flow
- local app startup and repo structure

Status:

- complete

## Phase 2 - Screenshot input workflow

Goal:
Turn the shell into a real screenshot-based desktop tool.

Completed:

- open screenshot from file
- display selected screenshot in the UI
- screenshot scaling for the preview panel
- basic screenshot loading edge-case handling

Status:

- complete

## Phase 3 - OCR evaluation

Goal:
Find the best OCR strategy for Pokémon-style Japanese game text.

Completed:

- benchmark dataset structure
- raw vs preprocessed comparisons
- benchmark scripts and backend wrappers
- evaluation of MangaOCR
- evaluation of EasyOCR
- evaluation of Tesseract
- evaluation of OCR.space
- evaluation of Google Vision

Current conclusion:

- local OCR winner: EasyOCR
- external OCR winner: Google Vision
- external fallback: OCR.space

Status:

- complete

## Phase 4 - Local OCR integration

Goal:
Integrate the chosen local OCR backend into the desktop app.

Completed:

- EasyOCR backend in app code
- OCR service layer
- `Re-run OCR` button integration
- OCR text inserted into the editable sentence field
- basic OCR failure handling in the GUI

Status:

- complete

## Phase 5 - Text normalization

Goal:
Normalize OCR output into cleaner text for user review and later tokenization.

Completed:

- display-oriented OCR normalization
- tokenization-oriented normalization function
- normalization wired into the OCR flow
- test coverage for normalization rules

Status:

- complete

## Phase 6 - Tokenization

Goal:
Convert reviewed Japanese text into clickable token candidates.

Completed:

- tokenizer selection
- tokenization service
- token candidate UI
- user token selection
- Jisho-style kanji candidate lookup for selected kana tokens

Status:

- complete

## Phase 7 - Card workflow

Goal:
Turn selected text into structured Anki-ready card data.

Completed:

- expression / reading / meaning fields
- source tagging
- card preview refinement
- card draft model
- AnkiConnect payload construction
- text-only Anki export through `Add to Anki`
- validation before export
- clean UI error handling for AnkiConnect failures

Status:

- complete

Current limits:

- fixed deck: `Japanese Mining`
- fixed note type: `JP Vocab`
- no screenshot/media export
- no configurable Anki field mapping yet

## Phase 8 - OCR backend choice in UI

Goal:
Allow the user to choose between local and external OCR backends.

Planned deliverables:

- backend selection setting
- Google Vision support in app code
- OCR.space fallback support
- local vs external OCR preference handling

Status:

- future

## Notes

The project direction is now based on benchmark evidence rather than assumptions:

- EasyOCR is the chosen local OCR backend
- Google Vision is the strongest external OCR option tested
- OCR.space remains useful as a lighter external fallback
