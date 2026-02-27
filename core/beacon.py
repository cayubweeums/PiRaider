"""Build 802.11 beacon frame bytes"""
"""
# TODO:
ensure setting up the interface does this:
❯ sudo ip link set wlan0 down
❯ sudo iw dev wlan0 set type monitor
❯ sudo ip link set wlan0 up
❯ sudo iw dev wlan0 set channel 6
"""


import os

from scapy.all import Dot11, Dot11Beacon, Dot11Elt, Raw, RadioTap, sendp
import scapy.packet

def build_beacon_frame(
    ssid: str,
    sender_mac: str,
    channel: int = 6, # default channel 6
) -> scapy.packet.Packet:
    """Build a single 802.11 beacon frame

    Args:
        ssid: SSID string (0–32 bytes; longer is truncated to 32 bytes).
        sender_mac: MAC address of the sender.
        channel: Optional channel (1–14). If set, appends Rates + DS IEs (same as ESP32 Marauder broadcastSetSSID).

    Returns:
        Full beacon frame.
    """
    ssid_bytes = ssid.encode("utf-8")
    if len(ssid_bytes) > 32:
        ssid_bytes = ssid_bytes[:32]

    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=sender_mac, addr3=sender_mac)

    # Open ESS (no privacy bit) with 1000 TU interval
    beacon = Dot11Beacon(beacon_interval=1000, cap=0x21)

    essid = Dot11Elt(ID='SSID', info=ssid_bytes, len=len(ssid_bytes))

    # Same basic supported rates ESP32 Marauder uses
    rates = Dot11Elt(ID="Rates", info=b"\x82\x84\x8b\x96\x24\x30\x48\x6c")

    # DS Parameter Set - tells clients were on this channel
    ds = Dot11Elt(ID="DSset", info=bytes([channel]))

    return RadioTap()/dot11/beacon/essid/rates/ds