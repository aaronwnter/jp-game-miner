# MVP Scope

## MVP objective

Build the smallest version of the app that proves the core screenshot-to-study workflow is viable.

## Current MVP direction

The MVP is now defined by the workflow that already exists plus the next steps needed to make it useful for study.

Current implemented parts:

1. Open screenshot from file
2. Display screenshot in the desktop app
3. Run OCR using EasyOCR
4. Normalize OCR output for display
5. Let the user review and edit the sentence manually
6. Tokenize the reviewed sentence
7. Let the user select a token to learn
8. Prepare editable card fields
9. Preview the card from editable fields
10. Add a text-only note to Anki through AnkiConnect

## In scope for the MVP

- desktop app with PySide6
- local screenshot import
- screenshot preview
- local OCR with EasyOCR
- user-editable OCR sentence field
- text normalization before later tokenization
- tokenization and token selection
- structured card field preparation
- text-only AnkiConnect export
- human-in-the-loop review at every important step

## Explicitly out of scope for the MVP

- full automation
- automatic card creation without review
- mobile app
- cloud sync
- browser-first version
- multiple card generation from one sentence
- advanced grammar mining
- polished backend-switching settings UI
- global hotkeys
- automatic textbox detection
- full queue/history workflow
- advanced theming
- screenshot/media export to Anki
- configurable Anki deck, note type, or field mapping

## MVP quality bar

The MVP is good enough when:

- the screenshot-to-text workflow is stable,
- the user can correct OCR output easily,
- the reviewed sentence can move into token selection,
- the selected candidate can populate editable card fields,
- and the reviewed card can be sent to Anki as a text-only note.

## MVP user story

```text
As a learner playing a Japanese game,
I want to load a screenshot, extract and clean the text,
review it, choose what matters, and turn it into study material,
so that gameplay naturally becomes something I can learn from.
```

## MVP development order

1. desktop shell
2. screenshot loading and display
3. OCR backend evaluation
4. EasyOCR integration in the app
5. display-oriented normalization
6. tokenization
7. token selection
8. structured card preparation
9. text-only AnkiConnect export
