# Product Flow

## Core flow

```text
[Gameplay]
    ↓
[User sees Japanese text]
    ↓
[User captures screenshot]
    ↓
[App loads screenshot]
    ↓
[OCR extracts raw text]
    ↓
[User reviews / fixes text]
    ↓
[Tokenizer splits sentence]
    ↓
[User selects token to learn]
    ↓
[App enriches token]
    ↓
[User edits card fields]
    ↓
[User approves card]
    ↓
[App sends note to Anki]
```

## Step-by-step

### 1. Capture

The user gets a screenshot from a game textbox.

Possible input methods later:

- import image from file
- paste image from clipboard
- hotkey capture

For MVP:

- import image from file

### 2. OCR

The app extracts Japanese text from the screenshot.

Output:

- raw text
- maybe confidence data later

Example:

```text
これから ぼうけんが はじまる！
```

### 3. Review OCR text

The user sees the OCR result in an editable text area.

Why this is required:

- OCR mistakes will happen
- games use stylized fonts
- learners need control over final text quality

### 4. Tokenization

The reviewed sentence is split into tokens.

Example:

```text
これから | ぼうけん | が | はじまる
```

### 5. Human selection

The user chooses the token that should become the focus of the card.

Example choice:

```text
ぼうけん
```

This is the most important product decision in the whole workflow.

### 6. Enrichment

The selected token is used to look up kanji candidates.

When the user chooses a candidate, the app fills editable card fields.

Current fields:

- expression
- reading
- meaning
- sentence
- source
- tags

Example:

```text
Expression: 冒険
Reading: ぼうけん
Meaning: adventure
Sentence: これから ぼうけんが はじまる！
Source: Pokemon
Tags: pokemon, game-mining, vocab
```

### 7. Card preview

The app previews the structured card from the editable enrichment fields.

Example:

```text
Front: 冒険
Back: ぼうけん / adventure
Context: これから ぼうけんが はじまる！
Source: Pokémon
Tags: pokemon, game-mining, vocab
```

### 8. Add to Anki

The user confirms the card.

The app validates required fields, then sends a text-only note to Anki through AnkiConnect.

Current Anki export target:

- deck: `Japanese Mining`
- note type: `JP Vocab`
- fields: `Expression`, `Reading`, `Meaning`, `Sentence`, `Source`, `Tags`

Screenshot/media export is not implemented yet.

## UX rule

The app should always keep the sentence and screenshot visible during review so the context is never lost.
