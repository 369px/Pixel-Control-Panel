import lib.gui as ui
from apps.sd_flasher.install_spruce import install_spruce, start_installation

def _main(root):
    #root.logo_img = None
    sd_selector = ui.create_sd_selector(root)
    terminal = ui.create_terminal(root)

    update_btn = ui.create_list_btn(
        text="Update spruce",
        command=lambda: start_installation(sd_selector, terminal),
    )

    install_btn = ui.create_list_btn(
        text="Fresh install (first time)",
        command=lambda: start_installation(sd_selector, terminal),
    )

    firmware_btn = ui.create_list_btn(
        text="Update firmware",
        command=lambda: root.quit(),
    )

    unbrick_btn = ui.create_list_btn(
        text="Unbrick",
        command=lambda: start_installation(sd_selector, terminal),
    )
