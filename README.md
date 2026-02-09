# PiRaider

Porting the amazing work by the team building the [ESP32 Marauder](https://github.com/justcallmekoko/ESP32Marauder) project to Python so it can run on normal hardware (e.g. Raspberry Pi, laptops) without ESP32 firmware level access.

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

Tools are grouped as in the ESP32 Marauder UI. Each section should contain links to the main files in the upstream repo that implement that tool.

- **WiFi**
  - Sniffers
    - [Probe Request Sniff](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Beacon Sniff](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Channel Analyzer](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Deauth Sniff](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Packet Count](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Packet Monitor](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [EAPOL/PMKID Scan](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Detect Pwnagotchi](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Detect Espressif](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Scan APs](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Raw Capture](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Station Sniff](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Signal Monitor](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Wardrive](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Station Wardrive](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [MAC Track](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [SAE Commit](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Detect Pineapple](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Detect MultiSSID](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Select probe SSIDs](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp)
  - Scanners
    - [Ping Scan](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [ARP Scan](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Port Scan All](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [SSH Scan](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Telnet Scan](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [DNS/HTTP/HTTPS/SMTP/RDP](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
  - Attacks
    - [Beacon Spam List](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Beacon Spam Random](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Evil Portal](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/EvilPortal.cpp)
    - [Rick Roll Beacon](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Probe Request Flood](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Deauth Flood](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [AP Clone Spam](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Karma](https://github.com/justcallmekoko/ESP32Marauder/wiki/karma)
    - [Bad Msg](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Sleep Attack](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [SAE Commit Flood](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Deauth Targeted](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
  - General
    - [Add SSID](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp) / [MenuFunctions](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp)
    - [Generate SSIDs](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Save/Load SSIDs](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/SDInterface.cpp), [WiFiScan](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Save/Load APs](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/SDInterface.cpp), [WiFiScan](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Clear SSIDs](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Clear APs](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Select APs](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp)
    - [Select Stations](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp)
    - [Select EP HTML File](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp), [EvilPortal](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/EvilPortal.cpp)
    - [View AP Info](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Set MACs](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Join WiFi](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Shutdown WiFi/BLE](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
- **Bluetooth**
  - Sniffers
    - [Bluetooth Analyzer](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Bluetooth Sniffer](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Flipper Sniff](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [AirTag Sniff](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [AirTag Monitor](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Bluetooth Wardrive](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Detect Card Skimmers](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Flock Sniff](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Flock Wardrive](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
  - Attacks
    - [Sour Apple](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [SwiftPair Spam](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Samsung BLE Spam](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Google BLE Spam](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Flipper BLE Spam](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [BT Spam All](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
    - [Spoof AirTag](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
- **Device**
  - Update Firmware
    - [Web Update](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/SDInterface.cpp) / MarauderOTA
    - [SD Update](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/SDInterface.cpp)
    - [ESP8266 Update](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp)
  - [Device Info](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp), [Display](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/Display.cpp)
  - [Settings](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/settings.cpp)
  - [GPS Data](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/GpsInterface.cpp)
  - [GPS Tracker](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/GpsInterface.cpp), [WiFiScan](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/WiFiScan.cpp)
  - [Reboot](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/CommandLine.cpp)
- **Bad USB**
  - [Test BadUSB](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/Keyboard.cpp)
  - [Run Ducky Script](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/Keyboard.cpp)

Menu and CLI wiring: [MenuFunctions.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/MenuFunctions.cpp), [CommandLine.cpp](https://github.com/justcallmekoko/ESP32Marauder/blob/master/esp32_marauder/CommandLine.cpp).
