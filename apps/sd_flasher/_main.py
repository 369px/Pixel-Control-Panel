import lib.gui as ui
from apps.sd_flasher.install_spruce import install_spruce, start_installation

def _main(root):
    #root.logo_img = None

    sd_selector = ui.sd_selector(root)
    terminal = ui.create_terminal(root)

    update_btn = ui.create_button(
        root,
        text="Update spruce",
        command=lambda e: start_installation(sd_selector, terminal),
    )

    install_btn = ui.create_button(
        root,
        text="Fresh install (first time)",
        command=lambda e: start_installation(sd_selector, terminal),
    )

    firmware_btn = ui.create_button(
        root,
        text="Update firmware",
        command=lambda e: root.quit(),
    )

    unbrick_btn = ui.create_button(
        root,
        text="Unbrick",
        command=lambda e: start_installation(sd_selector, terminal),
    )
