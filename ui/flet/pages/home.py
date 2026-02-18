import asyncio
from typing import Callable

import flet as ft

from core.radio import grab_all_bluetooth_interfaces, grab_all_wireless_interfaces

button_icon_size = 180

def home_page(page: ft.Page):
    return [
        ft.AppBar(
            actions=_get_radio_status(page),
        ),
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.IconButton(icon=ft.Icons.WIFI, icon_color=ft.Colors.PRIMARY, icon_size=button_icon_size, on_click=lambda: asyncio.create_task(page.push_route("/wifi"))),
                        ft.Text("WiFi", text_align=ft.TextAlign.CENTER),
                    ],
                    spacing=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        ft.IconButton(icon=ft.Icons.BLUETOOTH, icon_color=ft.Colors.PRIMARY, icon_size=button_icon_size, on_click=lambda: asyncio.create_task(page.push_route("/bluetooth"))),
                        ft.Text("Bluetooth", text_align=ft.TextAlign.CENTER),
                    ],
                    spacing=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        ft.IconButton(icon=ft.Icons.DEVICE_UNKNOWN, icon_color=ft.Colors.PRIMARY, icon_size=button_icon_size, on_click=lambda: asyncio.create_task(page.push_route("/devices"))),
                        ft.Text("Devices", text_align=ft.TextAlign.CENTER),
                    ],
                    spacing=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            spacing=50,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]

# TODO Improve this once we have implemented a config. If there is no prior set devices, then this should reflect the status of the 
    # current scan for devices and acquiring device capabilities process. Once that process is complete, it should show solid amber instead of flashing.
    # If there is a config set, then it should flash green until it configures the devices as needed and initializes them. After which the status 
    # should be solid green.
def _get_radio_status(page: ft.Page):
    icon_color = ft.Colors.AMBER_600
    wifi_available = True if grab_all_wireless_interfaces() is not None else False
    bt_available = True if grab_all_bluetooth_interfaces() is not None else False

    def _radio_icon(
        icon: str,
        should_animate: bool,
        duration: float,
        on_click: Callable[..., None] | None = None,
    ):
        """Return a static IconButton or animated Container based on availability."""
        btn = ft.IconButton(icon=icon, icon_color=icon_color, on_click=on_click)
        if not should_animate:
            return btn
        c = ft.Container(content=btn, opacity=0.1, animate_opacity=int(duration * 1000))

        async def animate():
            await asyncio.sleep(0.2)
            while True:
                c.opacity = 1
                page.update()
                await asyncio.sleep(duration)
                c.opacity = 0.1
                page.update()
                await asyncio.sleep(duration)

        page.run_task(animate)
        return c

    return [
        _radio_icon(ft.Icons.WIFI_FIND_OUTLINED, not wifi_available, 3.0, lambda: asyncio.create_task(page.push_route("/settings_wifi"))),
        _radio_icon(ft.Icons.BLUETOOTH_SEARCHING_OUTLINED, not bt_available, 2.5),
    ]
