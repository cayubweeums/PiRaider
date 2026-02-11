import pytest


def test_imports():
    import flet as ft
    from rich.logging import RichHandler
    from rich.traceback import install
    from rich import pretty
    from textual.app import App, ComposeResult
    import asyncio

    assert ft is not None
    assert RichHandler is not None
    assert install is not None
    assert pretty is not None
    assert App is not None
    assert ComposeResult is not None
    assert asyncio is not None