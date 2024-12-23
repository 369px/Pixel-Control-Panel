import zipfile
from tkinter import messagebox

def install_spruce(sd_path, zip_path):
    """Install Spruce OS on SD card"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(sd_path)
        messagebox.showinfo("Installation complete", "Spruce OS has been installed correctly!")
    except Exception as e:
        messagebox.showerror("Error", f"Error while installing: {e}")
