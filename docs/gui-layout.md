# GUI Layout Ideas

## Main screen goal

The main screen should support the entire review loop in one place.

The user should not have to jump through many pages or dialogs.

## Main window layout

```text
+----------------------------------------------------------------------------------+
| game2anki                                                      [Settings] [Help] |
+----------------------------------------------------------------------------------+
| [Open Screenshot] [Paste] [Re-run OCR] [Re-tokenize] [Save Draft]                |
+----------------------------------------------------------------------------------+
|                              |                                                   |
|   SCREENSHOT PANEL           |   OCR / SENTENCE PANEL                            |
|                              |                                                   |
|   +----------------------+   |   Sentence (editable):                            |
|   |                      |   |   +-------------------------------------------+   |
|   |     screenshot       |   |   | これから ぼうけんが はじまる！                |   |
|   |                      |   |   +-------------------------------------------+   |
|   |                      |   |                                                   |
|   |                      |   |   Token candidates:                               |
|   |                      |   |   [これから] [ぼうけん] [が] [はじまる]               |
|   +----------------------+   |                                                   |
|                              |   Selected token: ぼうけん                         |
|                              |                                                   |
+------------------------------+---------------------------------------------------+
| ENRICHMENT / CARD FIELDS                                                         |
|                                                                                  |
| Expression: [ 冒険                           ]   Reading: [ ぼうけん             ] |
| Meaning:    [ adventure                                                        ] |
| Source:     [ Pokemon                                                          ] |
| Tags:       [ pokemon, game-mining, vocab                                      ] |
|                                                                                  |
| Sentence:   [ これから ぼうけんが はじまる！                                       ] |
|                                                                                  |
+----------------------------------------------------------------------------------+
| CARD PREVIEW                                                                     |
| Front: 冒険                                                                       |
| Back: ぼうけん / adventure                                                        |
| Context: これから ぼうけんが はじまる！                                              |
| Source: Pokemon | Tags: pokemon, game-mining, vocab                                |
+----------------------------------------------------------------------------------+
| [Add to Anki] [Skip] [Clear]                                                     |
+----------------------------------------------------------------------------------+
```

## Layout principles

1. Screenshot and sentence should both be visible.
2. Token selection should be quick and obvious.
3. Card fields should always be editable.
4. Add-to-Anki should feel like the final confirmation step.
5. The screen should support keyboard-first use later.

## Secondary windows

### Settings window

This is planned UI. The current Anki export uses fixed v1 values instead of settings.

```text
+------------------------------------------------------+
| Settings                                             |
+------------------------------------------------------+
| Default deck:        [ Japanese Mining           ]   |
| Default note type:   [ JP Vocab                  ]   |
| Screenshot folder:   [ /data/screenshots         ]   |
| OCR backend:         [ mock / real backend       ]   |
| Source label preset: [ Pokemon                   ]   |
|                                                      |
| [Save]                                       [Close] |
+------------------------------------------------------+
```

### History / queue window

```text
+----------------------------------------------------------------------------------+
| Review Queue                                                                     |
+----------------------------------------------------------------------------------+
| ID     | Status      | Source   | Sentence Preview                    | Date     |
|--------+-------------+----------+-------------------------------------+----------|
| 001    | Captured    | Pokemon  | これから...                         | ...       |
| 002    | Drafted     | Pokemon  | きみは...                           | ...       |
| 003    | Added       | Pokemon  | どうぐを...                         | ...       |
+----------------------------------------------------------------------------------+
```

## MVP note

For the first version, only the main review screen is required. Anki export currently assumes deck `Japanese Mining`, note type `JP Vocab`, and fields `Expression`, `Reading`, `Meaning`, `Sentence`, `Source`, and `Tags`.
