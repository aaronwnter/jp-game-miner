# Repository Structure

## Goal

Keep the public repo understandable for users and contributors.

## Proposed structure

```text
game2anki/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ docs/
│  ├─ vision.md
│  ├─ product-flow.md
│  ├─ gui-layout.md
│  ├─ architecture.md
│  ├─ repo-structure.md
│  ├─ mvp-scope.md
│  ├─ roadmap.md
│  └─ github-workflow.md
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ ui/
│  ├─ application/
│  ├─ core/
│  ├─ integrations/
│  └─ storage/
├─ tests/
├─ scripts/
├─ assets/
│  ├─ screenshots/
│  └─ mock-data/
└─ requirements.txt
```

## Folder intent

### `docs/`

Planning, architecture, UX notes, repo process, milestones.

### `app/`

Main application code once implementation starts.

### `tests/`

Tests for pure logic and integration-safe behavior.

### `scripts/`

Helper scripts for local development.

### `assets/`

Example screenshots and demo resources for development.

## Public repo expectations

The repository should stay welcoming to people who are curious but not advanced developers.

That means:

- readable README
- simple run steps
- clear issue labels
- clear contributor notes
- minimal surprise in structure

## Early repo rule

Do not create too many top-level folders before they are needed.

The repo should feel small at the beginning.
