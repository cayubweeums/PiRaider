"""Tests for core.wifi Rick Roll Beacon: SSIDs and beacon frames."""

import pytest
import scapy.packet
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, RadioTap

from core.wifi import (
    rick_roll_ssids,
    get_rick_roll_ssids,
    get_rick_roll_beacon_frames,
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
