# [STORY-008] Beacon frame builder (core)

## Summary

Implement a function in core that builds a single 802.11 beacon frame as a **Scapy packet** from an SSID string (and optional BSSID / random BSSID) so the Rick Roll Beacon and future beacon-based tools can generate frames without duplicating logic.

## Description

The first real tool is the Rick Roll Beacon. In ESP32 Marauder, beacon frames are built from a hardcoded 128-byte base packet; the SSID and BSSID are overwritten (see `WiFiScan.h`: `packet[128]`, `rick_roll[8]`; wiki "Rick Roll Beacon"). This story ports the minimal "build one beacon frame" logic to Python in core: given an SSID string, produce a **Scapy packet object** (e.g. `scapy.packet.Packet`) representing the beacon frame (and optionally support random or explicit BSSID). No transmission yet.

**Scope:**
- Add a module under `core/` for beacon building (e.g. `core/beacon.py`). One clear responsibility: build one 802.11 beacon frame using **Scapy** (e.g. `Dot11`, `Dot11Beacon`, `Dot11Elt`, `RadioTap`), not raw `struct`/`bytearray`.
- Input: SSID (string); optional: BSSID (6 bytes) or "random BSSID". Output: **Scapy packet** (e.g. `scapy.packet.Packet`), not raw `bytes`. Callers may serialize with `bytes(packet)` for injection later. Frame format must match 802.11 beacon: Frame Control (beacon subtype), Duration, DA (broadcast), SA, BSSID, Sequence control, Timestamp, Beacon interval, Capability info, SSID IE (tag 0x00, length, SSID bytes). Reference: `WiFiScan.h` lines 324–336 (barebones packet).
- SSID length: handle at least 0–32 bytes (802.11). No encryption or other IEs required for PoC.
- No UI; no Flet/Rich in core. No transmission in this story.

**ESP32 Marauder:** `esp32_marauder/WiFiScan.h` — `packet[128]` base; SA/BSSID overwritten; SSID at offset 36 (0x00 tag, then length, then SSID). We replicate the same logical structure with Scapy so that generated frames are valid.

## Acceptance criteria

- [x] A function exists in core that takes an SSID string (and optionally BSSID or "random") and returns a **Scapy packet object** (e.g. `scapy.packet.Packet`) containing a single beacon frame.
- [x] The returned packet has correct structure: FC (beacon subtype), Duration, DA=0xff:ff:ff:ff:ff:ff, SA, BSSID, Seq, Timestamp, Beacon interval, Capability, SSID IE with the given SSID.
- [x] If "random BSSID" is used, SA and BSSID are the same 6 random bytes (or locally administered); no hardcoded BSSID in that mode.
- [x] SSID length 0–32 is supported; no crash for empty string or long string (truncate or reject with clear behavior; document it).
- [x] No UI or transmission code in this module.

## Definition of done

- Code merged. Unit tests cover the beacon builder. No regressions. KISS: one function or small set of functions; no extra abstraction.

## Subtasks / notes

- Build the beacon with **Scapy**: `RadioTap`, `Dot11` (type=0, subtype=8), `Dot11Beacon`, `Dot11Elt` for SSID (and optionally Rates, DS Parameter Set). Return the assembled `Packet`; callers may use `bytes(packet)` for injection. Do not build the frame from raw `struct`/`bytearray` in core.
