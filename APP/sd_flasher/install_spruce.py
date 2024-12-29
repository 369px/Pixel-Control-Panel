import zipfile
import lib.gui as ui
from tkinter import filedialog

from lib.sd_card import format_sd_card

def install_spruce(sd_path, zip_path, terminal):
    """Install Spruce OS on SD card"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(sd_path)
        ui.append_terminal_message(terminal, "Installation complete! SpruceUI has been installed correctly!")
    except Exception as e:
        ui.append_terminal_message(terminal, "Error while installing: {e}")

# Funzione per iniziare l'installazione
def start_installation(sd_selector, terminal):
    selected_sd = sd_selector.get()
    if not selected_sd or selected_sd == "No external SD found":
        ui.append_terminal_message(terminal, "Error: No SD card detected!\nPut that shit in dude...")
        return

    zip_path = filedialog.askopenfilename(title="Select spruceOS ZIP file", filetypes=[("ZIP Files", "*.zip")])
    if not zip_path:
        return

    ui.append_terminal_message(terminal, f"Formatting SD card: {selected_sd}...")
    format_sd_card(selected_sd)
    ui.append_terminal_message(terminal, f"Installing spruceOS from {zip_path}...")
    install_spruce(selected_sd, zip_path, terminal)
    ui.append_terminal_message(terminal, "Installation completed!")
