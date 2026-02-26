# [STORY-010] Device selection and persistence

## Summary

Let the user select which WiFi interface and which Bluetooth controller to use for testing. Persist selections via the config system (Story 007).

## Description

On a typical host (e.g. Raspberry Pi, laptop) there can be multiple WiFi interfaces and multiple Bluetooth controllers. The UI must support **choosing** which device to use for WiFi and which for Bluetooth. Selections **persist** between app instances via the config system.

**Scope:**
- **Selection UI:** Dropdowns or list selection in the Flet home screen (or a dedicated device/settings area) to pick one WiFi interface and one Bluetooth controller.
- **Persistence:** Use `core.config` (Story 007) to store `wifi_device` and `bluetooth_device`. On load: read from config; on selection change: update config via `save_config()`.
- **Integration:** Selected devices are available to the app (e.g. passed to future WiFi/BT tools); UI shows which device is "active" for each bucket.

**Dependencies:** Story 006 (device list with capabilities), Story 007 (config system), Story 009 (friendly names) provide the data, persistence, and display. This story adds selection controls and persistence of the user’s choice.

## Acceptance criteria

- [x] User can select one WiFi interface from a dropdown or list (populated from `grab_all_wireless_interfaces()`).
- [x] User can select one Bluetooth controller from a dropdown or list (populated from `grab_all_bluetooth_interfaces()`).
- [x] Selected WiFi and BT devices are **persisted** via `core.config` and restored on next app launch.
- [x] UI indicates which device is currently selected/active for WiFi and for Bluetooth.
- [x] No crash when no WiFi or no BT devices exist; show empty/disabled state.

## Definition of done

- Code merged. Selection UI works; selections persist via config. Manual check for selection and persistence.

## Subtasks / notes

- Config keys: `wifi_device`, `bluetooth_device` (per Story 007).
