import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from lib.gui import on_enter, on_leave
from APP.sd_flasher.detect_sd import detect_sd_card
from APP.sd_flasher.format_sd import format_sd_card
from APP.sd_flasher.install_spruce import install_spruce


def _main(root):
    # Keep references to images to avoid garbage collection
    root.logo_img = None

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

    # Container for SD card selection
    container_sd = tk.Frame(root, height=50)
    container_sd.pack(fill="both", expand=True)

    tk.Label(container_sd, text="Select SD Card:", fg="#7c6f64", font=("Arial", 12)).pack(side="left", padx=10)

    sd_selector = tk.StringVar()
    sd_devices = detect_sd_card() or ["No external SD found"]
    sd_dropdown = tk.OptionMenu(container_sd, sd_selector, *sd_devices)
    sd_dropdown.pack(side="left", padx=10, pady=10)
    sd_selector.set(sd_devices[0])

    # Container for logo
    container_logo = tk.Frame(root)
    container_logo.pack(fill="x", expand=True)

    # Load and display the logo image
    logo_image = Image.open("res/icon.png")
    resized_image = logo_image.resize((155, 155))
    root.logo_img = ImageTk.PhotoImage(resized_image)  # Store the reference in root
    logo_icon = tk.Label(container_logo, image=root.logo_img)
    logo_icon.pack(fill="both")

    # Container for "Install spruceUI" button
    container1 = tk.Frame(root, height=50)
    container1.pack(fill="both", expand=True)

    label1 = tk.Label(container1, text="Install spruceUI", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    label1.pack(fill="both", expand=True)
    label1.bind("<Button-1>", lambda e: start_installation())
    label1.bind("<Enter>", on_enter)
    label1.bind("<Leave>", on_leave)

    # Container for "Run unbricker" button
    container2 = tk.Frame(root, height=50)
    container2.pack(fill="both", expand=True)

    label2 = tk.Label(container2, text="Run unbricker", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    label2.pack(fill="both", expand=True)
    label2.bind("<Button-1>", lambda e: start_installation())
    label2.bind("<Enter>", on_enter)
    label2.bind("<Leave>", on_leave)

    # Container for "Exit" button
    container3 = tk.Frame(root, height=50)
    container3.pack(fill="both", expand=True)

    label3 = tk.Label(container3, text="Exit", bg="#282828", fg="#7c6f64", font=("Arial", 16))
    label3.pack(fill="both", expand=True)
    label3.bind("<Button-1>", lambda e: root.quit())
    label3.bind("<Enter>", on_enter)
    label3.bind("<Leave>", on_leave)
