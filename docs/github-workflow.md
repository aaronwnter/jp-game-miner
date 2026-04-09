# GitHub Workflow

## Repository style

Public, simple, beginner-friendly.

The repository should be easy to understand even for someone who just wants to follow the project or open their first issue.

## Branch strategy

Recommended:

- `main` for stable planning and working code
- short-lived feature branches for changes

Example branch names:

- `feature/pyside-shell`
- `feature/main-window-layout`
- `feature/mock-token-selection`
- `docs/repo-planning`
- `fix/readme-install-steps`

## Pull request style

Keep pull requests small and focused.

Good PR examples:

- add main window wireframe docs
- add repo structure docs
- add fake token selection screen
- add draft card model

Avoid PRs that change too many unrelated things at once.

## Issues

Suggested labels:

- `docs`
- `ui`
- `core`
- `anki`
- `ocr`
- `good first issue`
- `help wanted`
- `bug`
- `enhancement`

## Commit style

Simple and readable is enough.

Example format:

- `docs: add MVP scope`
- `ui: add main window shell`
- `core: add card draft model`
- `fix: handle missing screenshot path`

## Milestone suggestion

Milestone 1:

- planning docs complete

Milestone 2:

- PySide6 shell is usable

Milestone 3:

- local review loop works

Milestone 4:

- Anki integration works

## README expectations later

The README should eventually include:

- what the app does
- why it exists
- who it is for
- install steps
- screenshot or gif
- roadmap summary
- contribution notes

## Early project rule

Do not over-engineer the GitHub process before the app exists.

Use just enough process to stay clear and consistent.
