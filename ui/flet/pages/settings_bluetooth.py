import asyncio
import logging

import flet as ft

from core.radio import grab_all_bluetooth_interfaces

log = logging.getLogger(__name__)

def settings_bluetooth_page(page: ft.Page):
    bluetooth_controllers = grab_all_bluetooth_interfaces()
    log.info(f"Bluetooth controllers: {bluetooth_controllers}")
    return [
        ft.AppBar(
            title=ft.Text("Bluetooth Settings")
        ),
        ft.Text("Select a Bluetooth controller to use:", size=16),
        ft.Dropdown(
            width=220,
            options=_get_bluetooth_dropdown_options(),
        )
    ]


def _get_bluetooth_dropdown_options():
    bluetooth_controllers = grab_all_bluetooth_interfaces()
    options = []

    for controller in bluetooth_controllers:
        options.append(ft.DropdownOption(key=bluetooth_controllers[controller]['controller_mac'], text=f"{bluetooth_controllers[controller]['controller_name']} - Powered: {bluetooth_controllers[controller]['powered']} - Discoverable: {bluetooth_controllers[controller]['discoverable']}"))

    return options
