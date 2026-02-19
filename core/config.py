import os
import json
from pathlib import Path
import logging
from typing import Any

from core.radio import grab_all_bluetooth_interfaces, grab_all_wireless_interfaces

log = logging.getLogger(__name__)

"""
Config file format:
{
    "wifi_device": "wlan0",
    "bluetooth_device": "XX:XX:XX:XX:XX:XX"
}

File location:
$XDG_CONFIG_HOME/piraider/config.json
or
~/.config/piraider/config.json
"""

def _config_path() -> Path:
    base = Path(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")))
    return base / "piraider" / "config.json"


def load_config() -> dict:
    """
    Get the config from the config file.
    """
    path = _config_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        log.error(f"Failed to load config: {e}")
        return {}


def save_config(config: dict) -> None:
    """
    Save the config to the config file. Uses atomic write (temp file + rename).
    """
    path = _config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(".json.tmp")
    try:
        with open(temp_path, "w") as f:
            json.dump(config, f)
        os.replace(temp_path, path)
    except Exception as e:
        log.error(f"Failed to save config: {e}")
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise

def get_key(key: str, default: Any = None) -> Any:
    """
    Get a key from the config.
    """
    config = load_config()
    return config.get(key, default)

def set_key(key: str, value: Any) -> None:
    """
    Set a key in the config.
    """
    config = load_config()
    config[key] = value
    save_config(config)