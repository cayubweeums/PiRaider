import asyncio
import logging

import flet as ft

from core.radio import grab_all_wireless_interfaces

log = logging.getLogger(__name__)

def settings_wifi_page(page: ft.Page):
    return [
        ft.AppBar(
            title=ft.Text("Wifi Settings")
        ),
        ft.Text("Select a WiFi interface to use:", size=16),
        ft.Dropdown(
            width=220,
            options=_get_wifi_dropdown_options(),
        )
    ]


def _get_wifi_dropdown_options():
    wifi_interfaces = grab_all_wireless_interfaces()
    supported_bands_text = ""
    options = []

    for interface in wifi_interfaces:
        log.debug(f"Interface: {interface}")
        
        if bool(wifi_interfaces[interface]['interface_up']):
            status = "Up"
        else:
            status = "Down"
        if bool(wifi_interfaces[interface]['monitor_mode_supported']):
            monitor_mode = "Yes"
        else:
            monitor_mode = "No"
        for band in wifi_interfaces[interface]['band_capability']:
            supported_bands_text += f"{wifi_interfaces[interface]['band_capability'][band]} GHz, "
        options.append(ft.DropdownOption(key=wifi_interfaces[interface]['device_id'], text=f"{wifi_interfaces[interface]['device_id']} - {status} - mon mode: {monitor_mode} - {supported_bands_text}"))

    return options