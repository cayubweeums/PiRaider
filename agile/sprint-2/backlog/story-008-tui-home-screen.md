# [STORY-008] TUI home screen

## Summary

Implement a simple TUI home screen that shows the same top-level buckets (WiFi, Bluetooth, Device) as placeholders and displays radio status from core.

## Description

The PoC requires both UIs to show a simple home screen with the same top-level buckets as Marauder (WiFi, Bluetooth, Device) and "radios ready" or "not available". This story delivers the TUI (Rich) side.

**Scope:**
- TUI (under `ui/tui/`) shows a home screen with three top-level buckets: **WiFi**, **Bluetooth**, **Device**. Use Rich for layout (e.g. panel, table, or simple print of menu items). Placeholders only; no submenus or real actions yet.
- Call `core.radio` to get WiFi and BT status; display "radios ready" or "not available" (same meaning as in story 006). If radio module returns empty or error, show "not available".
- Entrypoint: `poetry run python main.py --tui` launches this TUI.
- No Flet code in TUI; no extra dependencies beyond Rich (already in project).

**ESP32 Marauder:** Same menu structure as in story 006; TUI is the terminal counterpart to the Flet home.

## Acceptance criteria

- [ ] Running `poetry run python main.py --tui` opens the TUI and shows the home screen.
- [ ] The home screen shows three top-level buckets: WiFi, Bluetooth, Device (placeholders).
- [ ] The home screen shows radio status: "radios ready" or "not available", derived from `core.radio`.
- [ ] No crash if radio module returns empty or error; show "not available".
- [ ] No new dependencies; use Rich only.

## Definition of done

- Code merged. TUI runs and shows buckets + radio status. KISS: simplest Rich layout that meets criteria.

## Subtasks / notes

- Rich: `Console`, `Panel`, or `Table` for the menu; single status line is enough for radio.
