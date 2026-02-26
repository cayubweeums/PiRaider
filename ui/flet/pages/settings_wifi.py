import asyncio
import logging

import flet as ft

from core.radio import grab_all_wireless_interfaces
from core.config import set_key

log = logging.getLogger(__name__)

class Wifi_Settings_Content:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dropdown_options = self._get_wifi_dropdown_options()
        self.dropdown = ft.Dropdown(
            width=220,
            options=self.dropdown_options,
        )
        self.floating_action_button = ft.FloatingActionButton(content="Save", on_click=lambda e: asyncio.create_task(self._save_wifi_config(e)))

    def get_content(self):
        return [
            ft.AppBar(
                title=ft.Text("Wifi Settings")
            ),
            ft.Text("Select a WiFi interface to use:", size=16),
            self.dropdown,
            self.floating_action_button,
        ]


    def _get_wifi_dropdown_options(self):
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

    async def _save_wifi_config(self, event: ft.ControlEvent | None = None):
        if event is not None:
            log.info(f"Saving WiFi config: {self.dropdown.value}")
            set_key("wifi_device", self.dropdown.value)
            log.info(f"WiFi device saved: {self.dropdown.value}")
        else:
            log.info("Saving WiFi config")