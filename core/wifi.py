import os
import signal
import subprocess
import time
import logging
from multiprocessing import Process
from typing import Tuple

import scapy.packet
from scapy.all import ( Dot11,
                        Dot11Beacon,
                        Dot11Elt,
                        RadioTap,
                        sendp,
                        hexdump)

from core.beacon import build_beacon_frame
from core.config import config, get_key
from core.radio import configure_interface

log = logging.getLogger(__name__)

# TODO: Before running any prank or attack have a configure interface function that will use the logic in utils to ensure the 
#   interface selected in the config is in monitor mode and on a specific channel

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

def start_rick_roll_beacon() -> Process | None:
    """
    Start the Rick Roll Beacon Prank

    Args:
        None
    
    Returns:
        A Process object if the process was started successfully, None otherwise
    """
    if config.get_key("running_processes", "rick_roll") is not None:
        log.warning("Already a running Rick Roll Beacon cannot start another")
        return None
    process = Process(target=send_rick_roll_beacon)
    process.start()
    config.set_key("running_processes", "rick_roll", process.pid)
    log.info(f"Started Rick Roll Beacon with process ID {process.pid}")
    return process

def send_rick_roll_beacon() -> None:
    """
    Send the Rick Roll Beacon Prank

    ex python line: sendp(frame, iface=iface, inter=0.100, loop=10000)

    """
    
    # Grab frames to send
    frames = get_rick_roll_beacon_frames()

    iface = get_key("wifi_device")
    if not iface:
        log.error("WiFi device not set in config, unable to start rick roll prank")
        return

    if not configure_interface(iface):
        log.error(f"Failed to configure interface {iface}, unable to start rick roll prank")
        return

    while True:
        for beacon in frames:
            sendp(beacon, iface=iface)
            time.sleep(0.045)

def stop_rick_roll_beacon() -> bool:
    """
    Stop the Rick Roll Beacon Prank

    Args:
        None

    Returns:
        True if the prank was stopped successfully, False otherwise
    """
    pid = config.get_key("running_processes", "rick_roll")
    if pid is None:
        log.warning("No running Rick Roll Beacon to stop")
        return False
    try:
        # Config stores PID (int); terminate the process by PID
        if isinstance(pid, int):
            os.kill(pid, signal.SIGTERM)
        else:
            # Legacy: Process object
            pid.terminate()
        config.set_key("running_processes", "rick_roll", None)
        _pid = pid if isinstance(pid, int) else getattr(pid, "pid", None)
        log.info(f"Stopped Rick Roll Beacon (PID {_pid})")
        return True
    except ProcessLookupError:
        config.set_key("running_processes", "rick_roll", None)
        log.info("Rick Roll Beacon process already exited")
        return True
    except Exception as e:
        log.error(f"Failed to stop Rick Roll Beacon: {e}")
        return False

def is_rick_roll_beacon_running() -> Tuple[bool, int | None]:
    """
    Check if the Rick Roll Beacon is running

    Args:
        None
    
    Returns:
        A tuple of a boolean indicating if the Rick Roll Beacon is running and the process ID if it is running, None otherwise
    """
    running, pid = False, None
    try:
        pid = config.get_key("running_processes", "rick_roll")
        running = pid is not None
    except Exception as e:
        log.error(f"Failed to get Rick Roll Beacon process: {e}")
    return running, pid

#endregion