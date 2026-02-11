# [STORY-005] Radio module unit tests

## Summary

Add unit tests for the core radio module using mocked or fake data so that radio detection logic is testable without hardware.

## Description

The PoC requires unit tests for logic that does not need hardware—e.g. radio detection with mocked/fake data. This story adds tests for `core/radio.py`: parsing of command output (e.g. `iw` list, `hciconfig`) and the public API returning expected structures when given fake subprocess output or mocked functions.

**Scope:**
- Tests live in `tests/` (e.g. `tests/test_radio.py` or under `tests/core/`).
- Cover at least: (1) parsing of sample `iw` (or equivalent) output and correct derivation of interface list / monitor capability / bands; (2) parsing of sample Bluetooth tool output and correct derivation of adapter status; (3) behavior when tools are missing or return empty/error (safe "not available" or empty result).
- Use mocks (e.g. `unittest.mock.patch` for `subprocess.run` or helper that returns raw output) or fixture files with real-looking output. No dependency on real WiFi/BT hardware for CI.
- All tests pass with `poetry run pytest`.

**ESP32 Marauder:** N/A — tests only.

## Acceptance criteria

- [ ] There is a test file that imports and tests `core.radio` (or the radio module).
- [ ] WiFi path: at least one test provides fake/mocked output from a WiFi detection command and asserts the returned structure (e.g. interface name, monitor_capable, bands) is correct.
- [ ] BT path: at least one test provides fake/mocked Bluetooth output and asserts the returned status is correct.
- [ ] At least one test covers "tools missing or error" and asserts no unhandled exception and a safe return value.
- [ ] `poetry run pytest` passes including these tests.

## Definition of done

- Code merged. All new tests pass. No regressions. KISS: minimal test code, no unnecessary abstraction.

## Subtasks / notes

- Fixtures: short snippets of `iw dev` / `iw list` (or equivalent) and `hciconfig` or `bluetoothctl show` in the test file as strings are fine; no need for external files unless the team prefers them.
