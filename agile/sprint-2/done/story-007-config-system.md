# [STORY-007] Config system for user preferences

## Summary

Implement a minimal config system that persists user preferences between app instances. Uses XDG config dir, JSON format, and stdlib-only. No new dependencies.

## Description

User preferences (e.g. selected WiFi/BT devices) must persist between runs. This story adds a **KISS config system**: single module, JSON file, XDG-compliant path, atomic writes.

**Design**

1. **Config path**
   - `$XDG_CONFIG_HOME/piraider/config.json` (or `~/.config/piraider/config.json` when `XDG_CONFIG_HOME` unset).
   - Create parent dirs on first save if missing.

2. **Format**
   - JSON object. Flat key-value for now. Example:
     ```json
     {"wifi_device": "wlan0", "bluetooth_device": "hci0"}
     ```
   - Extensible: add keys as new preferences are introduced (Story 010 and later).

3. **API** (`core/config.py`)
   - `load_config() -> dict`: Read and parse JSON. Return `{}` if file missing or invalid.
   - `save_config(config: dict) -> None`: Write config. Atomic: write to temp file in same dir, then `os.replace()` to target.
   - Optional convenience: `get(key: str, default: Any = None) -> Any` and `set(key: str, value: Any)` that load/save on each call — or keep it simpler: callers use `load_config()`, mutate dict, call `save_config()`. Prefer the latter for KISS.

4. **Error handling**
   - Missing file: return `{}`.
   - Invalid JSON: return `{}` and optionally log; do not crash.
   - Write failure (permission, disk full): log and raise; caller handles.

5. **Dependencies**
   - None. Use stdlib: `json`, `pathlib`, `os`. No TOML, no YAML, no extra packages.

6. **Known keys** (for Story 010)
   - `wifi_device`: str, interface ID (e.g. `wlan0`).
   - `bluetooth_device`: str, controller ID (e.g. `hci0`).

**Dependencies:** None. This story should be completed before Story 010 (device selection), which uses config for persistence.

**Scope:**
- Add `core/config.py` with `load_config()` and `save_config(config)`.
- Tests: unit tests for load (missing file, invalid JSON, valid JSON), save (atomic write, dir creation).
- No UI; no Flet/Rich. Pure core module.

## Acceptance criteria

- [x] `core/config.py` provides `load_config() -> dict` and `save_config(config: dict) -> None`.
- [x] Config path follows XDG: `$XDG_CONFIG_HOME/piraider/config.json` or `~/.config/piraider/config.json`.
- [x] Missing config file returns `{}`.
- [x] Invalid JSON returns `{}` (no crash).
- [x] Save uses atomic write (temp file + rename).
- [x] Parent dirs created on first save if missing.
- [x] No new dependencies; stdlib only.
- [x] Unit tests cover load (missing, invalid, valid) and save (creates file, atomic).

## Definition of done

- Code merged. Config module works; tests pass. Story 010 (device selection) will use this for persisting selected devices.

## Subtasks / notes

- `pathlib.Path` for path handling.
- `config_path = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "piraider" / "config.json"`
- Temp file: `config_path.with_suffix(".json.tmp")` or similar; delete on success after rename.
