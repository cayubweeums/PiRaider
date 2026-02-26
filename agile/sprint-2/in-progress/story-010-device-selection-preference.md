# [STORY-010] Device selection and default preference

## Summary

Let the user select which WiFi interface and which Bluetooth controller to use for testing. Add a preference rule to choose a default device when none is selected. Persist selections via the config system (Story 007).

## Description

On a typical host (e.g. Raspberry Pi, laptop) there can be multiple WiFi interfaces and multiple Bluetooth controllers. The UI must support **choosing** which device to use for WiFi and which for Bluetooth. When the user has not selected a device, a **default** is chosen automatically by a documented heuristic. Selections **persist** between app instances via the config system.

**Scope:**
- **Selection UI:** Dropdowns or list selection in the Flet home screen (or a dedicated device/settings area) to pick one WiFi interface and one Bluetooth controller.
- **Persistence:** Use `core.config` (Story 007) to store `wifi_device` and `bluetooth_device`. On load: read from config; on selection change: update config via `save_config()`.
- **Preference rule:** When no user selection exists (config empty or invalid), choose defaults as follows:
  - **WiFi:** Prefer an interface that (1) supports monitor mode, (2) is up, (3) supports 5 GHz if available. If multiple qualify, prefer the first by interface order. If none has monitor, prefer first up; if none up, prefer first available.
  - **Bluetooth:** Prefer the first controller that is powered. If none powered, prefer first available.
  - Document this rule in the story and in code (e.g. docstring or comment).
- **Integration:** Selected devices are available to the app (e.g. passed to future WiFi/BT tools); UI shows which device is "active" for each bucket.

**Dependencies:** Story 006 (device list with capabilities), Story 007 (config system), Story 009 (friendly names) provide the data, persistence, and display. This story adds selection controls and applies the preference when config is empty.

## Acceptance criteria

- [ ] User can select one WiFi interface from a dropdown or list (populated from `grab_all_wireless_interfaces()`).
- [ ] User can select one Bluetooth controller from a dropdown or list (populated from `grab_all_bluetooth_interfaces()`).
- [ ] When no selection exists in config, the app uses the **default preference** rule (WiFi: prefer monitor-capable, up, 5 GHz; BT: prefer first powered).
- [ ] The preference rule is documented in the story and in code.
- [ ] Selected WiFi and BT devices are **persisted** via `core.config` and restored on next app launch.
- [ ] UI indicates which device is currently selected/active for WiFi and for Bluetooth.
- [ ] No crash when no WiFi or no BT devices exist; show empty/disabled state.

## Definition of done

- Code merged. Selection UI works; preference rule applied; selections persist via config. Tests for the preference logic (unit tests with mocked device lists). Manual check for selection, persistence, and default behavior.

## Subtasks / notes

- Preference logic can live in a small function or module (e.g. `core/device_prefs.py` or similar) so it's testable.
- Config keys: `wifi_device`, `bluetooth_device` (per Story 007).
- "First by interface order" = iteration order of the dict from core; typically `wlan0` before `wlan1` etc.
