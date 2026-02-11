# [STORY-006] Flet home screen

## Summary

Implement a simple Flet home screen that shows the same top-level buckets as Marauder (WiFi, Bluetooth, Device) as placeholders and displays radio status from core.

## Description

The PoC requires both UIs to show a simple home screen with the same top-level buckets as the Marauder project (WiFi, Bluetooth, Device) as placeholders, and to show "radios ready" or "not available" from the radio module. This story delivers the Flet side.

**Scope:**
- Flet app (under `ui/flet/`) shows a single home screen with three top-level buckets: **WiFi**, **Bluetooth**, **Device**. They can be buttons, list tiles, or text labels that look like menu buckets; no submenus or real actions yet (placeholders).
- Call `core.radio` (or equivalent) to get WiFi and BT status; display a clear "radios ready" or "not available" (or equivalent) on the home screen. Criteria for "ready": at least one WiFi interface with monitor capability and/or BT adapter up (define in agreement with story 004). If neither is available, show "not available".
- Layout and styling: minimal and readable; no extra frameworks. Follow Flet conventions used in the repo (or standard Flet patterns if this is the first Flet screen).
- Entrypoint remains `main.py`; default run still launches this Flet app.

**ESP32 Marauder:** Marauder UI has WiFi, Bluetooth, Device (and sometimes Bad USB) as top-level menu buckets; we match that structure for the port (WiFi, Bluetooth, Device only per PoC).

## Acceptance criteria

- [ ] Running `poetry run python main.py` opens the Flet app with a home screen.
- [ ] The home screen shows three top-level buckets: WiFi, Bluetooth, Device (as placeholders; no full submenus required).
- [ ] The home screen shows radio status: either "radios ready" or "not available" (or equivalent), derived from `core.radio` (or equivalent) and updated at load time.
- [ ] No crash if radio module returns empty or error; show "not available" or similar.
- [ ] No new dependencies beyond those already in the project.

## Definition of done

- Code merged. Flet app runs and shows buckets + radio status. Tests: covered by existing pytest if any UI tests are added; otherwise manual check is acceptable for this story. KISS: simplest layout that meets criteria.

## Subtasks / notes

- Radio status can be a single line of text (e.g. "Radios: ready" / "Radios: not available") or two lines for WiFi and BT separately; keep it simple.
