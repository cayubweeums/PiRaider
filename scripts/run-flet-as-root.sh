#!/usr/bin/env bash
# Run PiRaider Flet UI as root (so ip/iw work without sudoers) while keeping
# access to your display. Run this script as your normal user (do not sudo it).
set -e
cd "$(dirname "$0")/.."
exec sudo env \
  DISPLAY="${DISPLAY:-}" \
  XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-}" \
  WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-}" \
  DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-}" \
  "$(pwd)/.venv/bin/python" main.py "$@"
