# MVP Scope

## MVP objective

Build the smallest version that proves the core learning loop works.

## In scope

1. Open screenshot from file
2. Display screenshot in the app
3. Show OCR text in an editable field
4. Tokenize reviewed sentence
5. Let the user select a token
6. Let the user edit expression, reading, and meaning
7. Preview a simple card
8. Send the card to Anki or prepare the payload for that step
9. Save basic local draft/history data

## Out of scope

- global hotkeys
- automatic textbox detection
- multiple cards from one line
- pitch accent
- cloud sync
- user accounts
- fancy theme system
- grammar mining mode
- advanced duplicate review interface
- mobile app
- browser version
- plugin ecosystem

## MVP quality bar

The MVP is good enough if:

- the workflow feels understandable,
- the user stays in control,
- the app is stable for repeated manual use,
- and setup is not painful.

## MVP user story

```text
As a learner playing a Japanese game,
I want to load a screenshot, review the extracted sentence,
select the word I care about, and make an Anki card from it,
so that gameplay naturally becomes study material.
```

## MVP development order

1. Desktop shell with fake data
2. Screenshot loading
3. Editable sentence field
4. Token selection
5. Card field editing
6. Card preview
7. Anki integration
8. Real OCR integration
