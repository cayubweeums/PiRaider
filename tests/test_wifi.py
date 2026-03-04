"""Tests for core.wifi Rick Roll Beacon: SSIDs, beacon frames, and start/stop/status API."""

from unittest.mock import MagicMock, patch

import pytest
import scapy.packet
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, RadioTap

from core.wifi import (
    rick_roll_ssids,
    get_rick_roll_ssids,
    get_rick_roll_beacon_frames,
    is_rick_roll_beacon_running,
    start_rick_roll_beacon,
    stop_rick_roll_beacon,
)

EXPECTED_RICK_ROLL_SSIDS = [
    "01 Never gonna give you up",
    "02 Never gonna let you down",
    "03 Never gonna run around",
    "04 and desert you",
    "05 Never gonna make you cry",
    "06 Never gonna say goodbye",
    "07 Never gonna tell a lie",
    "08 and hurt you",
]


def test_rick_roll_ssids_length_and_content():
    """The eight Rick Roll SSIDs are defined and match the Marauder lyric strings."""
    assert len(rick_roll_ssids) == 8
    assert rick_roll_ssids == EXPECTED_RICK_ROLL_SSIDS


def test_get_rick_roll_ssids_index_0():
    """get_rick_roll_ssids(0) returns the first SSID."""
    assert get_rick_roll_ssids(0) == EXPECTED_RICK_ROLL_SSIDS[0]


def test_get_rick_roll_ssids_index_4():
    """get_rick_roll_ssids(4) returns the fifth SSID."""
    assert get_rick_roll_ssids(4) == EXPECTED_RICK_ROLL_SSIDS[4]


def test_get_rick_roll_ssids_index_7():
    """get_rick_roll_ssids(7) returns the last SSID."""
    assert get_rick_roll_ssids(7) == EXPECTED_RICK_ROLL_SSIDS[7]


def test_get_rick_roll_ssids_none_returns_first():
    """get_rick_roll_ssids(None) returns the first SSID (default)."""
    assert get_rick_roll_ssids(None) == EXPECTED_RICK_ROLL_SSIDS[0]


def test_get_rick_roll_ssids_negative_returns_first():
    """get_rick_roll_ssids with negative index returns the first SSID."""
    assert get_rick_roll_ssids(-1) == EXPECTED_RICK_ROLL_SSIDS[0]


def test_get_rick_roll_ssids_out_of_range_returns_first():
    """get_rick_roll_ssids with index >= 8 returns the first SSID."""
    assert get_rick_roll_ssids(8) == EXPECTED_RICK_ROLL_SSIDS[0]
    assert get_rick_roll_ssids(100) == EXPECTED_RICK_ROLL_SSIDS[0]


def test_rick_roll_ssids_full_list_in_order():
    """Callers can obtain all eight Rick Roll SSIDs in order via the public list."""
    all_ssids = list(rick_roll_ssids)
    assert len(all_ssids) == 8
    assert all_ssids == EXPECTED_RICK_ROLL_SSIDS


def test_get_rick_roll_beacon_frames_returns_eight_packets():
    """get_rick_roll_beacon_frames returns a list of exactly 8 Scapy packets."""
    frames = get_rick_roll_beacon_frames()
    assert isinstance(frames, list)
    assert len(frames) == 8
    for pkt in frames:
        assert isinstance(pkt, scapy.packet.Packet)


def test_get_rick_roll_beacon_frames_ssids_in_order():
    """Each beacon frame has SSID IE matching the eight Rick Roll SSIDs in order."""
    frames = get_rick_roll_beacon_frames()
    assert len(frames) == 8
    for i, pkt in enumerate(frames):
        elt = pkt[Dot11Elt]
        assert elt.ID == 0  # SSID
        info = elt.info if isinstance(elt.info, bytes) else elt.info.encode("utf-8")
        expected_ssid_bytes = EXPECTED_RICK_ROLL_SSIDS[i].encode("utf-8")
        assert info == expected_ssid_bytes


def test_get_rick_roll_beacon_frames_structure():
    """Each returned packet has expected 802.11 beacon structure (Dot11, Dot11Beacon, Dot11Elt)."""
    frames = get_rick_roll_beacon_frames()
    for pkt in frames:
        assert RadioTap in pkt
        assert Dot11 in pkt
        assert Dot11Beacon in pkt
        assert Dot11Elt in pkt
        dot11 = pkt[Dot11]
        assert dot11.type == 0
        assert dot11.subtype == 8  # beacon
        assert dot11.addr1.lower() == "ff:ff:ff:ff:ff:ff"
        # BSSID (addr2/addr3) is random per frame when not provided
        assert dot11.addr2 == dot11.addr3


# --- is_rick_roll_beacon_running ---


@patch("core.wifi.config")
def test_is_rick_roll_beacon_running_no_process_returns_false_none(mock_config):
    """When no process is stored in config, is_rick_roll_beacon_running returns (False, None)."""
    mock_config.get_key.return_value = None
    assert is_rick_roll_beacon_running() == (False, None)


@patch("core.wifi.config")
def test_is_rick_roll_beacon_running_stored_pid_returns_true_pid(mock_config):
    """When a PID is stored in config, is_rick_roll_beacon_running returns (True, that pid)."""
    mock_config.get_key.return_value = 12345
    assert is_rick_roll_beacon_running() == (True, 12345)


@patch("core.wifi.config")
def test_is_rick_roll_beacon_running_config_raises_returns_false_none(mock_config):
    """When config.get_key raises, is_rick_roll_beacon_running returns (False, None) and does not raise."""
    mock_config.get_key.side_effect = RuntimeError("config error")
    result = is_rick_roll_beacon_running()
    assert result == (False, None)


# --- start_rick_roll_beacon ---


@patch("core.wifi.config")
def test_start_rick_roll_beacon_already_running_returns_none(mock_config):
    """When a process is already recorded, start_rick_roll_beacon returns None and does not start another."""
    mock_config.get_key.return_value = 999
    result = start_rick_roll_beacon()
    assert result is None
    mock_config.get_key.assert_called_once_with("running_processes", "rick_roll")
    mock_config.set_key.assert_not_called()


@patch("core.wifi.Process")
@patch("core.wifi.config")
def test_start_rick_roll_beacon_starts_and_stores_pid(mock_config, mock_process_cls):
    """When no process is running, start_rick_roll_beacon starts a process and stores its PID in config."""
    mock_config.get_key.return_value = None
    mock_proc = MagicMock()
    mock_proc.pid = 4242
    mock_process_cls.return_value = mock_proc

    result = start_rick_roll_beacon()

    assert result is mock_proc
    mock_process_cls.assert_called_once()
    mock_proc.start.assert_called_once()
    mock_config.set_key.assert_called_once_with("running_processes", "rick_roll", 4242)


# --- stop_rick_roll_beacon ---


@patch("core.wifi.config")
def test_stop_rick_roll_beacon_not_running_returns_false(mock_config):
    """When no process is recorded, stop_rick_roll_beacon returns False and does not call terminate."""
    mock_config.get_key.return_value = None
    result = stop_rick_roll_beacon()
    assert result is False
    mock_config.get_key.assert_called_once_with("running_processes", "rick_roll")
    mock_config.set_key.assert_not_called()


@patch("core.wifi.config")
def test_stop_rick_roll_beacon_running_terminates_and_returns_true(mock_config):
    """When a process is recorded, stop_rick_roll_beacon terminates it, clears config, and returns True."""
    mock_proc = MagicMock()
    mock_proc.pid = 4242
    mock_config.get_key.return_value = mock_proc

    result = stop_rick_roll_beacon()

    assert result is True
    mock_config.get_key.assert_called_with("running_processes", "rick_roll")
    mock_proc.terminate.assert_called_once()
    mock_config.set_key.assert_called_once_with("running_processes", "rick_roll", None)


@patch("core.wifi.config")
def test_stop_rick_roll_beacon_terminate_raises_returns_false(mock_config):
    """When terminate or config update fails, stop_rick_roll_beacon returns False and does not raise."""
    mock_proc = MagicMock()
    mock_proc.terminate.side_effect = OSError("kill failed")
    mock_config.get_key.return_value = mock_proc

    result = stop_rick_roll_beacon()

    assert result is False
