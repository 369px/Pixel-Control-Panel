from lib.gui import style as ui, terminal
#from lib.gui.button import BButton
from apps.sd_flasher.update import start_update
import apps.sd_flasher.events as events
import tkinter as tk

def _main(root):
    menu_container = tk.Frame(root)
    menu_container.pack(fill="both", expand=True, side="bottom")

    display = terminal.create("bottom")

    sd_selector = ui.create_sd_selector(display,"top")

    update_btn = ui.Button(
        parent=menu_container,
        text="Update spruce",
        command=lambda: display.confirmation(
            "Drop an update file or press 'A' to download the latest release",
            lambda: start_update(sd_selector, display)
        )
    ).create()

    install_btn = ui.Button(
        parent=menu_container,
        text="Fresh Install (first time)",
    ).create()

    firmware_btn = ui.Button(
        parent=menu_container,
        text="Update Firmware"
    ).create()

    unbrick_btn = ui.Button(
        parent=menu_container,
        text="Unbrick",
    ).create()
