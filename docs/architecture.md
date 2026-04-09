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

## Design rules

1. UI should not contain business logic.
2. Every generated value should be editable by the user.
3. OCR and tokenization backends should be replaceable.
4. A failed external integration should not crash the app.
5. Storage should be local-first.

## MVP architecture note

For early development, mocked OCR and mocked dictionary enrichment are acceptable so the user flow can be tested before harder integrations are added.
