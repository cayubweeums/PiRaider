import asyncio
import logging
from multiprocessing import Process
from typing import Optional

import flet as ft

from core.wifi import (
    is_rick_roll_beacon_running,
    start_rick_roll_beacon,
    stop_rick_roll_beacon,
)

log = logging.getLogger(__name__)

# Seconds to wait before treating process exit as "start failed" (e.g. no interface)
_EARLY_EXIT_SEC = 2.0


class Wifi_Page_Content:
    def __init__(self, page: ft.Page):
        self.page = page
        self._status: str = "idle"
        self._process: Optional[Process] = None
        running, _ = is_rick_roll_beacon_running()
        if running:
            self._status = "running"

        self._status_badge = ft.Container(
            content=ft.Text(self._status.capitalize(), size=14, weight=ft.FontWeight.W_500),
            bgcolor=ft.Colors.GREY_400 if self._status == "idle" else ft.Colors.GREEN_400,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=8,
        )
        self._error_text = ft.Text("", color=ft.Colors.ERROR, size=14, visible=False)
        self._start_btn = ft.ElevatedButton(
            "Start",
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE),
            on_click=lambda e: asyncio.create_task(self._on_start(e)),
            disabled=(self._status == "running"),
        )
        self._stop_btn = ft.ElevatedButton(
            "Stop",
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE),
            on_click=lambda e: asyncio.create_task(self._on_stop(e)),
            disabled=(self._status == "idle"),
        )

    def get_content(self):
        return [
            ft.AppBar(title=ft.Text("WiFi")),
            ft.Text("Rick Roll Beacon", size=18, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[
                    ft.Text("Status:", size=14),
                    self._status_badge,
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.START,
            ),
            self._error_text,
            ft.Row(
                controls=[self._start_btn, self._stop_btn],
                spacing=12,
            ),
        ]

    def _set_status(self, status: str) -> None:
        self._status = status
        self._status_badge.content = ft.Text(status.capitalize(), size=14, weight=ft.FontWeight.W_500)
        self._status_badge.bgcolor = (
            ft.Colors.GREY_400 if status == "idle" else ft.Colors.GREEN_400
        )
        self._start_btn.disabled = status == "running"
        self._stop_btn.disabled = status == "idle"

    def _show_error(self, message: str) -> None:
        self._error_text.value = message
        self._error_text.visible = True

    def _clear_error(self) -> None:
        self._error_text.value = ""
        self._error_text.visible = False

    async def _on_start(self, e: ft.ControlEvent) -> None:
        self._clear_error()
        try:
            process = await asyncio.to_thread(start_rick_roll_beacon)
        except Exception as ex:
            log.exception("Start Rick Roll Beacon failed")
            self._show_error(f"Start failed: {ex}")
            self.page.update()
            return

        if process is None:
            # Already running (e.g. from another session)
            self._set_status("running")
            self._process = None
            self.page.update()
            return

        self._process = process
        self._set_status("running")
        self.page.update()

        # Detect early exit (e.g. no monitor interface)
        async def check_early_exit():
            await asyncio.sleep(_EARLY_EXIT_SEC)
            if self._process is not None and not self._process.is_alive():
                self._process = None
                self._set_status("idle")
                self._show_error(
                    "Transmission stopped. Check WiFi interface is set and supports monitor mode."
                )
                self.page.update()

        asyncio.create_task(check_early_exit())

    async def _on_stop(self, e: ft.ControlEvent) -> None:
        self._clear_error()
        try:
            await asyncio.to_thread(stop_rick_roll_beacon)
        except Exception as ex:
            log.exception("Stop Rick Roll Beacon failed")
            self._show_error(f"Stop failed: {ex}")
        self._process = None
        self._set_status("idle")
        self.page.update()
