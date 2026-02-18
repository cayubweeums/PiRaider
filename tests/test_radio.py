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


def test_wireless_empty_listing_returns_empty_dict_no_crash():
    """When iw dev returns empty or no interfaces, no crash and returns empty dict."""
    iw_dev_empty = MagicMock(returncode=0, stderr="", stdout="")
    with patch("core.radio.subprocess.run", return_value=iw_dev_empty):
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


def test_bluetooth_empty_listing_returns_empty_dict_no_crash():
    """When bluetoothctl list returns empty or no controllers, no crash and returns empty dict."""
    list_empty = MagicMock(returncode=0, stderr="", stdout="")
    with patch("core.radio.subprocess.run", return_value=list_empty):
        result = grab_all_bluetooth_interfaces()
    assert result == {}


def test_wireless_success_returns_expected_interface_data():
    """Successful iw/ip path returns parsed wireless interface data."""
    iw_dev_proc = MagicMock(returncode=0, stderr="", stdout="phy#0\n\tInterface wlan0\n")
    iw_phy_proc = MagicMock(returncode=0, stderr="", stdout="ignored by patched parser")
    ip_link_proc = MagicMock(returncode=0, stderr="", stdout="2: wlan0: <BROADCAST> state UP mode DEFAULT\n")

    parsed_phy = {
        "phy0": {
            "Supported interface modes": {"_items": ["managed", "monitor"]},
            "Band 1": {"Frequencies": {"_items": ["2412.0 MHz [1] (30.0 dBm)"]}},
            "Band 2": {"Frequencies": {"_items": ["5180.0 MHz [36] (23.0 dBm)"]}},
        }
    }

    with patch("core.radio.subprocess.run", side_effect=[iw_dev_proc, iw_phy_proc, ip_link_proc]), patch(
        "core.radio.parse_indented_output", return_value=parsed_phy
    ):
        result = grab_all_wireless_interfaces()

    assert result == {
        "wlan0": {
            "physical_id": "phy0",
            "device_id": "wlan0",
            "interface_up": True,
            "monitor_mode_supported": True,
            "band_capability": {
                "Band 1": "2.4",
                "Band 2": "5",
            },
        }
    }


def test_bluetooth_success_returns_expected_controller_data():
    """Successful bluetoothctl path returns controller data keyed by MAC."""
    list_proc = MagicMock(
        returncode=0,
        stderr="",
        stdout="Controller 4C:49:6C:9D:4D:14 cayub-gamin [default]\n",
    )
    show_proc = MagicMock(returncode=0, stderr="", stdout="ignored by patched parser")
    parsed_bt = {
        "Controller": "4C:49:6C:9D:4D:14 (public)",
        "Name": "cayub-gamin",
        "Powered": "yes",
        "Discoverable": "no",
        "Pairable": "yes",
        "Discovering": "yes",
        "Roles": "peripheral",
    }

    with patch("core.radio.subprocess.run", side_effect=[list_proc, show_proc]), patch(
        "core.radio.parse_indented_output", return_value=parsed_bt
    ):
        result = grab_all_bluetooth_interfaces()

    assert result == {
        "4C:49:6C:9D:4D:14": {
            "controller_mac": "4C:49:6C:9D:4D:14",
            "controller_name": "cayub-gamin",
            "powered": "yes",
            "discoverable": "no",
            "pairable": "yes",
            "discovering": "yes",
            "roles": "peripheral",
        },
    }
