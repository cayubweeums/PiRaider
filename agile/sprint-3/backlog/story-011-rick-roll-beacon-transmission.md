# [STORY-011] Rick Roll Beacon transmission

## Summary

Wire beacon transmission so that the Rick Roll Beacon can send frames over the air from a monitor-mode interface, using the core beacon builder and Rick Roll logic, with a clear start/stop or time-limited run.

## Description

The Rick Roll tool must actually transmit beacon frames so that devices nearby see the lyric SSIDs. On a Pi/laptop we use an external WiFi interface in monitor mode and either raw socket injection or a subprocess to an existing tool (e.g. `aireplay-ng`, or a small helper). This story implements the transmission path in core and documents requirements (monitor mode, permissions, supported platforms).

**Scope:**
- Core only: an interface to "run Rick Roll Beacon" that (1) uses the beacon builder and Rick Roll logic to produce frames, (2) sends them via a chosen method. Options: (a) subprocess to a tool that accepts beacon frames or pcap; (b) raw socket (Linux) if dependencies allow; (c) documented "manual" flow (e.g. write pcap and user runs `tcpreplay`). Prefer the simplest option that works on Linux with a typical monitor-capable dongle.
- Start/stop: either run for a bounded time (e.g. N seconds) or run until stopped (e.g. by UI). Expose a simple API: e.g. `run_rick_roll(interface: str, duration_seconds: Optional[int] = None)` or `start_rick_roll(interface)` / `stop_rick_roll()`. Document behavior if interface is not in monitor mode.
- Document: which tools or kernel interfaces are required (e.g. `iw`, monitor mode, possibly `libpcap` or external binary), and that the user must put the interface in monitor mode (or we do it in this story if KISS allows). No silent failures: if transmission is not possible, log or return a clear error.
- No UI in this story; UI integration in Sprint 4. Optional: log or return packet count for the UI to display later.

**ESP32 Marauder:** On ESP32, `esp_wifi_80211_tx()` sends the frame. We port the *effect* (send beacon frames in a loop) to a host environment using OS and tooling.

## Acceptance criteria

- [ ] There is a core API to run the Rick Roll Beacon (e.g. `run_rick_roll(interface, duration_seconds)` or equivalent) that sends beacon frames built from the Rick Roll logic.
- [ ] Frames are sent using the chosen method (subprocess or raw socket); method is documented.
- [ ] If the interface is not available or not in monitor mode, the function exits or returns with a clear error (no silent failure).
- [ ] Requirements (monitor mode, tool names, permissions) are documented (e.g. in README or docstring).
- [ ] No UI code in core; transmission can be tested manually or via a small script.
- [ ] Optional: packet count or status is available for the UI (e.g. return value or callback).

## Definition of done

- Code merged. Manual test possible: run from CLI or script with a monitor-mode interface and observe SSIDs on another device or sniffer. No regressions. KISS: minimal transmission path; prefer existing tools over custom C/Rust if they suffice.

## Subtasks / notes

- If using subprocess: e.g. write beacon frames to a pcap or pipe and invoke `aireplay-ng` or similar; or use a Python library that wraps injection (e.g. scapy with monitor interface). Document the choice.
- If raw socket is used: Linux only; require CAP_NET_RAW or root; document it.
