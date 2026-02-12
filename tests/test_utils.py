"""Tests for core.utils.parse_indented_output."""

import pytest

from core.utils import parse_indented_output


# bluetoothctl show output examples
BLUETOOTHCTL_SHOW_1 = """
Controller AA:BB:CC:DD:EE:01 (public)
	Manufacturer: 0x0046 (70)
	Version: 0x0c (12)
	Name: device-a #2
	Alias: device-a #2
	Class: 0x007c0000 (8126464)
	Powered: yes
	PowerState: on
	Discoverable: no
	DiscoverableTimeout: 0x000000b4 (180)
	Pairable: yes
	UUID: Message Notification Se.. (00001133-0000-1000-8000-00805f9b34fb)
	UUID: A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)
	UUID: OBEX Object Push          (00001105-0000-1000-8000-00805f9b34fb)
	UUID: Vendor specific           (03b80e5a-ede8-4b33-a751-6ce34ec4c700)
	UUID: Message Access Server     (00001132-0000-1000-8000-00805f9b34fb)
	UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
	UUID: IrMC Sync                 (00001104-0000-1000-8000-00805f9b34fb)
	UUID: Vendor specific           (00005005-0000-1000-8000-00805f9b34fb)
	UUID: A/V Remote Control Target (0000110c-0000-1000-8000-00805f9b34fb)
	UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
	UUID: Phonebook Access Server   (0000112f-0000-1000-8000-00805f9b34fb)
	UUID: Device Information        (0000180a-0000-1000-8000-00805f9b34fb)
	UUID: Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)
	UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
	UUID: Phonebook Access Client   (0000112e-0000-1000-8000-00805f9b34fb)
	UUID: Handsfree Audio Gateway   (0000111f-0000-1000-8000-00805f9b34fb)
	UUID: Audio Source              (0000110a-0000-1000-8000-00805f9b34fb)
	UUID: Vendor specific           (185f3df4-3268-4e3f-9fca-d4d5059915bd)
	UUID: OBEX File Transfer        (00001106-0000-1000-8000-00805f9b34fb)
	UUID: Handsfree                 (0000111e-0000-1000-8000-00805f9b34fb)
	Modalias: usb:v1D6Bp0246d0555
	Discovering: no
	Roles: central
	Roles: peripheral
Advertising Features:
	ActiveInstances: 0x00 (0)
	SupportedInstances: 0x14 (20)
	SupportedIncludes: tx-power
	SupportedIncludes: appearance
	SupportedIncludes: local-name
	SupportedSecondaryChannels: 1M
	SupportedSecondaryChannels: 2M
	SupportedSecondaryChannels: Coded
	SupportedCapabilities.MinTxPower: 0xfffffff2 (-14)
	SupportedCapabilities.MaxTxPower: 0x000d (13)
	SupportedCapabilities.MaxAdvLen: 0xfb (251)
	SupportedCapabilities.MaxScnRspLen: 0xfb (251)
	SupportedFeatures: CanSetTxPower
	SupportedFeatures: HardwareOffload
"""

BLUETOOTHCTL_SHOW_2 = """
Controller AA:BB:CC:DD:EE:02 (public)
	Manufacturer: 0x0002 (2)
	Version: 0x0d (13)
	Name: device-b
	Alias: device-b
	Class: 0x007c0000 (8126464)
	Powered: yes
	PowerState: on
	Discoverable: no
	DiscoverableTimeout: 0x000000b4 (180)
	Pairable: yes
	UUID: Message Notification Se.. (00001133-0000-1000-8000-00805f9b34fb)
	UUID: A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)
	UUID: Vendor specific           (03b80e5a-ede8-4b33-a751-6ce34ec4c700)
	UUID: OBEX Object Push          (00001105-0000-1000-8000-00805f9b34fb)
	UUID: Message Access Server     (00001132-0000-1000-8000-00805f9b34fb)
	UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
	UUID: IrMC Sync                 (00001104-0000-1000-8000-00805f9b34fb)
	UUID: Vendor specific           (00005005-0000-1000-8000-00805f9b34fb)
	UUID: A/V Remote Control Target (0000110c-0000-1000-8000-00805f9b34fb)
	UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
	UUID: Phonebook Access Server   (0000112f-0000-1000-8000-00805f9b34fb)
	UUID: Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)
	UUID: Device Information        (0000180a-0000-1000-8000-00805f9b34fb)
	UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
	UUID: Phonebook Access Client   (0000112e-0000-1000-8000-00805f9b34fb)
	UUID: Handsfree Audio Gateway   (0000111f-0000-1000-8000-00805f9b34fb)
	UUID: Audio Source              (0000110a-0000-1000-8000-00805f9b34fb)
	UUID: Vendor specific           (185f3df4-3268-4e3f-9fca-d4d5059915bd)
	UUID: OBEX File Transfer        (00001106-0000-1000-8000-00805f9b34fb)
	UUID: Handsfree                 (0000111e-0000-1000-8000-00805f9b34fb)
	Modalias: usb:v1D6Bp0246d0555
	Discovering: yes
	Roles: central
	Roles: peripheral
Advertising Features:
	ActiveInstances: 0x00 (0)
	SupportedInstances: 0x0c (12)
	SupportedIncludes: tx-power
	SupportedIncludes: appearance
	SupportedIncludes: local-name
	SupportedSecondaryChannels: 1M
	SupportedSecondaryChannels: 2M
	SupportedSecondaryChannels: Coded
	SupportedCapabilities.MinTxPower: 0xffffffde (-34)
	SupportedCapabilities.MaxTxPower: 0x0007 (7)
	SupportedCapabilities.MaxAdvLen: 0xfb (251)
	SupportedCapabilities.MaxScnRspLen: 0xfb (251)
	SupportedFeatures: CanSetTxPower
	SupportedFeatures: HardwareOffload
"""

# iw phy output excerpt
IW_PHY_INFO = """
Wiphy phy4
	wiphy index: 4
	max # scan SSIDs: 4
	max scan IEs length: 482 bytes
	max # sched scan SSIDs: 10
	max # match sets: 16
	Retry short limit: 7
	Retry long limit: 4
	Coverage class: 0 (up to 0m)
	Device supports AP-side u-APSD.
	Device supports T-DLS.
	Supported Ciphers:
		* WEP40 (00-0f-ac:1)
		* WEP104 (00-0f-ac:5)
		* TKIP (00-0f-ac:2)
		* CCMP-128 (00-0f-ac:4)
		* CCMP-256 (00-0f-ac:10)
		* GCMP-128 (00-0f-ac:8)
		* GCMP-256 (00-0f-ac:9)
		* CMAC (00-0f-ac:6)
		* CMAC-256 (00-0f-ac:13)
		* GMAC-128 (00-0f-ac:11)
		* GMAC-256 (00-0f-ac:12)
	Available Antennas: TX 0x3 RX 0x3
	Configured Antennas: TX 0x3 RX 0x3
	Supported interface modes:
		* managed
		* AP
		* AP/VLAN
		* monitor
		* P2P-client
		* P2P-GO
		* P2P-device
	Band 1:
		Capabilities: 0x9ff
			RX LDPC
			HT20/HT40
			SM Power Save disabled
			RX Greenfield
			RX HT20 SGI
			RX HT40 SGI
			TX STBC
			RX STBC 1-stream
			Max AMSDU length: 7935 bytes
			No DSSS/CCK HT40
		Maximum RX AMPDU length 65535 bytes (exponent: 0x003)
		Minimum RX AMPDU time spacing: No restriction (0x00)
		HT TX/RX MCS rate indexes supported: 0-15
		Frequencies:
			* 2412.0 MHz [1] (30.0 dBm)
			* 2417.0 MHz [2] (30.0 dBm)
			* 2437.0 MHz [6] (30.0 dBm)
			* 2467.0 MHz [12] (disabled)
			* 2484.0 MHz [14] (disabled)
	Band 2:
		Capabilities: 0x9ff
			RX LDPC
			HT20/HT40
		Frequencies:
			* 5180.0 MHz [36] (23.0 dBm)
			* 5200.0 MHz [40] (23.0 dBm)
			* 5745.0 MHz [149] (30.0 dBm)
			* 5825.0 MHz [165] (30.0 dBm)
"""

def test_iw_phy_parsing_unchanged():
    """iw phy output parsing must remain correct (no accumulate_repeated_keys)."""
    result = parse_indented_output(IW_PHY_INFO)

    assert "Wiphy phy4" in result
    inner = result["Wiphy phy4"]

    assert inner["wiphy index"] == "4"
    assert inner["max # scan SSIDs"] == "4"
    assert inner["max scan IEs length"] == "482 bytes"

    assert "Supported interface modes" in inner
    modes = inner["Supported interface modes"]
    assert "_items" in modes
    assert "managed" in modes["_items"]
    assert "monitor" in modes["_items"]
    assert "AP" in modes["_items"]
    assert "P2P-device" in modes["_items"]

    assert "Supported Ciphers" in inner
    assert "WEP40 (00-0f-ac:1)" in inner["Supported Ciphers"]["_items"]

    assert "Band 1" in inner
    band1 = inner["Band 1"]
    assert band1["Capabilities"] == "0x9ff"
    assert "2412.0 MHz" in str(band1["Frequencies"]["_items"])
    assert "RX LDPC" in band1  # Capability sub-items under Band 1

    assert "Band 2" in inner
    band2 = inner["Band 2"]
    assert "5180.0 MHz" in str(band2["Frequencies"]["_items"])


def test_bluetoothctl_controller_line():
    """Controller line parsed as single key with full MAC."""
    result = parse_indented_output(BLUETOOTHCTL_SHOW_1, accumulate_repeated_keys=True)
    assert result["Controller"] == "AA:BB:CC:DD:EE:01 (public)"

    result2 = parse_indented_output(BLUETOOTHCTL_SHOW_2, accumulate_repeated_keys=True)
    assert result2["Controller"] == "AA:BB:CC:DD:EE:02 (public)"


def test_bluetoothctl_repeated_keys():
    """Repeated keys (UUID, Roles, SupportedIncludes, etc.) preserved as lists."""
    result = parse_indented_output(BLUETOOTHCTL_SHOW_1, accumulate_repeated_keys=True)

    assert len(result["UUID"]) == 20
    assert result["UUID"][0] == "Message Notification Se.. (00001133-0000-1000-8000-00805f9b34fb)"
    assert result["UUID"][-1] == "Handsfree                 (0000111e-0000-1000-8000-00805f9b34fb)"
    assert result["Roles"] == ["central", "peripheral"]

    adv = result["Advertising Features"]
    assert adv["SupportedIncludes"] == ["tx-power", "appearance", "local-name"]
    assert adv["SupportedSecondaryChannels"] == ["1M", "2M", "Coded"]
    assert adv["SupportedFeatures"] == ["CanSetTxPower", "HardwareOffload"]


def test_bluetoothctl_advertising_features_nested():
    """Advertising Features subsection and all sub-keys present."""
    result = parse_indented_output(BLUETOOTHCTL_SHOW_1, accumulate_repeated_keys=True)

    adv = result["Advertising Features"]
    assert adv["ActiveInstances"] == "0x00 (0)"
    assert adv["SupportedInstances"] == "0x14 (20)"
    assert adv["SupportedCapabilities.MinTxPower"] == "0xfffffff2 (-14)"
    assert adv["SupportedCapabilities.MaxTxPower"] == "0x000d (13)"
    assert adv["SupportedCapabilities.MaxAdvLen"] == "0xfb (251)"
    assert adv["SupportedCapabilities.MaxScnRspLen"] == "0xfb (251)"


def test_bluetoothctl_second_controller():
    """Second controller (different SupportedInstances) parses correctly."""
    result = parse_indented_output(BLUETOOTHCTL_SHOW_2, accumulate_repeated_keys=True)

    assert result["Name"] == "device-b"
    assert result["Discovering"] == "yes"
    assert result["Advertising Features"]["SupportedInstances"] == "0x0c (12)"
    assert result["Advertising Features"]["SupportedCapabilities.MinTxPower"] == "0xffffffde (-34)"


def test_bluetoothctl_without_accumulate_single_values():
    """Without accumulate_repeated_keys, repeated keys overwrite (backward compat)."""
    result = parse_indented_output(BLUETOOTHCTL_SHOW_1, accumulate_repeated_keys=False)

    assert result["Controller"] == "AA:BB:CC:DD:EE:01 (public)"
    assert isinstance(result["UUID"], str)
    assert isinstance(result["Roles"], str)


def test_controller_regex_mac_with_leading_zero():
    """Controller MAC with leading zero (00:...) parses correctly."""
    text = "Controller 00:11:22:33:44:55 (public)"
    result = parse_indented_output(text, accumulate_repeated_keys=True)
    assert result["Controller"] == "00:11:22:33:44:55 (public)"
