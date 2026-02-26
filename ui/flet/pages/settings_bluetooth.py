import asyncio
import logging

import flet as ft

from core.radio import grab_all_bluetooth_interfaces
from core.config import set_key

log = logging.getLogger(__name__)

class Bluetooth_Settings_Content:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dropdown_options = self._get_bluetooth_dropdown_options()
        self.dropdown = ft.Dropdown(
            width=220,
            options=self.dropdown_options,
        )
        self.floating_action_button = ft.FloatingActionButton(content="Save", on_click=lambda e: asyncio.create_task(self._save_bluetooth_config(e)))


    def get_content(self):
        return [
            ft.AppBar(
                title=ft.Text("Bluetooth Settings")
            ),
            ft.Text("Select a Bluetooth controller to use:", size=16),
            self.dropdown,
            self.floating_action_button,
        ]

    def _get_bluetooth_dropdown_options(self):
        bluetooth_controllers = grab_all_bluetooth_interfaces()
        options = []

        for controller in bluetooth_controllers:
            options.append(ft.DropdownOption(key=bluetooth_controllers[controller]['controller_mac'], text=f"{bluetooth_controllers[controller]['controller_name']} - {bluetooth_controllers[controller]['controller_mac']} - Powered: {bluetooth_controllers[controller]['powered']} - Discoverable: {bluetooth_controllers[controller]['discoverable']}"))

        return options

    async def _save_bluetooth_config(self, event: ft.ControlEvent | None = None):
        if event is not None:
            log.info(f"Saving Bluetooth config: {self.dropdown.value}")
            set_key("bluetooth_device", self.dropdown.value)
            log.info(f"Bluetooth device saved: {self.dropdown.value}")
        else:
            log.info("Saving Bluetooth config")