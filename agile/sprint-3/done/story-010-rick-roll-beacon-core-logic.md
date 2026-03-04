# [STORY-010] Rick Roll Beacon core logic

## Summary

Implement the core logic for the Rick Roll Beacon in `core/wifi.py`: define the eight lyric SSIDs and expose functions to get SSIDs (by index or full list) and to get all beacon frames as Scapy packets, without transmission or UI.

## Description

In ESP32 Marauder, the Rick Roll Beacon sends beacon frames whose SSIDs are the eight "Never Gonna Give You Up" lyric lines (see `WiFiScan.h` `rick_roll[8]`). This story implements the same list and a simple API in `core/wifi.py` so that callers (transmission or tests) can obtain SSID strings and beacon frames; transmission and UI are separate stories.

**Approach:**
- **SSIDs in `core/wifi.py`:** The eight Rick Roll SSIDs are defined as a list of strings (matching Marauder’s lyrics). Two functions provide access:
  - **By index:** A function that, given an index, returns the Rick Roll SSID string at that index (e.g. for "next" or a specific lyric). Invalid or missing index can return the first SSID or the caller can use the full list and index themselves.
  - **Full list:** A function (or direct use of the list) that returns all eight Rick Roll SSID strings in order, so callers can iterate or pick by index.
- **Beacon frames in `core/wifi.py`:** A separate function that, when called, builds and returns **all** Rick Roll beacon frames in order as a **list of Scapy packets**. Each frame is built via the beacon builder (story 008); BSSID is random per frame when not provided.
- No transmission (no raw socket, no subprocess). No UI. Callable from tests and from the future transmission layer.

**ESP32 Marauder:** `esp32_marauder/WiFiScan.h` — `rick_roll[8]`; we only implement the data + SSID access + "all frames" list here.

## Acceptance criteria

- [x] The eight Rick Roll SSIDs are defined in `core/wifi.py` and match the Marauder lyric strings.
- [x] A function in `core/wifi.py` returns a single Rick Roll SSID string given an index (or the first/default when index is out of range or omitted).
- [x] A function in `core/wifi.py` returns the full list of Rick Roll SSID strings in order (or the list is exposed so callers can get "all" without a separate function, and the index-based function covers "next/one").
- [x] A function in `core/wifi.py` returns all Rick Roll beacon frames in order as a list of Scapy packets; each frame is built via the beacon builder; BSSID is random per frame when not provided.
- [x] No transmission or UI code; core-only.
- [x] Unit test(s): SSID by index and full list behave correctly; the "all frames" function returns 8 packets with expected SSIDs in order.

## Definition of done

- Code merged. Unit test(s) pass. No regressions. KISS: minimal logic, reuse beacon builder.

## Subtasks / notes

- SSID API: e.g. `get_rick_roll_ssids(index=None)` returning one string by index, and the list `rick_roll_ssids` (or `get_rick_roll_ssids_list()`) for the full list. Adjust to match actual API.
- Frames API: e.g. `get_rick_roll_beacon_frames() -> list[Packet]` that returns all eight frames in order.
