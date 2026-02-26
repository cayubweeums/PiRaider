import logging

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Footer, Label, Select, Static, Button

from core.config import get_key, has_key, set_key
from core.radio import grab_all_wireless_interfaces

log = logging.getLogger(__name__)


class WifiConfigScreen(Screen):
    """Screen to set the active WiFi interface (dropdown selection)."""

    # Bindings for the screen
    BINDINGS = [Binding("q", "pop_screen", "Back")]

    # Initialize the vars we will use to hold the dropdown values b4 saving to config
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._pending_wifi_device: str | None = None

    def compose(self) -> ComposeResult:
        interfaces = grab_all_wireless_interfaces() or {}
        supported_bands_text = ""
        options = list[str]()

        # Iterate over the interfaces present and add them to the dropdown with a summary of their capabilities
        for interface in interfaces:
            if bool(interfaces[interface]['interface_up']):
                status = "Up"
            else:
                status = "Down"
            if bool(interfaces[interface]['monitor_mode_supported']):
                monitor_mode = "Yes"
            else:
                monitor_mode = "No"
            for band in interfaces[interface]['band_capability']:
                supported_bands_text += f"{interfaces[interface]['band_capability'][band]} GHz, "
            options.append(f"{interfaces[interface]['device_id']} - {status} - mon mode: {monitor_mode} - {supported_bands_text}")

        # Get the current WiFi device from the config or use the first available interface
        current = get_key("wifi_device") if has_key("wifi_device") else None
        initial = current if current in options else (options[0] if options else Select.BLANK)
        self._pending_wifi_device = (
            # Set the pending WiFi device but first strip away the capabilities text
            initial.split(" - ")[0].strip() if isinstance(initial, str) and initial else None
        )

        # Build the screen elements
        yield Static("WiFi interface", id="wifi_config_title")
        yield Label("Choose interface:")
        if options:
            yield Select.from_values(
                options,
                prompt="WiFi interface",
                allow_blank=False,
                value=initial,
                id="wifi_interface_select",
            )
        else:
            yield Select(
                [("(no interfaces found)", None)],
                prompt="WiFi interface",
                allow_blank=True,
                id="wifi_interface_select",
            )
        yield Footer()
        with Horizontal(id="wifi_config_actions"):
            yield Button("Save", id="save_wifi_config", variant="success")

    # When the dropdown is changed, make sure it wasn't changed to blank, then update the pending WiFi device
    @on(Select.Changed, "#wifi_interface_select")
    def _on_wifi_select_changed(self, event: Select.Changed) -> None:
        value = event.value
        if value is None or value is Select.BLANK or not value.strip():
            self._pending_wifi_device = None
            return
        device_id = value.split(" - ")[0].strip()
        self._pending_wifi_device = device_id if device_id else None

    # When the save button is pressed, ensure the value in pending is not nothing, then save it to the config
    @on(Button.Pressed, "#save_wifi_config")
    def _on_wifi_select_saved(self, event: Button.Pressed) -> None:
        device_id = self._pending_wifi_device
        if device_id is None:
            select = self.query_one("#wifi_interface_select", Select)
            raw = select.value
            if raw and raw is not Select.BLANK and isinstance(raw, str) and raw.strip():
                device_id = raw.split(" - ")[0].strip()
        if not device_id:
            log.warning("No WiFi interface selected; not persisting.")
            return
        set_key("wifi_device", device_id)
        log.info("WiFi interface saved: %s", device_id)
        self.notify(f"Saved: {device_id}", title="WiFi config")

    # When the user presses the back button, pop the screen and refresh the header
    def action_pop_screen(self) -> None:
        self.app.pop_screen()
        if hasattr(self.app, "refresh_header_from_config"):
            self.app.refresh_header_from_config()
