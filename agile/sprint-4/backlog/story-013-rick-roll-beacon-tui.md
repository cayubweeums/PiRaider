# [STORY-013] Rick Roll Beacon in TUI

## Summary

Add WiFi > Attacks > Rick Roll Beacon to the TUI: user can start and stop the attack; TUI shows status and optionally packet rate.

## Description

Same as story 012 but for the Rich TUI: expose Rick Roll Beacon under WiFi > Attacks so the terminal user can run the first tool from the TUI.

**Scope:**
- From the TUI home screen, provide navigation: **WiFi** → **Attacks** → **Rick Roll Beacon** (key or menu selection). Match Marauder menu location.
- On the Rick Roll screen: **Start** and **Stop** (key or option). When started, call the core transmission API with the selected interface; run until stopped.
- Display status (Idle / Running / Stopped) and, if available, packet count or rate. On error (e.g. no interface), show message and do not crash.
- Interface selection: same as Flet (first monitor-capable or simple list). No new core logic.

**ESP32 Marauder:** Same as story 012; TUI is the terminal counterpart.

## Acceptance criteria

- [ ] User can navigate from TUI home to WiFi > Attacks > Rick Roll Beacon.
- [ ] User can start and stop the Rick Roll Beacon; transmission uses core API.
- [ ] Status is shown; error from core is displayed.
- [ ] Optional: packet count or rate when available.
- [ ] No core logic in TUI; all transmission via core.

## Definition of done

- Code merged. Manual test: start/stop from TUI. No regressions. KISS: minimal TUI screens.

## Subtasks / notes

- Rich: use same pattern as home screen (e.g. menu options, key bindings). Run transmission in a thread so Stop can be handled.
