import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
import textwrap
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
        e.widget.config(bg="#ebdbb2", cursor="@res/hand.cur")

def on_leave_menu(e, page, widget_page):
    # Restore original color only if the widget is not selected
    if page != widget_page:
        e.widget.config(bg=e.widget.original_bg)

# hovering everywhere else
def on_enter(e):
    # Save original attribute to restore on_leave
    if not hasattr(e.widget, "original_bg"):
        e.widget.original_bg = e.widget.cget("bg")
    e.widget.config(bg="#ebdbb2", cursor="@res/hand.cur")

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
    root.device_image = tk.PhotoImage(file="res/miyooa30.png")
    root.settings_image = tk.PhotoImage(file="res/settings-uns.png")
    root.sd_image = tk.PhotoImage(file="res/sd.png")
    root.connect_image = tk.PhotoImage(file="res/connect.png")

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

def sd_selector(root):
    # Container for SD card selection
    container_sd = tk.Frame(root, height=50)
    container_sd.pack(fill="both", expand=True)

    tk.Label(container_sd, text="Select SD Card:", fg="#7c6f64", font=("Arial", 12)).pack(side="left", padx=10)

    sd_select = tk.StringVar()
    sd_devices = detect_sd_card() or ["No external SD found"]
    sd_dropdown = tk.OptionMenu(container_sd, sd_select, *sd_devices)
    sd_dropdown.pack(side="left", padx=10, pady=10)
    sd_select.set(sd_devices[0])

    return sd_select

def create_button(root, text, command, bg ="#282828", fg = "#7c6f64", font = ("Arial", 16)):
    """Crea un blocco con un bottone personalizzabile."""
    container = tk.Frame(root, height=50)
    container.pack(fill="both", expand=True)

    label = tk.Label(container, text=text, bg=bg, fg=fg, font=font)
    label.pack(fill="both", expand=True)
    label.bind("<Button-1>", command)
    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)

    return container

def create_terminal(root):
    # Container for logo
    terminal_canvas = tk.Canvas(root, height=155)
    terminal_canvas.pack(fill="x", expand=True,pady=(0,0))

    # Load and display the logo image
    logo_image = Image.open("res/terminal_bg.png")
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
