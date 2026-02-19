"""Unit tests for core.config: load (missing, invalid, valid) and save (creates file, atomic)."""

import json
import pytest

from core.config import load_config, save_config


@pytest.fixture
def xdg_config_home(tmp_path, monkeypatch):
    """Point XDG_CONFIG_HOME at a temp dir so tests don't touch real config."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    return tmp_path


def test_load_config_missing_file_returns_empty_dict(xdg_config_home):
    """When config file does not exist, load_config returns {}."""
    # xdg_config_home is empty, so piraider/config.json does not exist
    assert load_config() == {}


def test_load_config_invalid_json_returns_empty_dict(xdg_config_home):
    """When config file contains invalid JSON, load_config returns {} and does not crash."""
    config_dir = xdg_config_home / "piraider"
    config_dir.mkdir(parents=True)
    (config_dir / "config.json").write_text("not valid json {")
    assert load_config() == {}


def test_load_config_valid_json_returns_parsed_dict(xdg_config_home):
    """When config file contains valid JSON, load_config returns the parsed dict."""
    config_dir = xdg_config_home / "piraider"
    config_dir.mkdir(parents=True)
    data = {"wifi_device": "wlan0", "bluetooth_device": "hci0"}
    (config_dir / "config.json").write_text(json.dumps(data))
    assert load_config() == data


def test_save_config_creates_file_and_parent_dirs(xdg_config_home):
    """save_config creates parent dirs if missing and writes the config file."""
    assert not (xdg_config_home / "piraider").exists()
    save_config({"a": 1, "b": "two"})
    config_file = xdg_config_home / "piraider" / "config.json"
    assert config_file.exists()
    assert json.loads(config_file.read_text()) == {"a": 1, "b": "two"}


def test_save_config_atomic_no_temp_left(xdg_config_home):
    """After a successful save, no .json.tmp file remains (atomic write via temp + rename)."""
    save_config({"wifi_device": "wlan0"})
    config_dir = xdg_config_home / "piraider"
    tmp_files = list(config_dir.glob("*.json.tmp"))
    assert tmp_files == [], "temp file must be removed after atomic rename"


def test_save_config_atomic_overwrites_existing(xdg_config_home):
    """Save overwrites existing config with new content in one shot (atomic)."""
    config_dir = xdg_config_home / "piraider"
    config_dir.mkdir(parents=True)
    (config_dir / "config.json").write_text('{"old": true}')
    save_config({"new": "value"})
    assert json.loads((config_dir / "config.json").read_text()) == {"new": "value"}
