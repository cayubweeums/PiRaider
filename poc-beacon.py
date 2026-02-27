"""
Below currently works on phone but didn't show on my windows machine
"""

from scapy.all import ( Dot11,
                        Dot11Beacon,
                        Dot11Elt,
                        RadioTap,
                        sendp,
                        hexdump)

SSID = "pee pee poo poo"
iface = "wlp198s0f3u1i3"
sender = "00:c0:ca:b7:e9:b8"
channel = 6

dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=sender, addr3=sender) # can change addr2 and addr3 to bssid maybe?

# Open ESS (no privacy bit) with 1000 TU interval
beacon = Dot11Beacon(beacon_interval=1000, cap=0x21)

essid = Dot11Elt(ID='SSID',info=SSID, len=len(SSID))

# Same basic supported rates ESP32 Marauder uses
rates = Dot11Elt(ID="Rates", info=b"\x82\x84\x8b\x96\x24\x30\x48\x6c")

# DS Parameter Set - tells clients were on this channel
ds = Dot11Elt(ID="DSset", info=bytes([channel]))

frame = RadioTap()/dot11/beacon/essid/rates/ds

sendp(frame, iface=iface, inter=0.100, loop=10000)