from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import RadioButton


class CustomHeader(Horizontal):
    """Header showing WiFi/Bluetooth status (display-only, set programmatically)."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a custom header (values set from config by app)."""
        yield RadioButton("WiFi", id="wifi_status", value=False)
        yield RadioButton("Bluetooth", id="bluetooth_status", value=False)