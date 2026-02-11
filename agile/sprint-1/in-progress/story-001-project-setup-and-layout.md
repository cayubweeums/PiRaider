# [STORY-001] Project setup and layout

## Summary

Add Poetry, project layout, and a single `main.py` entrypoint that launches Flet by default or TUI via `--tui`. Establishes the repo structure required by the PoC (reference plan).

## Description

The PoC requires one entrypoint (`main.py`) and a clear layout: Flet under `ui/flet/`, TUI under `ui/tui/`, shared logic in `core/`. No app code exists yet; this story creates the minimal structure and wiring so that `poetry run python main.py` and `poetry run python main.py --tui` work (even if the UIs are stubs).

**Scope:**
- Add `pyproject.toml` with Poetry, Python 3.x, and dependencies: `flet`, `rich`. No extra deps for now.
- Add `main.py` at repo root: parse CLI (e.g. `argparse`); default → launch Flet app; `--tui` → launch TUI. Stub UIs are acceptable (e.g. a single window/screen that closes or shows "PiRaider").
- Create directories: `ui/flet/`, `ui/tui/`, `core/`, `tests/`. Leave `core/` empty or with `__init__.py` only.
- Flet app can live in `ui/flet/app.py` (or single module) and be invoked from `main.py`; TUI similarly in `ui/tui/` and invoked from `main.py`.
- No global pip install for project deps; all install via `poetry install`.

**ESP32 Marauder:** This is project scaffolding only; no direct port of upstream code. Layout aligns with the intended separation (UI vs core) described in the PoC.

## Acceptance criteria

- [x] `pyproject.toml` exists with Poetry config, Python version, and dependencies `flet` and `textual`.
- [x] `poetry install` runs successfully and creates a lockfile.
- [x] `main.py` exists at repo root and is the only script users run for the app.
- [x] `poetry run python main.py` starts the Flet app (window or web window opens; may be minimal).
- [x] `poetry run python main.py --tui` starts the TUI (terminal UI; may be minimal, e.g. single screen).
- [ ] Directories `ui/flet/`, `ui/tui/`, `core/`, `tests/` exist; `core` has no UI code.
- [ ] No project dependencies are installed via `pip install -r requirements.txt` or global pip for app deps.

## Definition of done

- Code merged (or equivalent). `poetry install` and both run commands work. No regressions. Follow KISS: minimal code to satisfy the criteria.

## Subtasks / notes

- Use `argparse` or similar; keep flag set small (e.g. `--tui` only for now).
- Flet: `ft.app(main)` or equivalent in `ui/flet/`; import and run from `main.py`.
- TUI: Rich `Console` or simple layout; import and run from `main.py`.
- Optional: `core/__init__.py` and `ui/flet/__init__.py`, `ui/tui/__init__.py` for clean imports.
