# Architecture

## Architecture goal

Keep the logic separated from the UI so the app stays maintainable and testable.

## High-level structure

```text
+----------------------+
|      PySide6 UI      |
+----------+-----------+
           |
           v
+----------------------+
|   Application Layer  |
|  review coordination |
+----------+-----------+
           |
           v
+----------------------+     +----------------------+
|    Core Services     | --> |     Local Storage    |
| OCR / tokenize /     |     | SQLite / files       |
| enrich / card build  |     +----------------------+
+----------+-----------+
           |
           v
+----------------------+
|   External Services  |
| AnkiConnect / OCR    |
| backend / dictionary |
+----------------------+
```

## Planned layers

### 1. UI layer

Responsible for:

- windows
- forms
- token click interactions
- card preview
- user actions

Suggested folder:

- `app/ui/`

### 2. Application layer

Responsible for:

- screen-to-service coordination
- command flow
- state transitions
- passing data between UI and services

Suggested folder:

- `app/application/`

### 3. Core services

Responsible for:

- OCR
- sentence cleanup
- tokenization
- dictionary lookup
- card building

Suggested folder:

- `app/core/`

### 4. Integrations

Responsible for:

- AnkiConnect
- OCR adapters
- optional dictionary providers

Suggested folder:

- `app/integrations/`

### 5. Persistence

Responsible for:

- local storage
- settings
- draft history
- screenshots
- queue state

Suggested folder:

- `app/storage/`

## Data flow

```text
screenshot
   ↓
OCR result
   ↓
cleaned sentence
   ↓
tokens
   ↓
selected token
   ↓
enriched entry
   ↓
card draft
   ↓
Anki note payload
```

## Current Anki export

The current app uses a small text-only AnkiConnect integration.

- `CardDraft` lives in `app/core/card.py`.
- AnkiConnect client code lives in `app/integrations/anki/`.
- The UI builds a card draft from editable enrichment fields.
- Required fields are validated before sending anything to Anki.
- The v1 deck is fixed to `Japanese Mining`.
- The v1 note type is fixed to `JP Vocab`.
- The v1 note fields are `Expression`, `Reading`, `Meaning`, `Sentence`, `Source`, and `Tags`.
- Screenshot/media export is intentionally not part of the current implementation.

## Design rules

1. UI should not contain business logic.
2. Every generated value should be editable by the user.
3. OCR and tokenization backends should be replaceable.
4. A failed external integration should not crash the app.
5. Storage should be local-first.

## MVP architecture note

The app now has real OCR, dictionary candidate lookup, card draft construction, and AnkiConnect export. Storage, settings, queue/history, and media export are still future layers.
