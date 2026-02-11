import argparse
import os
import logging
import datetime

import flet as ft
from rich.logging import RichHandler
from rich.traceback import install
from rich import pretty

# Flet UI main entrypoint
from ui.flet.main import flet_main

# TUI UI main entrypoint
from ui.tui.main import tui_main

'''
# Setup Logging
'''
_time = datetime.date.today()

LOG_LEVEL = logging.INFO
FORMAT = '%(asctime)s %(levelname)-8s %(message)s'

if not os.path.exists('./logs'):
    os.makedirs('./logs')
logging.basicConfig(filename='./logs/{}.log'.format(_time), format=FORMAT, level=LOG_LEVEL, datefmt="[%X]")
log = logging.getLogger("frontend_main")

install() # Install Rich traceback
pretty.install() # Install Rich pretty print

'''
# Parse CLI arguments and orchestrate UIs kick offs
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tui", action="store_true", help="Run the TUI")
    parser.add_argument("--web", action="store_true", help="Run the Web app")
    args = parser.parse_args()

    # Don't add the log handler to the TUI or it will print over the TUI
    if not args.tui:
        logging.getLogger().addHandler(RichHandler())

    if args.tui:
        log.info("Running the TUI")
        tui_main()
    if args.web:
        log.info("Running the Web app")
        flet_main(web=True)
    elif not args.tui and not args.web:
        log.info("Running the Native app")
        flet_main()