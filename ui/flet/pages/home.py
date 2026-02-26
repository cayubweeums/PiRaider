import asyncio
from typing import Callable

import flet as ft

from core.config import get_key
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
        )
    ]

def _device_set_in_config(key: str) -> bool:
    """True if key exists in config and has a non-empty value."""
    value = get_key(key) or ""
    return bool(str(value).strip())


def _get_radio_status(page: ft.Page):
    wifi_set = _device_set_in_config("wifi_device")
    bt_set = _device_set_in_config("bluetooth_device")
    wifi_icon = ft.Icons.WIFI if wifi_set else ft.Icons.WIFI_FIND_OUTLINED
    wifi_color = ft.Colors.GREEN if wifi_set else ft.Colors.AMBER_600
    bt_icon = ft.Icons.BLUETOOTH_CONNECTED_SHARP if bt_set else ft.Icons.BLUETOOTH_SEARCHING_OUTLINED
    bt_color = ft.Colors.GREEN if bt_set else ft.Colors.AMBER_600
    wifi_available = True if grab_all_wireless_interfaces() else False
    bt_available = True if grab_all_bluetooth_interfaces() else False

    def _radio_icon(
        icon: str,
        icon_color: str,
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
        _radio_icon(wifi_icon, wifi_color, not wifi_available, 3.0, lambda: asyncio.create_task(page.push_route("/settings_wifi"))),
        _radio_icon(bt_icon, bt_color, not bt_available, 2.5, lambda: asyncio.create_task(page.push_route("/settings_bluetooth"))),
    ]
