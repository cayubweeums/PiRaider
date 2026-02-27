# [STORY-010] Rick Roll Beacon core logic

## Summary

Implement the core logic for the Rick Roll Beacon: cycle through the eight lyric SSIDs and produce a sequence of beacon frames (using the beacon builder), without transmission or UI.

## Description

In ESP32 Marauder, the Rick Roll Beacon sends beacon frames whose SSIDs are the eight "Never Gonna Give You Up" lyric lines (see `WiFiScan.h` `rick_roll[8]`). This story implements the same list and the logic that cycles through them to produce frames; transmission and UI are separate stories.

**Scope:**
- Add Rick Roll–specific logic in core (e.g. in `core/beacon.py` or `core/rick_roll.py`). Expose a simple API: e.g. "get the list of Rick Roll SSIDs" and "get the next beacon frame (bytes) for the current lyric index" so that a caller (transmission or test) can iterate.
- The eight SSIDs must match Marauder’s lyrics (e.g. "01 Never gonna give you up", "02 Never gonna let you down", … "08 and hurt you"). Exact strings from upstream: `WiFiScan.h` lines 317–326.
- Use the beacon builder from story 008 to build each frame; BSSID can be random per frame (Marauder overwrites BSSID with random bytes each time).
- No transmission (no raw socket, no subprocess to injector). No UI. Callable from tests and from the future transmission layer.

**ESP32 Marauder:** `esp32_marauder/WiFiScan.h` — `rick_roll[8]` and the loop that calls the equivalent of broadcastSetSSID with each lyric; we only implement the data + "next frame" logic here.

## Acceptance criteria

- [ ] The eight Rick Roll SSIDs are defined in core and match the Marauder lyric strings.
- [ ] There is a way to obtain "the next beacon frame" for the Rick Roll sequence (e.g. function that returns (frame_bytes, ssid_index) or yields frames in order). Cycling (after 8, back to 0) is implemented.
- [ ] Each frame is built via the beacon builder (story 008); BSSID is random per frame or per call.
- [ ] No transmission or UI code; core-only.
- [ ] Unit test: iterating 8 times (or 9) returns correct SSIDs in order and frames are valid (e.g. contain the expected SSID).

## Definition of done

- Code merged. Unit test(s) pass. No regressions. KISS: minimal logic, reuse beacon builder.

## Subtasks / notes

- API idea: `def next_rick_roll_frame() -> bytes` with an internal counter, or `def rick_roll_frames()` generator yielding (bytes, ssid_string). Choose one and stick to it.
