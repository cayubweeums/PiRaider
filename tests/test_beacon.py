"""Tests for core.beacon.build_beacon_frame."""

import pytest
import scapy.packet
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, RadioTap

from core.beacon import build_beacon_frame


def test_build_beacon_frame_returns_scapy_packet():
    """Return value is a Scapy Packet (e.g. for bytes(packet) or layer access)."""
    pkt = build_beacon_frame(ssid="Test", sender_mac="00:11:22:33:44:55")
    assert isinstance(pkt, scapy.packet.Packet)


def test_build_beacon_frame_structure_fc_da_sa_bssid_ssid_ie():
    """Frame has beacon subtype, DA broadcast, SA/BSSID set, SSID IE present with requested SSID."""
    ssid = "MyAP"
    sender = "aa:bb:cc:dd:ee:ff"
    pkt = build_beacon_frame(ssid=ssid, sender_mac=sender)

    assert RadioTap in pkt
    assert Dot11 in pkt
    assert Dot11Beacon in pkt
    dot11 = pkt[Dot11]
    assert dot11.type == 0
    assert dot11.subtype == 8  # beacon
    assert dot11.addr1.lower() == "ff:ff:ff:ff:ff:ff"
    assert dot11.addr2.lower() == sender.lower()
    assert dot11.addr3.lower() == sender.lower()

    # First Dot11Elt is SSID
    elt = pkt[Dot11Elt]
    assert elt.ID == 0  # SSID
    info = elt.info if isinstance(elt.info, bytes) else elt.info.encode("utf-8")
    assert info == ssid.encode("utf-8")


def test_build_beacon_frame_ssid_empty():
    """Empty SSID (0 bytes) is supported."""
    pkt = build_beacon_frame(ssid="", sender_mac="00:00:00:00:00:01")
    elt = pkt[Dot11Elt]
    assert elt.ID == 0
    assert elt.len == 0
    assert (elt.info if isinstance(elt.info, bytes) else elt.info.encode("utf-8")) == b""


def test_build_beacon_frame_ssid_one_byte():
    """SSID of length 1 is supported."""
    pkt = build_beacon_frame(ssid="x", sender_mac="00:00:00:00:00:02")
    elt = pkt[Dot11Elt]
    assert elt.len == 1
    info = elt.info if isinstance(elt.info, bytes) else elt.info.encode("utf-8")
    assert info == b"x"


def test_build_beacon_frame_ssid_32_bytes():
    """SSID of length 32 bytes is supported."""
    ssid_32 = "a" * 32
    pkt = build_beacon_frame(ssid=ssid_32, sender_mac="00:00:00:00:00:03")
    elt = pkt[Dot11Elt]
    assert elt.len == 32
    info = elt.info if isinstance(elt.info, bytes) else elt.info.encode("utf-8")
    assert info == ssid_32.encode("utf-8")


def test_build_beacon_frame_ssid_longer_than_32_bytes_truncated():
    """SSID longer than 32 bytes is truncated to 32 bytes (802.11 max)."""
    ssid_long = "a" * 33
    pkt = build_beacon_frame(ssid=ssid_long, sender_mac="00:00:00:00:00:04")
    elt = pkt[Dot11Elt]
    assert elt.len == 32
    info = elt.info if isinstance(elt.info, bytes) else elt.info.encode("utf-8")
    assert info == ("a" * 32).encode("utf-8")


def test_build_beacon_frame_sa_and_bssid_equal_when_sender_mac_given():
    """SA (addr2) and BSSID (addr3) are set and equal when sender_mac is given."""
    sender = "ca:fe:ba:be:00:11"
    pkt = build_beacon_frame(ssid="SameBSSID", sender_mac=sender)
    dot11 = pkt[Dot11]
    assert dot11.addr2 == dot11.addr3
    assert dot11.addr2.lower() == sender.lower()


def test_build_beacon_frame_random_sender_mac_when_none():
    """When sender_mac is None, a random MAC is used; SA and BSSID are equal and valid."""
    pkt = build_beacon_frame(ssid="RickRoll")
    dot11 = pkt[Dot11]
    assert dot11.addr2 == dot11.addr3
    # Format xx:xx:xx:xx:xx:xx (6 hex bytes)
    mac = dot11.addr2
    parts = mac.split(":")
    assert len(parts) == 6
    for p in parts:
        assert len(p) == 2
        int(p, 16)  # valid hex


def test_build_beacon_frame_serializable_to_bytes():
    """Packet can be serialized to bytes (e.g. for injection); no UI or transmission."""
    pkt = build_beacon_frame(ssid="Serial", sender_mac="de:ad:be:ef:00:00")
    raw = bytes(pkt)
    assert isinstance(raw, bytes)
    assert len(raw) > 0
