import tkinter as tk
import lib.gui as ui
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

from APP.sd_flasher.detect_sd import detect_sd_card
from APP.sd_flasher.format_sd import format_sd_card
from APP.sd_flasher.install_spruce import install_spruce

def _main(root):
    # Keep references to images to avoid garbage collection
    root.logo_img = None

    # Funzione per iniziare l'installazione
    def start_installation():
        selected_sd = sd_selector.get()
        if not selected_sd or selected_sd == "No external SD found":
            ui.append_terminal_message(terminal, "Error: No SD card selected!")
            return

        zip_path = filedialog.askopenfilename(title="Select spruceOS ZIP file", filetypes=[("ZIP Files", "*.zip")])
        if not zip_path:
            return

        ui.append_terminal_message(terminal, f"Formatting SD card: {selected_sd}...")
        format_sd_card(selected_sd)
        ui.append_terminal_message(terminal, f"Installing spruceOS from {zip_path}...")
        install_spruce(selected_sd, zip_path)
        ui.append_terminal_message(terminal, "Installation completed!")

    # Container for SD card selection
    container_sd = tk.Frame(root, height=50)
    container_sd.pack(fill="both", expand=True)

    tk.Label(container_sd, text="Select SD Card:", fg="#7c6f64", font=("Arial", 12)).pack(side="left", padx=10)

    sd_selector = tk.StringVar()
    sd_devices = detect_sd_card() or ["No external SD found"]
    sd_dropdown = tk.OptionMenu(container_sd, sd_selector, *sd_devices)
    sd_dropdown.pack(side="left", padx=10, pady=10)
    sd_selector.set(sd_devices[0])

    terminal = ui.create_terminal(root)

    list_item1 = tk.Frame(root, height=50)
    list_item1.pack(fill="both", expand=True)

    update_label = tk.Label(list_item1, text="Update spruce", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    update_label.pack(fill="both", expand=True)
    update_label.bind("<Button-1>", lambda e: start_installation())
    update_label.bind("<Enter>", ui.on_enter)
    update_label.bind("<Leave>", ui.on_leave)

    list_item2 = tk.Frame(root, height=50)
    list_item2.pack(fill="both", expand=True)

    install_label = tk.Label(list_item2, text="Fresh install (first time)", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    install_label.pack(fill="both", expand=True)
    install_label.bind("<Button-1>", lambda e: start_installation())
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
    label2.bind("<Button-1>", lambda e: start_installation())
    label2.bind("<Enter>", ui.on_enter)
    label2.bind("<Leave>", ui.on_leave)
