import logging
from typing import Any

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Footer, Label, Select, Static, Button

from core.config import get_key, has_key, set_key
from core.radio import grab_all_bluetooth_interfaces

log = logging.getLogger(__name__)


class BluetoothConfigScreen(Screen):
    """Screen to set the active Bluetooth interface (dropdown selection)."""

    BINDINGS = [Binding("q", "pop_screen", "Back")]

    # Initialize the vars we will use to hold the dropdown values b4 saving to config
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._pending_bluetooth_device: str | None = None

    def compose(self) -> ComposeResult:
        interfaces = grab_all_bluetooth_interfaces() or {}
        options = list[str]()

        for controller in interfaces:
            options.append(f"{interfaces[controller]['controller_name']} - {interfaces[controller]['controller_mac']} - Powered: {interfaces[controller]['powered']} - Discoverable: {interfaces[controller]['discoverable']}")

        # Get the current Bluetooth device from the config or use the first available controller
        current = get_key("bluetooth_device") if has_key("bluetooth_device") else None
        initial = current if current in options else (options[0] if options else Select.BLANK)

        # Build the screen elements
        yield Static("Bluetooth interface", id="bluetooth_config_title")
        yield Label("Choose controller:")
        if options:
            yield Select.from_values(
                options,
                prompt="Bluetooth controller",
                allow_blank=False,
                value=initial,
                id="bluetooth_controller_select",
            )
        else:
            yield Select(
                [("(no controllers found)", None)],
                prompt="Bluetooth controller",
                allow_blank=True,
                id="bluetooth_controller_select",
            )
        yield Footer()
        with Horizontal(id="bluetooth_config_actions"):
            yield Button("Save", id="save_bluetooth_config", variant="success")

    # When the dropdown is changed, make sure it wasn't changed to blank, then update the pending Bluetooth device
    @on(Select.Changed, "#bluetooth_controller_select")
    def _on_bluetooth_controller_select_changed(self, event: Select.Changed) -> None:
        value = event.value
        if value is None or value is Select.BLANK or not value.strip():
            self._pending_bluetooth_device = None
            return
        device_id = value.split(" - ")[1].strip() # The MAC address is the second item in the dropdown
        self._pending_bluetooth_device = device_id if device_id else None

    # When the save button is pressed, ensure the value in pending is not nothing, then save it to the config
    @on(Button.Pressed, "#save_bluetooth_config")
    def _on_bluetooth_controller_select_saved(self, event: Button.Pressed) -> None:
        device_id = self._pending_bluetooth_device
        if device_id is None:
            select = self.query_one("#bluetooth_controller_select", Select)
            raw = select.value
            if raw and raw is not Select.BLANK and isinstance(raw, str) and raw.strip():
                device_id = raw.split(" - ")[1].strip() # The MAC address is the second item in the dropdown
        if not device_id:
            log.warning("No Bluetooth controller selected; not persisting.")
            return
        set_key("bluetooth_device", device_id)
        log.info("Bluetooth controller saved: %s", device_id)
        self.notify(f"Saved: {device_id}", title="Bluetooth config")

    # When the user presses the back button, pop the screen and refresh the header
    def action_pop_screen(self) -> None:
        self.app.pop_screen()
        if hasattr(self.app, "refresh_header_from_config"):
            self.app.refresh_header_from_config()
