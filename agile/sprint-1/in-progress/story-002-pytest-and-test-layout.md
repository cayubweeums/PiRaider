# [STORY-002] Pytest and test layout

## Summary

Add pytest as the test runner and a minimal test layout under `tests/` so that `poetry run pytest` is the single command to run the suite.

## Description

The PoC specifies pytest under `tests/`, with unit tests for logic that does not need hardware. This story adds pytest to the project and ensures one smoke test so the pipeline is in place for later stories (e.g. parsing, radio with mocked data).

**Scope:**
- Add `pytest` (and optionally `pytest-cov` if desired; not required for PoC) to dev-dependencies in `pyproject.toml`.
- Create `tests/` with at least one passing test (e.g. `test_smoke.py` with `def test_smoke(): assert True` or a trivial import test).
- Ensure `poetry run pytest` runs and passes.
- Document nowhere that tests are run via another command; the one way is `poetry run pytest`.

**ESP32 Marauder:** N/A — test infrastructure only.

## Acceptance criteria

- [x] `pytest` is a dev-dependency in `pyproject.toml`; `poetry install` installs it.
- [x] Directory `tests/` exists and is the canonical place for tests.
- [x] At least one test file exists (e.g. `tests/test_smoke.py`) and the test passes.
- [x] `poetry run pytest` executes and exits with success.
- [x] No duplicate or conflicting test runner (e.g. only pytest, not unittest as primary).
- [ ] Tests run in a workflow prior to merging to main and prevent a merge to main

## Definition of done

- Code merged. `poetry run pytest` passes. No regressions. KISS: minimal config.

## Subtasks / notes

- If the project uses a `src/` layout or package name, ensure `pyproject.toml` or `pytest` config allows discovery of the package under `core/` if tests import from it later; for this story, a single self-contained smoke test is enough.
