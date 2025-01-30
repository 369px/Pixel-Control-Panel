from lib.gui import style as ui, terminal
#from lib.gui.button import BButton
from apps.sd_flasher.update import start_update
from apps.sd_flasher.format import start_formatting
from apps.sd_flasher.fresh_install import start_installing
import apps.sd_flasher.events as events
import tkinter as tk
import lib.sd_card as sd


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
        text="Fresh install",
        command=lambda: display.confirmation(
            "Drop a firmware file or press 'A' to download the latest release",
            lambda: start_installing(sd_selector, display)
        )
    ).create()


    '''
    firmware_btn = ui.Button(
        parent=menu_container,
        text="Update Firmware",
        command=lambda: display.user_input(
            "Input password to format SD Card",
            lambda: flash_unbricker(sd_selector, display))
    ).create()
    '''
    unbrick_btn = ui.Button(
        parent=menu_container,
        text="Format",
        command=lambda: display.confirmation(
            "Drop an unbricker image or\npress 'A' to download / install it",
            lambda: start_formatting(sd_selector, display)
        )
    ).create()
