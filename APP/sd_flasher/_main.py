import tkinter as tk
import lib.gui as ui

from APP.sd_flasher.install_spruce import install_spruce
from APP.sd_flasher.install_spruce import start_installation

def _main(root):
    #root.logo_img = None

    sd_selector = ui.sd_selector(root)
    terminal = ui.create_terminal(root)

    list_item1 = tk.Frame(root, height=50)
    list_item1.pack(fill="both", expand=True)

    update_label = tk.Label(list_item1, text="Update spruce", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    update_label.pack(fill="both", expand=True)
    update_label.bind("<Button-1>", lambda e: start_installation(sd_selector, terminal))
    update_label.bind("<Enter>", ui.on_enter)
    update_label.bind("<Leave>", ui.on_leave)

    list_item2 = tk.Frame(root, height=50)
    list_item2.pack(fill="both", expand=True)

    install_label = tk.Label(list_item2, text="Fresh install (first time)", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    install_label.pack(fill="both", expand=True)
    install_label.bind("<Button-1>", lambda e: start_installation(sd_selector, terminal))
    install_label.bind("<Enter>", ui.on_enter)
    install_label.bind("<Leave>", ui.on_leave)

    container3 = tk.Frame(root, height=50)
    container3.pack(fill="both", expand=True)

    label3 = tk.Label(container3, text="Update firmware", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    label3.pack(fill="both", expand=True)
    label3.bind("<Button-1>", lambda e: root.quit())
    label3.bind("<Enter>", ui.on_enter)
    label3.bind("<Leave>", ui.on_leave)

    # Container for "Run unbricker" button
    container2 = tk.Frame(root, height=50)
    container2.pack(fill="both", expand=True)

    label2 = tk.Label(container2, text="Unbrick", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    label2.pack(fill="both", expand=True)
    label2.bind("<Button-1>", lambda e: start_installation(sd_selector, terminal))
    label2.bind("<Enter>", ui.on_enter)
    label2.bind("<Leave>", ui.on_leave)
