# [STORY-009] Friendly device names for WiFi and Bluetooth

## Summary

Display human-readable "common device names" for WiFi interfaces and Bluetooth controllers instead of raw IDs (e.g. `wlan0`, `hci0`). Implement the lookup logic and define how names are obtained on Linux.

## Description

Users should see friendly names like "(Built-in)", "(Internal)", "(ALFA 83473LNM)" rather than only technical IDs. This story defines **how** to obtain and map those names on a Linux host, implements the lookup, and wires it into the Flet device list (Story 006).

**Scope:**
- Add a core helper (e.g. in `core/` or `core/utils.py`) that maps `device_id` / `physical_id` / controller ID to a friendly name.
- Use friendly names in the Flet device list when available; fallback to raw ID + "(Unknown)" or "(No description)" when not found.
- Document the design so a developer can implement without guessing.

**Design: how we find friendly names**

1. **WiFi interfaces**
   - **sysfs:** `/sys/class/net/<device_id>/device/` links to the physical device. Read `uevent` or `product`/`vendor` for USB devices.
   - **USB devices:** `/sys/class/net/<device_id>/device/../../idVendor` and `idProduct` (or `modalias`) → match against `lsusb` output or a static USB ID database (e.g. `/usr/share/hwdata/usb.ids` or `usb-devices` output) for vendor/model strings.
   - **PCI devices:** `/sys/class/net/<device_id>/device/vendor` and `device` → match against `lspci` or PCI ID database for vendor/device names.
   - **Built-in detection:** Devices under `/sys/class/net/<device_id>/device/subsystem/` or parent bus (e.g. `pci`) with no USB parent → treat as built-in; use "(Built-in)" or "(Internal)".
   - **udev (optional):** `udevadm info -e -n <device_id>` for `ID_NET_NAME`, `ID_VENDOR`, `ID_MODEL` etc. as fallback.

2. **Bluetooth controllers**
   - **bluetoothctl show:** `bluetoothctl show <controller_id>` returns `Name` and `Alias` — use these when present.
   - **sysfs:** `/sys/class/bluetooth/<controller_id>/device/` has similar vendor/device/product for USB/PCI devices.
   - **Built-in:** Same heuristic as WiFi; PCI devices on motherboard = "(Built-in)".

3. **Fallback**
   - If no friendly name found: show `device_id (Unknown)` or `device_id (No description)`.
   - Prefer simplicity: use one or two reliable sources (e.g. sysfs + bluetoothctl) before adding udev/lspci/lsusb.

4. **Output format**
   - Friendly name: e.g. `wlan0 — ALFA 83473LNM` or `wlan0 (ALFA 83473LNM)` or `ALFA 83473LNM (wlan0)`; decide and document. Must include the raw ID so the user can correlate with system tools.

## Acceptance criteria

- [ ] A core helper (or module) resolves `device_id` for WiFi and controller ID for BT to a friendly name string.
- [ ] WiFi: Built-in devices show "(Built-in)" or "(Internal)"; USB/PCI devices show vendor/model when available from sysfs, udev, lsusb, or lspci.
- [ ] Bluetooth: `bluetoothctl show` Name/Alias used when present; otherwise sysfs/udev for USB/PCI; built-in shows "(Built-in)".
- [ ] Fallback: when no friendly name found, show `device_id (Unknown)` or `device_id (No description)`.
- [ ] The Flet device list (Story 006) displays friendly names instead of raw IDs when the helper is wired in.
- [ ] The story or code documents which OS sources are used and the mapping logic (inline comments or a short design note in the module).

## Definition of done

- Code merged. Helper implemented and used in Flet device list. Tests for the helper (e.g. mock sysfs/bluetoothctl) where practical. Manual check on real hardware with built-in and USB devices.

## Subtasks / notes

- Start with sysfs + bluetoothctl; add udev/lsusb/lspci only if needed for better coverage.
- USB ID database: `usb.ids` or `lsusb -v` parsing; avoid adding heavy deps; prefer stdlib + subprocess where possible.
- Consider caching lookups (devices rarely change during a session).
