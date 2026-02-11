# PiRaider

Porting the amazing work by the team building the [ESP32 Marauder](https://github.com/justcallmekoko/ESP32Marauder) project to Python so it can run on normal hardware (e.g. Raspberry Pi, laptops) without ESP32 firmware level access.

## Requirements
- If booting from usb:
    - Add `usb_max_current_enable=1` to your `/boot/firmware/config.txt` so you don't get the warning message

## UI 'Vision' Board
- https://www.reddit.com/r/outrun/comments/134m0u2/build_an_aesthetic_world_fictional_ui/

## Fun git visualization command
```bash
gource --camera-mode track  --file-filter "__pycache__|\.py[cod]$|__init__\.py$" --viewport 1920x1080 -a 1 -s 1 --output-ppm-stream - | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i -   -vcodec libx264 -preset ultrafast -pix_fmt yuv420p output.mp4
```

## Porting plan

ESP32 Marauder is a WiFi/Bluetooth tool suite that runs as firmware on the ESP32. The goal here is to bring the same kinds of tools and workflows to Python so they run on a Pi or laptop—using an external WiFi/BT dongle and Python or subprocess calls to existing tools where that makes sense.

### Step 1: Single usable tool version (PoC)

Get one path working end-to-end, then build on it.

**UIs.** We’ll have two ways to use the app: Flet (one library for both web and native), and a TUI (Rich) for the terminal. One entrypoint, `main.py`, with flags: default runs the Flet app, something like `--tui` runs the TUI. Layout: `main.py` at the root; Flet under something like `ui/flet/`; TUI under `ui/tui/`; shared logic in `core/`. The core only exposes functions and data with no UI code in there. For the PoC, both UIs just need to show a simple home screen with the same top-level buckets as the Marauder project (WiFi, Bluetooth, Device) as placeholders.

**Radios.** To make this project as easy to use as possible, we will automatically detect and configure our interfaces and list their capabilities. Which wifi devices can use monitor mode, which wifi devices can hit 2.4, 5, and 6 Ghz respectively. The same for Bluetooth: detect the adapter and whether it’s up and usable for scanning. A small module (e.g. `core/radio.py`) can return these values/checks; both UIs then show “radios ready” or a clear “not available” instead of failing later in a confusing way.

**Dependencies.** Use Poetry for the project, no global pip install for project deps. Flet and Rich for the UIs. Whatever we need for radio detection.

**First real tool.** We will be working towards the initial tool built and working to be the Rick Roll Beacon. This one should help get the project's foundation built out as this not only requires porting some of the wifi scan cpp file which is a critial piece, but also other aspects like our repos file structure. It will also help us in determining if python is up for this task or not.

**Tests.** Set up a pytest suite under `tests/`. Unit tests for things that don’t need hardware (e.g. parsing scan output, or radio detection from mocked/fake data). The idea is that every new tool adds tests. Running `poetry run pytest` will be the one way to run the suite.

### After the PoC: porting the rest

Tackle passive/sniffing/scanning tools first (e.g beacon sniff, probe sniff, station scan, ping/ARP/port scan), then attacks (deauth, beacon spam, evil portal, etc.), then Bluetooth (BLE scan, then BLE spam).

---

## Tool structure (UI → upstream code)

Tools are grouped as in the ESP32 Marauder UI. Implementation status is tracked per tool.

**Status legend:** ✅ Implemented · ◐ Partially implemented · ○ Not implemented · ⊘ Not possible (ESP32-only or no equivalent)

### WiFi

| Tool | Status | Reference |
|------|--------|-----------|
| *Sniffers* | | |
| Probe Request Sniff | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Beacon Sniff | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Channel Analyzer | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Deauth Sniff | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Packet Count | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Packet Monitor | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| EAPOL/PMKID Scan | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Detect Pwnagotchi | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Detect Espressif | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Scan APs | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Raw Capture | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Station Sniff | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Signal Monitor | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Wardrive | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Station Wardrive | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| MAC Track | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| SAE Commit | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Detect Pineapple | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Detect MultiSSID | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Select probe SSIDs | ○ | [MenuFunctions.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp) |
| *Scanners* | | |
| Ping Scan | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| ARP Scan | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Port Scan All | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| SSH Scan | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Telnet Scan | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| DNS/HTTP/HTTPS/SMTP/RDP | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| *Attacks* | | |
| Beacon Spam List | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Beacon Spam Random | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Evil Portal | ○ | [EvilPortal.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/EvilPortal.cpp) |
| Rick Roll Beacon | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Probe Request Flood | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Deauth Flood | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| AP Clone Spam | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Karma | ○ | [karma (wiki)](https://github.com/justcallmekoko/ESP32Marauder/wiki/karma) |
| Bad Msg | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Sleep Attack | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| SAE Commit Flood | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Deauth Targeted | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| *General* | | |
| Add SSID | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp), [MenuFunctions.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp) |
| Generate SSIDs | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Save/Load SSIDs | ○ | [SDInterface.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/SDInterface.cpp), [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Save/Load APs | ○ | [SDInterface.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/SDInterface.cpp), [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Clear SSIDs | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Clear APs | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Select APs | ○ | [MenuFunctions.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp) |
| Select Stations | ○ | [MenuFunctions.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp) |
| Select EP HTML File | ○ | [MenuFunctions.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp), [EvilPortal.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/EvilPortal.cpp) |
| View AP Info | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Set MACs | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Join WiFi | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Shutdown WiFi/BLE | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |

### Bluetooth

| Tool | Status | Reference |
|------|--------|-----------|
| *Sniffers* | | |
| Bluetooth Analyzer | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Bluetooth Sniffer | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Flipper Sniff | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| AirTag Sniff | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| AirTag Monitor | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Bluetooth Wardrive | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Detect Card Skimmers | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Flock Sniff | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Flock Wardrive | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| *Attacks* | | |
| Sour Apple | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| SwiftPair Spam | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Samsung BLE Spam | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Google BLE Spam | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Flipper BLE Spam | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| BT Spam All | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Spoof AirTag | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |

### Device

| Tool | Status | Reference |
|------|--------|-----------|
| *Update Firmware* | | |
| Web Update | ○ | [SDInterface.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/SDInterface.cpp) / MarauderOTA |
| SD Update | ○ | [SDInterface.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/SDInterface.cpp) |
| ESP8266 Update | ○ | [MenuFunctions.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp) |
| Device Info | ○ | [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp), [Display.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/Display.cpp) |
| Settings | ○ | [settings.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/settings.cpp) |
| GPS Data | ○ | [GpsInterface.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/GpsInterface.cpp) |
| GPS Tracker | ○ | [GpsInterface.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/GpsInterface.cpp), [WiFiScan.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) |
| Reboot | ○ | [CommandLine.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/CommandLine.cpp) |
| Menu and CLI wiring | ○ | [MenuFunctions.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp), [CommandLine.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/CommandLine.cpp) |

### Bad USB

| Tool | Status | Reference |
|------|--------|-----------|
| Test BadUSB | ○ | [Keyboard.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/Keyboard.cpp) |
| Run Ducky Script | ○ | [Keyboard.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/Keyboard.cpp) |
