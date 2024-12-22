import os
import subprocess
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import PhotoImage
from tkinter import *
from PIL import Image, ImageTk
import zipfile

def detect_sd_card():
    """Detect connected SD Cards."""
    devices = []
    if platform.system() == "Windows":
        drives = [f"{chr(letter)}:\\" for letter in range(65, 91) if os.path.exists(f"{chr(letter)}:\\")]
        for drive in drives:
            if "Removable" in os.popen(f"vol {drive}").read():
                devices.append(drive)
    elif platform.system() == "Darwin":
        volumes = [os.path.join("/Volumes", d) for d in os.listdir("/Volumes") if os.path.ismount(os.path.join("/Volumes", d))]
        devices.extend(volumes)
    elif platform.system() == "Linux":
        user = os.getenv("USER", "default_user")
        media_path = f"/media/{user}"
        if os.path.exists(media_path):
            devices.extend([os.path.join(media_path, d) for d in os.listdir(media_path)])
    return devices

def format_sd_card(sd_path):
    """Automatically format SD Card"""
    os_type = platform.system()

    try:
        if os_type == "Windows":
            script = f"""
            select volume {sd_path[0]}
            format fs=fat32 quick
            exit
            """
            with open("format_script.txt", "w") as script_file:
                script_file.write(script)

            subprocess.run("diskpart /s format_script.txt", check=True, shell=True)
            os.remove("format_script.txt")

        elif os_type == "Darwin":
            subprocess.run(["diskutil", "eraseDisk", "FAT32", "SDCARD", "MBRFormat", sd_path], check=True)

        elif os_type == "Linux":
            subprocess.run(["sudo", "mkfs.vfat", "-F", "32", sd_path], check=True)

        messagebox.showinfo("Formatting completed", "Your SD card has been formatted correctly!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error while formatting: {e}")

def install_spruce(sd_path, zip_path):
    """Install Spruce OS on SD card"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(sd_path)
        messagebox.showinfo("Installation complete", "Spruce OS has been installed correctly!")
    except Exception as e:
        messagebox.showerror("Error", f"Error while installing: {e}")

def main():
    root = tk.Tk()
    root.title("spruceUI Control Panel")
    root.geometry("300x339")
    root.resizable(False, False)

    # Set app background color
    root.configure(bg="#282828")

    # Set app icon
    icon = tk.PhotoImage(file="res/icon.png")
    root.iconphoto(False, icon)

    # Function to manage hovering on elements
    def on_enter(e):
        e.widget.config(fg="#282828")
        e.widget.config(bg="#ebdbb2")

    def on_leave(e):
        e.widget.config(fg="#7c6f64")
        e.widget.config(bg="#282828")

    # Function to start installation
    def start_installation():
        selected_sd = sd_selector.get()
        if not selected_sd or selected_sd == "No external SD found":
            messagebox.showerror("Error", "No SD card selected!")
            return

        zip_path = filedialog.askopenfilename(title="Select spruceOS ZIP file", filetypes=[("ZIP Files", "*.zip")])
        if not zip_path:
            return

        format_sd_card(selected_sd)
        install_spruce(selected_sd, zip_path)

    topbar_container = tk.Frame(root, bg="#282828", height=25, pady=0)
    topbar_container.pack(side='top', fill="x", padx=0)

    # Carica l'immagine a sinistra nella top bar
    device_image = tk.PhotoImage(file="res/miyooa30.png")
    device_icon = tk.Label(topbar_container, bg="#282828", image=device_image)
    device_icon.pack(side="left")
    device_icon.bind("<Enter>", on_enter)
    device_icon.bind("<Leave>", on_leave)

    # Carica l'immagine a destra nella top bar
    settings_image = tk.PhotoImage(file="res/settings-uns.png")
    settings_icon = tk.Label(topbar_container, bg="#282828", image=settings_image)
    settings_icon.pack(side="right", padx=0)
    settings_icon.bind("<Enter>", on_enter)
    settings_icon.bind("<Leave>", on_leave)

    container_sd = tk.Frame(root, height=50)
    container_sd.pack(fill="both", expand=True)

    tk.Label(container_sd, text="Select SD Card:", fg="#7c6f64", font=("Arial", 12)).pack(side="left", padx=10)

    sd_selector = tk.StringVar()
    sd_devices = detect_sd_card() or ["No external SD found"]
    sd_dropdown = tk.OptionMenu(container_sd, sd_selector, *sd_devices)
    sd_dropdown.pack(side="left", padx=10, pady=10)
    sd_selector.set(sd_devices[0])

    container_logo = tk.Frame(root)
    container_logo.pack(fill="x", expand=True)

    logo_image = Image.open("res/icon.png")
    resized_image = logo_image.resize((155, 155))
    logo_img = ImageTk.PhotoImage(resized_image)
    logo_icon = tk.Label(container_logo, image=logo_img)
    logo_icon.pack(fill="both")

    container1 = tk.Frame(root, height=50)
    container1.pack(fill="both", expand=True)

    label1 = tk.Label(container1, text="Install spruceUI", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    label1.pack(fill="both", expand=True)
    label1.bind("<Button-1>", lambda e: start_installation())
    label1.bind("<Enter>", on_enter)
    label1.bind("<Leave>", on_leave)

    container2 = tk.Frame(root, height=50)
    container2.pack(fill="both", expand=True)

    label2 = tk.Label(container2, text="Run unbricker", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    label2.pack(fill="both", expand=True)
    label2.bind("<Button-1>", lambda e: start_installation())
    label2.bind("<Enter>", on_enter)
    label2.bind("<Leave>", on_leave)

    container3 = tk.Frame(root, height=50)
    container3.pack(fill="both", expand=True)

    label3 = tk.Label(container3, text="Exit", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    label3.pack(fill="both", expand=True)
    label3.bind("<Button-1>", lambda e: root.quit())
    label3.bind("<Enter>", on_enter)
    label3.bind("<Leave>", on_leave)

    root.mainloop()

if __name__ == "__main__":
    main()
