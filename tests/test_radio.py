"""Tests for core.radio module. Uses mocked subprocess output."""

import pytest
from unittest.mock import patch, MagicMock

from core.radio import grab_all_wireless_interfaces, grab_all_bluetooth_interfaces


def test_wireless_tools_missing_or_error_returns_empty_dict():
    """When iw is missing or fails, no exception is raised and returns empty dict."""
    with patch("core.radio.subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("iw not found")
        result = grab_all_wireless_interfaces()
    assert result == {}


def test_wireless_tools_return_nonzero_returns_empty_dict():
    """When iw returns non-zero exit, no exception and returns empty dict."""
    mock_proc = MagicMock()
    mock_proc.returncode = 1
    mock_proc.stderr = "command not found"
    mock_proc.stdout = ""
    with patch("core.radio.subprocess.run", return_value=mock_proc):
        result = grab_all_wireless_interfaces()
    assert result == {}


def test_bluetooth_tools_missing_or_error_returns_empty_dict():
    """When bluetoothctl is missing or fails, no exception and returns empty dict."""
    with patch("core.radio.subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("bluetoothctl not found")
        result = grab_all_bluetooth_interfaces()
    assert result == {}


def test_bluetooth_tools_return_nonzero_returns_empty_dict():
    """When bluetoothctl returns non-zero exit, no exception and returns empty dict."""
    mock_proc = MagicMock()
    mock_proc.returncode = 1
    mock_proc.stderr = "Failed to connect"
    mock_proc.stdout = ""
    with patch("core.radio.subprocess.run", return_value=mock_proc):
        result = grab_all_bluetooth_interfaces()
    assert result == {}
