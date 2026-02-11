# [STORY-004] Core radio module

## Summary

Implement `core/radio.py` to auto-detect WiFi and Bluetooth interfaces and report their capabilities (monitor mode, bands, BT status) so both UIs can show "radios ready" or "not available" without failing later.

## Description

The PoC requires automatic detection and configuration of interfaces: which WiFi devices support monitor mode; which support 2.4 / 5 / 6 GHz; Bluetooth adapter status and usability for scanning. A small module (e.g. `core/radio.py`) returns these; no UI in core.

**Scope:**
- Add `core/radio.py` (and ensure `core/` is a package if needed). Expose a small, stable API: e.g. a function like `get_radio_status()` or `get_wifi_capabilities()` and `get_bt_status()` that return structured data (dicts or dataclasses).
- WiFi: detect interfaces (e.g. via `iw`, `ip link`, or platform-specific calls); for each, determine if monitor mode is supported; determine band support (2.4, 5, 6 GHz) where possible. Prefer subprocess calls to existing tools (iw, iwconfig) over custom C extensions. Return a list of interfaces with at least: name, monitor_capable, bands (or similar).
- Bluetooth: detect adapter (e.g. via `hciconfig` or `bluetoothctl`); report whether an adapter is present and up/usable for scanning. Return at least: present, up (or equivalent).
- No UI code in `core/`; no Flet or Rich imports in `core/radio.py`. Core only exposes functions and data.
- Handle missing tools or permissions gracefully: return "not available" or equivalent rather than raising uncaught exceptions to the caller.

**ESP32 Marauder:** Marauder runs on ESP32 with built-in WiFi/BT; we port the *concept* of "radios ready" and capability reporting to a PC/Pi environment where we query the OS and existing CLI tools.

## Acceptance criteria

- [ ] `core/radio.py` exists and is importable from the project.
- [ ] At least one public function returns WiFi capability info (e.g. list of interfaces with monitor capability and band info, or a single aggregate "ready" flag with details).
- [ ] At least one public function returns Bluetooth adapter status (present, up/usable).
- [ ] No UI dependencies in `core/radio.py`; no Flet or Rich in core.
- [ ] If `iw`/`ip`/Bluetooth tools are missing or fail, the module returns safe values (e.g. "not available" or empty list) rather than crashing.
- [ ] API is documented enough for UI callers (docstrings or type hints).

## Definition of done

- Code merged. Tests for this module are in story 005; this story only requires the implementation. No known regressions. KISS: minimal abstraction, use subprocess to existing tools where possible.

## Subtasks / notes

- Linux-first is acceptable; document "tested on Linux" if Windows/macOS are not supported for radio detection.
- Example API: `def get_wifi_status() -> dict: ...` with keys like `interfaces`, `monitor_capable`, `bands`; `def get_bt_status() -> dict: ...` with `present`, `up` or similar.
