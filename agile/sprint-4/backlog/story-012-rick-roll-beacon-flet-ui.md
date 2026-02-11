# [STORY-012] Rick Roll Beacon in Flet UI

## Summary

Add WiFi > Attacks > Rick Roll Beacon to the Flet app: user can start and stop the attack; UI shows status and optionally packet rate.

## Description

The first shipped tool is the Rick Roll Beacon. After core transmission is implemented (story 011), both UIs must expose it. This story adds the Flet flow: from the home screen, navigate to WiFi (or WiFi > Attacks) and choose "Rick Roll Beacon"; user can start and stop; status (and packet rate if available from core) is shown.

**Scope:**
- From the Flet home screen, provide a path: **WiFi** → **Attacks** → **Rick Roll Beacon** (or equivalent: e.g. WiFi submenu with "Attacks" then "Rick Roll Beacon"). Match Marauder menu location: WiFi > Attacks > Rick Roll Beacon.
- On the Rick Roll screen: a control to **Start** and a control to **Stop**. When started, call the core transmission API (story 011) with the selected interface (from radio status or a dropdown); run until stopped or for a bounded time if the API supports it.
- Display status: e.g. "Idle", "Running", "Stopped". If core exposes packet count or rate, show it (e.g. "Packets sent: N" or "Rate: N/s"). If start fails (e.g. no monitor interface), show a clear error message.
- Interface selection: use the first monitor-capable interface from `core.radio` or let the user choose from a list; keep it simple. Document if only one interface is supported for now.
- No new core logic; Flet only calls core and displays results.

**ESP32 Marauder:** Menu: WiFi > Attacks > Rick Roll Beacon; attack runs until user exits (touch screen). We port: start/stop and status display.

## Acceptance criteria

- [ ] User can navigate from home to WiFi > Attacks > Rick Roll Beacon in the Flet app.
- [ ] User can start the Rick Roll Beacon (transmission starts using core API).
- [ ] User can stop the Rick Roll Beacon (transmission stops).
- [ ] Status is shown (Idle / Running / Stopped or equivalent).
- [ ] If core returns an error (e.g. no interface), the UI shows an error message and does not crash.
- [ ] Optional: packet count or rate is displayed when available from core.
- [ ] No core logic duplicated in the UI; all transmission via core.

## Definition of done

- Code merged. Manual test: start/stop from Flet and verify beacons (e.g. with another device scanning for networks). No regressions. KISS: minimal screens and controls.

## Subtasks / notes

- Run core transmission in a thread or async so the UI stays responsive for Stop. Join or cancel on stop.
