# game2anki

Turn moments from gameplay into high-quality Anki cards, with the learner staying in control of what gets learned.

This repository currently contains the **planning and product documentation** for the project. It is intentionally code-light at this stage and is focused on:

- product scope
- user flow
- desktop UX ideas
- architecture planning
- repository structure
- milestones
- contributor direction

## Project summary

The app helps a learner:

1. capture Japanese text from a game,
2. extract the text,
3. break it into tokens,
4. choose what matters,
5. review the card fields,
6. add the result to Anki.

The key principle is:
**human-in-the-loop card creation**

The tool should automate the boring parts without taking away the learning decision.

## Planned stack

- Python
- PySide6
- SQLite
- Pillow
- optional OCR / tokenizer integrations later
- AnkiConnect for Anki integration

## Current status

PySide6 Shell with placeholder/mock-data and no functionalities implemented.

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate # On Linux and Mac
.\.venv\Scripts\activate # On Windows (choose activate file type based on shell)
pip install -r requirements.txt
python -m app.main
```

## Docs index

- [`docs/vision.md`](docs/vision.md)
- [`docs/product-flow.md`](docs/product-flow.md)
- [`docs/gui-layout.md`](docs/gui-layout.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/repo-structure.md`](docs/repo-structure.md)
- [`docs/mvp-scope.md`](docs/mvp-scope.md)
- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/github-workflow.md`](docs/github-workflow.md)

## Notes

This repo is planned as a public repository aimed at learners who want to study Japanese through games like Pokémon, while keeping setup approachable and the workflow fast.

## License

This project is licensed under the GNU GPL v3.

You are free to use, modify, and distribute this software, as long as any distributed versions remain open-source under the same license.
