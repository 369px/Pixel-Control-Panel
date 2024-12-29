# RHCP GUI LIBRARY
# Author(s): 369px
# CC-BY-NC 4.0
#
# Use this library to easily theme the GUI in the spruce fashion.
# You can implement it by first importing this file like this:
    #
    #           import lib.gui as ui
    #
#
# Then, you can call any function in here like this:
    #
    #           ui.any_function()
    #
#
# Assign it to a variable for better management:
    #
    #           your_var = ui.any_function()
    #
#
# Don't worry, you don't have to understand everything in here
# I'll do my best to explain things as easily as I can
# At least ones you'll need.

import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
import textwrap
import os
import platform
from lib.gui_context import context
from lib.sd_card import detect_sd_card

def fix_window(root, width=300, height=369):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Functions to manage hovering on MENU elements (topbar)
def on_enter_menu(e, page, widget_page):
    # Hover only if the widget is not selected
    if page != widget_page:
        if not hasattr(e.widget, "original_bg"):
            e.widget.original_bg = e.widget.cget("bg")
        e.widget.config(bg="#ebdbb2", cursor="@res/gui/hand.cur")

def on_leave_menu(e, page, widget_page):
    # Restore original color only if the widget is not selected
    if page != widget_page:
        e.widget.config(bg=e.widget.original_bg)

# hovering everywhere else
def on_enter(e, sel_bg="#ebdbb2"):
    # Save original attribute to restore on_leave
    if not hasattr(e.widget, "original_bg"):
        e.widget.original_bg = e.widget.cget("bg")
    e.widget.config(bg=sel_bg, cursor="@res/gui/hand.cur")

def on_leave(e):
    e.widget.config(bg=e.widget.original_bg)  # Restore original color

def create_gui(root, page, set_page):
    root.title("spruceUI Control Panel")

    root.resizable(False, False)

    # Set app background color
    root.configure(bg="#282828")

    # Set app icon
    icon = tk.PhotoImage(file="res/icon.png")
    root.iconphoto(False, icon)

    # Keep references to images to avoid garbage collection
    root.device_image = tk.PhotoImage(file="res/devices/miyooa30.png")
    root.settings_image = tk.PhotoImage(file="res/apps/settings-uns.png")
    root.sd_image = tk.PhotoImage(file="res/apps/sd.png")
    root.connect_image = tk.PhotoImage(file="res/apps/connect.png")

    def on_icon_click(new_page):
        set_page(new_page)  # Use the set_page function from main.py

    def generate_top_bar():
        topbar_container = tk.Frame(root, bg="#242424", height=25, pady=0)
        topbar_container.pack(side='top', fill="x", padx=0)

        selected_col = "#323232"
        unselected_col = "#242424"

        # Section we'll use to change between different devices
        device_icon = tk.Label(topbar_container, bg=unselected_col, image=root.device_image)
        device_icon.pack(side="left")
        device_icon.bind("<Enter>", lambda e: on_enter_menu(e, page, "device"))
        device_icon.bind("<Leave>", lambda e: on_leave_menu(e, page, "device"))

        # Icons attached to the right are the app icons
        settings_icon = tk.Label(topbar_container, bg=selected_col if page == "settings" else unselected_col, image=root.settings_image)
        sd_icon = tk.Label(topbar_container, bg=selected_col if page == "sd" else unselected_col, image=root.sd_image)
        connect_icon = tk.Label(topbar_container, bg=selected_col if page == "connect" else unselected_col, image=root.connect_image)

        # Assign callbacks to click events
        settings_icon.bind("<Button-1>", lambda e: on_icon_click("settings"))
        sd_icon.bind("<Button-1>", lambda e: on_icon_click("sd"))
        connect_icon.bind("<Button-1>", lambda e: on_icon_click("connect"))

        settings_icon.pack(side="right", padx=0)
        settings_icon.bind("<Enter>", lambda e: on_enter_menu(e, page, "settings"))
        settings_icon.bind("<Leave>", lambda e: on_leave_menu(e, page, "settings"))

        sd_icon.pack(side="right", padx=0)
        sd_icon.bind("<Enter>", lambda e: on_enter_menu(e, page, "sd"))
        sd_icon.bind("<Leave>", lambda e: on_leave_menu(e, page, "sd"))

        connect_icon.pack(side="right", padx=0)
        connect_icon.bind("<Enter>", lambda e: on_enter_menu(e, page, "connect"))
        connect_icon.bind("<Leave>", lambda e: on_leave_menu(e, page, "connect"))

    generate_top_bar()

def refresh_sd_devices(sd_select, sd_dropdown):
    # Get updated SD devices
    sd_devices = detect_sd_card() or ["Insert SD Card and select it here"]

    # Remove old devices from the dropdown
    menu = sd_dropdown['menu']
    menu.delete(0, 'end')

    # Add new devices to the dropdown
    for device in sd_devices:
        menu.add_command(label=device, command=tk._setit(sd_select, device))

    # Set the first item as selected
    sd_select.set(sd_devices[0])

def eject_sd(sd_device, sd_select, sd_dropdown):
    system_os = platform.system()  # Get the operating system
    if sd_device != "Insert SD Card and select it here":
        try:
            if system_os == "Linux":
                # On Linux, use umount to unmount the SD card
                os.system(f"umount {sd_device}")
                print(f"{sd_device} successfully unmounted on Linux.")
            elif system_os == "Darwin":
                # On macOS, use diskutil unmount to unmount the SD card
                os.system(f"diskutil unmount {sd_device}")
                print(f"{sd_device} successfully unmounted on macOS.")
            elif system_os == "Windows":
                # On Windows, use PowerShell to unmount the device
                # Assume the SD is a 'D:' type device; adjust the command based on the drive letter
                # Use "diskpart" to unmount the device or "mountvol" to unmount the drive letter
                os.system(f"mountvol {sd_device} /p")
                print(f"{sd_device} successfully unmounted on Windows.")
            else:
                print(f"Operating system {system_os} not supported for unmounting.")
                return False
        except Exception as e:
            print(f"Error unmounting {sd_device}: {e}")
            return False
    else:
        print("No SD found to unmount.")

    refresh_sd_devices(sd_select, sd_dropdown)

def create_sd_selector(root):
    # SD selection container
    container_sd = tk.Frame(root, height=50)
    container_sd.pack(fill="both", expand=True)

    #tk.Label(container_sd, text="Select SD:", fg="#7c6f64", font=("Arial", 12)).pack(side="left", padx=(10, 5))

    sd_select = tk.StringVar()
    sd_devices = detect_sd_card() or ["Insert SD Card and select it here"]
    sd_dropdown = tk.OptionMenu(container_sd, sd_select, *sd_devices)
    sd_dropdown.pack(side="left", pady=10, padx=(15,0))
    sd_select.set(sd_devices[0])

    sd_dropdown.bind("<Button-1>", lambda e: refresh_sd_devices(sd_select, sd_dropdown))

    # Icon references
    #root.refresh_icon = Image.open("res/gui/refresh.png")
    root.eject_icon = Image.open("res/gui/eject.png")

    # Resize images to fit the label (e.g., 16x16 pixels)
    #refresh_icon_resized = root.refresh_icon.resize((16, 16))
    eject_icon_resized = root.eject_icon.resize((22, 22))

    # Convert resized images to PhotoImage compatible with Tkinter
    #root.refresh_icon_tk = ImageTk.PhotoImage(refresh_icon_resized)
    root.eject_icon_tk = ImageTk.PhotoImage(eject_icon_resized)

    # Create labels for icons with resized images
    #refresh_icon = tk.Label(container_sd, bg="#323232", image=root.refresh_icon_tk)
    eject_icon = tk.Label(container_sd, bg="#323232", image=root.eject_icon_tk)

    # Bind the "refresh" icon click event to the refresh function
    #refresh_icon.bind("<Button-1>", lambda e: refresh_sd_devices(sd_select, sd_dropdown))

    # Bind the "eject" icon click event to unmount the SD card
    eject_icon.bind("<Button-1>", lambda e: eject_sd(sd_select.get(), sd_select, sd_dropdown))  # Pass the selected SD device

    eject_icon.pack(side="right", padx=(0, 9))
    eject_icon.bind("<Enter>", lambda e: on_enter(e, "#242424"))
    eject_icon.bind("<Leave>", lambda e: on_leave(e))

    # Bind the hover event on the "refresh" icon
    #refresh_icon.pack(side="right", padx=(0, 0))
    #refresh_icon.bind("<Enter>", lambda e: on_enter(e))
    #refresh_icon.bind("<Leave>", lambda e: on_leave(e))

    return sd_select

def create_list_btn(text, command, bg="#282828", fg="#7c6f64", font=("Arial", 16)):
    """Create a block with a customizable button."""
    root = context.get_root()  # Automatically get the root from the context

    container = tk.Frame(root, height=50)
    container.pack(fill="both", expand=True)

    label = tk.Label(container, text=text, bg=bg, fg=fg, font=font)
    label.pack(fill="both", expand=True)
    label.bind("<Button-1>", lambda e: command())  # Directly call the function
    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)

    return container


def create_terminal(root):
    # Container for logo
    terminal_canvas = tk.Canvas(root, height=155)
    terminal_canvas.pack(fill="x", expand=True,pady=(0,0))

    # Load and display the logo image
    logo_image = Image.open("res/gui/terminal_bg.png")
    resized_image = logo_image.resize((155, 155))

    root.logo_img = ImageTk.PhotoImage(resized_image)  # Store the reference in root
    terminal_canvas.create_image(75, 0, anchor="nw", image=root.logo_img)  # Posiziona l'immagine in alto a sinistra

    return terminal_canvas

def append_terminal_message(terminal, message, x=0, y=0):
    width = terminal.winfo_width()
    height = terminal.winfo_height()

    # Create a font object to measure text width
    font_size = 12
    font = tkfont.Font(family="Arial", size=font_size)

    # Calculate max number of chars per line based on max width
    char_width = font.measure("a")
    max_width = width
    max_chars_per_line = max_width // char_width

    # Split message by \n and wrap each line
    lines = message.split("\n")
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(textwrap.wrap(line, width=max_chars_per_line))

    # Delete previous text if it exists
    if hasattr(terminal, 'text_items') and terminal.text_items:
        for item in terminal.text_items:
            terminal.delete(item)

    # Center text block
    block_height = len(wrapped_lines) * font_size
    y_start = (height // 2) - (block_height // 2)

    # Draw each row centered
    terminal.text_items = []
    for i, line in enumerate(wrapped_lines):
        y_line = y_start + i * font_size
        text_item = terminal.create_text(
            width // 2, y_line, text=line, font=("Arial", font_size), fill="#ebdbb2", anchor="center"
        )
        terminal.text_items.append(text_item)
