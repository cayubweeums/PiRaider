# [STORY-008] Beacon frame builder (core)

## Summary

Implement a function in core that builds 802.11 beacon frame bytes from an SSID string (and optional random BSSID) so the Rick Roll Beacon and future beacon-based tools can generate frames without duplicating logic.

## Description

The first real tool is the Rick Roll Beacon. In ESP32 Marauder, beacon frames are built from a hardcoded 128-byte base packet; the SSID and BSSID are overwritten (see `WiFiScan.h`: `packet[128]`, `rick_roll[8]`; wiki "Rick Roll Beacon"). This story ports the minimal "build one beacon frame" logic to Python in core: given an SSID string, produce the raw beacon frame bytes (and optionally randomize BSSID). No transmission yet.

**Scope:**
- Add a module under `core/` for beacon building (e.g. `core/beacon.py` or `core/wifi.py`). One clear responsibility: build 802.11 beacon frame bytes.
- Input: SSID (string); optional: BSSID (6 bytes) or "random BSSID". Output: bytes (full beacon frame, suitable for injection later). Frame format must match the Marauder structure: Frame Control, Duration, DA (0xff...), SA, BSSID, Sequence control, Timestamp, Beacon interval, Capability info, SSID IE (tag 0x00, length, SSID bytes). Reference: `WiFiScan.h` lines 324–336 (barebones packet).
- SSID length: handle at least 0–32 bytes (802.11). No encryption or other IEs required for PoC.
- No UI; no Flet/Rich in core. No transmission in this story.

**ESP32 Marauder:** `esp32_marauder/WiFiScan.h` — `packet[128]` base; SA/BSSID overwritten; SSID at offset 36 (0x00 tag, then length, then SSID). We replicate the same structure so that generated frames are valid.

## Acceptance criteria

- [ ] A function exists in core that takes an SSID string (and optionally BSSID or "random") and returns a `bytes` object containing a single beacon frame.
- [ ] The returned frame has correct structure: FC, Duration, DA=0xff:ff:ff:ff:ff:ff, SA, BSSID, Seq, Timestamp, Beacon interval, Capability, SSID IE with the given SSID.
- [ ] If "random BSSID" is used, SA and BSSID are the same 6 random bytes (or locally administered); no hardcoded BSSID in that mode.
- [ ] SSID length 0–32 is supported; no crash for empty string or long string (truncate or reject with clear behavior; document it).
- [ ] No UI or transmission code in this module.

## Definition of done

- Code merged. Unit tests in story 009. No regressions. KISS: one function or small set of functions; no extra abstraction.

## Subtasks / notes

- Marauder base packet (hex): 0x80 0x00 0x00 0x00 (FC, Duration), then 6 bytes DA, 6 SA, 6 BSSID, 2 seq, 8 timestamp, 2 interval, 2 capability, then SSID IE (0x00, len, payload). Build this in Python (struct or bytearray).
