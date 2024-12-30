import lib.gui as ui
from apps.sd_flasher.update import install_spruce, start_update

def _main(root):
    sd_selector = ui.create_sd_selector()
    terminal = ui.create_terminal()

    update_btn = ui.create_list_btn(
        text="Update spruce",
        command=lambda: start_update(sd_selector, terminal),
    )

    install_btn = ui.create_list_btn(
        text="Fresh install (first time)",
        command=lambda: ui.window(300,100),
    )

    firmware_btn = ui.create_list_btn(
        text="Update firmware",
        command=lambda: root.quit(),
    )

    unbrick_btn = ui.create_list_btn(
        text="Unbrick",
        command=lambda: start_update(sd_selector, terminal),
    )
