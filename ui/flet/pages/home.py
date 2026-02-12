import asyncio

import flet as ft

button_icon_size = 180

def home_page(page: ft.Page):
    return [
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