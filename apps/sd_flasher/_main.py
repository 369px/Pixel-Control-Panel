import lib.gui as ui
import lib.terminal as terminal
from apps.sd_flasher.update import start_update
import tkinter

def _main(root):
    unbrick_btn = ui.create_list_btn(
        text="Unbrick",
        command=lambda: start_update(sd_selector, display),
        side="bottom",
    )

    firmware_btn = ui.create_list_btn(
        text="Update firmware",
        command=lambda: root.quit(),
        side="bottom",
    )

    install_btn = ui.create_list_btn(
        text="Fresh install (first time)",
        command=lambda: display.message("ciao!"),
        side="bottom",
    )

    update_btn = ui.create_list_btn(
        text="Update spruce",
        command=lambda: start_update(sd_selector, display),
        side="bottom",
    )

    display = terminal.create("bottom")
    sd_selector = ui.create_sd_selector(display,"top")
