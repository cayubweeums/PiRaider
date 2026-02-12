import re
import subprocess
import logging
from rich.traceback import install
from rich import pretty
from rich import print

from utils import parse_indented_output

log = logging.getLogger(__name__)

install()
pretty.install()

'''
# Frequency ranges (MHz) and their band labels
'''
BAND_RANGES = [
    (2400, 2500, '2.4'),   # 2.4 GHz (ch 1–14)
    (5150, 5925, '5'),     # 5 GHz (UNII-1 through ch 165)
    (5925, 7125, '6'),     # 6 GHz (WiFi 6E)
]

#region Helpers

def freq_mhz_from_item(item: str) -> float | None:
    """Extract MHz from strings like '2412.0 MHz [1] (30.0 dBm)'."""
    m = re.search(r'(\d+\.?\d*)\s*MHz', item)
    return float(m.group(1)) if m else None

def band_from_mhz(mhz: float) -> str | None:
    """Map MHz to band label ('2.4', '5', '6') or None."""
    for low, high, label in BAND_RANGES:
        if low <= mhz <= high:
            return label
    return None

#endregion

#region Radio functs

def grab_all_wireless_interfaces() -> dict:
    """
    Grabs all wireless interfaces, pulls relevant info for them like state and capabilities
    
    Returns:
        dict: A dictionary of all wireless interfaces and their relevant info
    """
    relevant_device_info = {}

    # Grab all wireless interfaces
    log.info("Querying all wireless interfaces")
    result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
    interfaces = []
    for lines in result.stdout.split('\n'):
        if lines.startswith('phy#'):
            key = lines.replace('#', '').strip()
        for line in lines.split('\t'):
            if line.startswith('Interface'):
                current_interface = {
                    'physical_id': key,
                    'device_id': line.split(' ')[1].strip()
                }
                interfaces.append(current_interface)
    log.debug(f"Found Interfaces: {interfaces}")

    for interface in interfaces:
        phy_info = parse_indented_output(subprocess.run(['iw', 'phy', f'{interface["physical_id"]}', 'info'], capture_output=True, text=True).stdout)
        for physical_id in phy_info:
            
            # Check if monitor mode is supported
            if 'monitor' in phy_info[physical_id]['Supported interface modes']['_items']:
                log.info(f"Monitor mode supported: {interface['device_id']}")

            # Grab all supported frequencies via their bands
            supported_frequencies = {}
            for band_key, band_data in phy_info[physical_id].items():
                if band_key.startswith('Band'):

                    log.debug(f"Found band: {band_key}")

                    log.debug(f"Frequencies found for band {band_key}: {band_data['Frequencies']['_items']}")

                    current_supported_frequencies = []
                    for frequency in band_data['Frequencies']['_items']:
                        current_supported_frequencies.append(freq_mhz_from_item(frequency))
                    
                    log.debug(f"{band_key}: Likely capability: {band_from_mhz((sum(current_supported_frequencies)) / len(current_supported_frequencies))}")
                    
                    supported_frequencies[band_key] = band_from_mhz((sum(current_supported_frequencies)) / len(current_supported_frequencies))

            # Check if the interface is being used already
            interface_up = False
            result = subprocess.run(['ip', 'link', 'show', interface['device_id']], capture_output=True, text=True)
            if 'state UP' in result.stdout:
                
                log.debug(f"Interface {interface['device_id']} is up")
                
                interface_up = True
            else:
                
                log.debug(f"Interface {interface['device_id']} is down")
                
                interface_up = False 
            
            relevant_device_info[interface['device_id']] = {
                'physical_id': interface['physical_id'],
                'device_id': interface['device_id'],
                'interface_up': interface_up,
                'band_capability': supported_frequencies
            }
            log.info(f"Relevant device info: {relevant_device_info}")

def grab_all_bluetooth_interfaces() -> dict:
    """
    Grabs all bluetooth interfaces, pulls relevant info for them like state and capabilities
    
    Returns:
        dict: A dictionary of all bluetooth interfaces and their relevant info
    """
    relevant_device_info = {}
    # Have to use the mac address to index the controllers via bluetoothctl show <mac_address>
    result = subprocess.run(['bluetoothctl', 'list'], capture_output=True, text=True)
    if result.returncode != 0:
        log.error(f"Failed to list bluetooth controllers: {result.stderr}")
        return relevant_device_info
    else:
        for controller in result.stdout.split('\n'):
            for segment in controller.split(' '):
                if ':' in segment:
                    log.info(f"Found bluetooth controller: {controller}")

                    bluetooth_controller_info = parse_indented_output(
                        subprocess.run(['bluetoothctl', 'show', segment], capture_output=True, text=True).stdout,
                        accumulate_repeated_keys=True,
                    )
                    log.debug(bluetooth_controller_info)

    return relevant_device_info

#endregion