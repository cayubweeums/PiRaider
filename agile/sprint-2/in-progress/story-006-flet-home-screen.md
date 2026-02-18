# [STORY-006] Flet home screen with device list and capabilities

## Summary

Implement a Flet home screen with top-level buckets (WiFi, Bluetooth, Device), radio status, and a **device list** showing available WiFi interfaces and Bluetooth controllers with their **capabilities** from `core.radio`.

## Description

The PoC requires a Flet home screen matching Marauder’s top-level buckets (WiFi, Bluetooth, Device) as placeholders, plus radio status. This story extends that with a **device list** showing what radios are available and their capabilities so the user can understand what hardware is usable before later selecting devices for testing.

**Scope:**
- Flet app (under `ui/flet/`) shows a home screen with three top-level buckets: **WiFi**, **Bluetooth**, **Device** (placeholders; no full submenus).
- **Radio status line:** "radios ready" or "not available" from `core.radio` at load time (criteria: at least one WiFi interface with monitor capability and/or BT adapter up).
- **Device list:** Display the list of available devices from `core.radio`:
  - **WiFi:** For each interface from `grab_all_wireless_interfaces()`, show: interface ID, interface up/down, band capability (2.4/5/6 GHz), monitor support (if core exposes it).
  - **Bluetooth:** For each controller from `grab_all_bluetooth_interfaces()`, show: controller ID and whatever capabilities the current core returns (e.g. Powered, Discoverable, Pairable).
- Use **raw IDs** for now (e.g. `wlan0`, `hci0`); friendly names are handled in Story 009.
- Layout: minimal and readable; follow Flet conventions.
- Entrypoint: `main.py`; default run launches this Flet app.

**Core dependency:** `core.radio` must return:
- `grab_all_wireless_interfaces()` → dict keyed by interface ID; values: `physical_id`, `device_id`, `interface_up`, `band_capability` (dict of band labels); `monitor_supported` (bool) if available or inferred.
- `grab_all_bluetooth_interfaces()` → dict keyed by controller ID; values: parsed `bluetoothctl show` output (controller info, Powered, etc.).

If core does not yet return `monitor_supported` for WiFi, add it as a small extension or infer from existing `iw phy` data within this story.

## Acceptance criteria

- [x] Running `poetry run python main.py` opens the Flet app with a home screen.
- [x] The home screen shows three top-level buckets: WiFi, Bluetooth, Device (placeholders; no full submenus).
- [x] The home screen shows radio status: "radios ready" or "not available", derived from `core.radio` at load time.
- [x] The home screen shows a **list of WiFi interfaces** from `grab_all_wireless_interfaces()` with: interface ID, up/down state, band capability, monitor support.
- [ ] The home screen shows a **list of Bluetooth controllers** from `grab_all_bluetooth_interfaces()` with: controller ID and relevant capabilities (e.g. Powered, Discoverable).
- [ ] No crash if radio module returns empty or error; show "not available" or empty list.
- [ ] No new dependencies beyond those already in the project.

## Definition of done

- Code merged. Flet app runs and shows buckets, radio status, and device list with capabilities. Tests: covered by existing pytest if any UI tests are added; otherwise manual check is acceptable. KISS: simplest layout that meets criteria.

## Subtasks / notes

- Radio status can be a single line or two lines for WiFi/BT; keep it simple.
- Device list can be two sections (WiFi, Bluetooth) or a combined list; designer choice.
- If `grab_all_wireless_interfaces` or `grab_all_bluetooth_interfaces` do not yet return the expected structure, extend core in this story or file a quick follow-up; this story unblocks on usable data from core.
