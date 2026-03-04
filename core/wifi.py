import os

import scapy.packet

from core.beacon import build_beacon_frame



#region Rick Roll Beacon
"""
Rick Roll Beacon Prank Logic
"""

rick_roll_ssids = [
    "01 Never gonna give you up",
    "02 Never gonna let you down",
    "03 Never gonna run around",
    "04 and desert you",
    "05 Never gonna make you cry",
    "06 Never gonna say goodbye",
    "07 Never gonna tell a lie",
    "08 and hurt you"
]

def get_rick_roll_ssids(index: int = None) -> str:
    """
    Get the Rick Roll SSIDs

    Args:
        index: The index of the SSID to get. If None, return the first SSID.
    
    Returns:
        A specific SSID per the index provided
    """
    if index is None or index < 0 or index >= len(rick_roll_ssids):
        return rick_roll_ssids[0]
    return rick_roll_ssids[index]

def get_rick_roll_beacon_frames() -> list[scapy.packet.Packet]:
    """
    Get the Rick Roll Beacon frames list of scapy packets

    Args:
        None
    
    Returns:
        A list of Beacon frames scapy packets.
    """
    return [build_beacon_frame(ssid=ssid) for ssid in rick_roll_ssids]

#endregion