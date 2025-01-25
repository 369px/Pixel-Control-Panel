# RHCP GUI LIBRARY
# Author(s): 369px
# CC-BY-NC 4.0
#
# Use this library to easily theme GUI in the spruce fashion
# Read this while looking at the template in: [TODO]
#
# You can implement it by first importing this file like this:
    #
    #           import lib.gui.style as ui
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
#from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.font as tkfont
import textwrap, os, platform
from lib.gui.context import context
#import lib.terminal as terminal_func
import lib.sd_card as sd
from typing import Callable, Tuple, Any, Optional

topbar_container = None
bottombar_container = None

class Button:
    ''' To create a button do:

    button_name = Button( ARGUMENTS... ).create()

    Arguments:
    1. parent = any_container,
    - any_container can be any parent container you want to attach this button in. Simplier UI can avoit using this argument
    2. text = "Button label",
    - The label you want to display on the button
    3. command = lambda: any_function(),
    - any_function() can be any function you want to run when an user clicks on the button, leave lambda there
    4. side = "top",
    - add this to put buttons in a list. can be "top" / "bottom"
    4. grid = (row,column),
    - add this to put buttons in a grid. like "grid=(0,1)"
    - [!!!] Remember, you either use "side" or "grid", buttons can't be both in a grid and in a list
    5. bg = "#282828",
    - Background in hex value
    6. fg = "#7c6f64",
    - Button text color
    7. font = ("Arial", 16)
    '''
    def __init__(
        self,
        parent=None,
        text="Label",
        command=None,
        side="top",  # "top" or "bottom" for stack layout
        grid=None,  # tuple (row, column) for grid layout
        bg="#282828",
        fg="#7c6f64",
        font=("Arial", 16),
    ):
        self.parent = parent or context.get_root()  # Use context if parent is not provided
        self.text = text
        self.command = command or (lambda: None)  # Default to a no-op if no command provided
        self.side = side
        self.grid = grid
        self.bg = bg
        self.fg = fg
        self.font = font
        self.container = None

    def create(self):
        """ Creates a customizable button
        """
        # Create the container frame for the button
        self.container = tk.Frame(self.parent, height=50)

        # Use grid or pack separately
        if self.grid:
            # Use grid layout if grid_position is defined
            row, col = self.grid
            self.container.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
        else:
            # Use pack layout (top or bottom) if no grid_position
            if self.side == "bottom":
                self.container.pack(fill="both", expand=True, side="bottom")
            else:
                self.container.pack(fill="both", expand=True, side="top")

        # Create the label inside the container (acting as a button)
        label = tk.Label(self.container, text=self.text, bg=self.bg, fg=self.fg, font=self.font, width=20)
        label.pack(fill="both", expand=True)

        # Bind the command to the label
        label.bind("<Button-1>", lambda e: self.command())
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)

        return self.container

''' Setting a custom background for an app:

            ui.background("#369369")

'''
def background(color="#282828"):
    """
    Changes the background color of an app.

    Args:
    - color (str) (optional): The desired background color in hex format (e.g., "#000000")
    """
    root = context.get_root()  # Automatically get the root from the context
    root.configure(bg=color)

    # Update the background of all children widgets
    def update_children_bg(widget):
        for child in widget.winfo_children():
            if isinstance(child, tk.Frame) or isinstance(child, tk.Label) or isinstance(child, tk.Button):
                child.configure(bg=color)
            update_children_bg(child)

    update_children_bg(root)


''' Creating an SD selector dropdown menu

            ui.create_sd_selector("bottom")

'''
def create_sd_selector(terminal,container_side="top",container_bg="#323232"):
    '''
    Creates an dropdown element showing all connected external devices

    Args:
    - side (str) (optional): set to "bottom" to attach element to the bottom
    '''
    root = context.get_root()

    # SD selection container
    container_sd = tk.Frame(root, height=50, bg=container_bg)

    if container_side == "bottom":
        container_sd.pack(fill="both", expand=True, side="bottom")
    else:
        container_sd.pack(fill="both", expand=True, side="top")

    tk.Label(container_sd, text="TF / SD Card", bg=container_bg, fg="#7c6f64", font=("Arial", 12)).pack(side="left", padx=(12, 5))

    # Icon reference
    root.eject_icon = Image.open("res/gui/eject.png")

    # Resize images to fit the label
    eject_icon_resized = root.eject_icon.resize((22, 22))

    # Convert resized images to PhotoImage compatible with Tkinter
    root.eject_icon_tk = ImageTk.PhotoImage(eject_icon_resized)

    # Create labels for icons with resized images
    eject_icon = tk.Label(container_sd, bg=container_bg, image=root.eject_icon_tk)

    # Bind the "eject" icon click event to unmount the SD card
    eject_icon.bind("<Button-1>", lambda e: sd.eject_sd(sd_select.get(), sd_select, sd_dropdown, terminal))  # Pass the selected SD device

    eject_icon.pack(side="right", padx=(9, 9))
    eject_icon.bind("<Enter>", lambda e: on_enter(e, "#242424"))
    eject_icon.bind("<Leave>", lambda e: on_leave(e))

    sd_select = tk.StringVar()
    sd_devices = sd.detect_sd_card() or ["Plug in and select"]
    sd_dropdown = tk.OptionMenu(container_sd, sd_select, *sd_devices)
    sd_dropdown.config(bg=container_bg, width=20, highlightthickness=0, bd=0)
    sd_dropdown.pack(side="right", pady=5, padx=(15,0))
    sd_select.set(sd_devices[0])


    sd_dropdown.bind("<Button-1>", lambda e: sd.refresh_sd_devices(sd_select, sd_dropdown))

    return sd_select

#
#       ui.window(width,height)
#
# Changes width and height value of the app window
# To only change the width call it like this:       ui.window(330)
# To only change the height call this function:     ui.window_y(400)
#
def window(width=300, height=369):
    '''
    Changes or resets the window's width and height.
    Call without arguments to reset the window to default value.

    Args:
    - width (int) (optional): Changes width of the window, pass only this to only change width
    - height (int) (optional): Changes height of the window
    '''
    root = context.get_root() # Automatically get the root from the context

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

# use this to increse height easily (if you don't' remember width is 300)
# todo: make it smarter (add custom height/width to current value)
def window_y(val):
    '''
    Changes the window's height

    Args:
    - val (int): new height value you want to assign to the window
    '''
    window(300,val)

# Functions to manage hovering on MENU elements (topbar)
def on_enter_menu(e, page, widget_page, sel_bg="#ebdbb2"):
    # Hover only if the widget is not selected
    if page != widget_page:
        if not hasattr(e.widget, "original_bg"):
            e.widget.original_bg = e.widget.cget("bg")
        e.widget.config(bg=sel_bg, cursor="@res/gui/hand.cur")

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

def create_gui(root, app, set_app):
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

    def on_icon_click(new_app):
        set_app(new_app)  # Use the set_app function from main.py

    def generate_top_bar():
        topbar_container = tk.Frame(root, bg="#242424", height=25, pady=0)
        topbar_container.pack(side='top', fill="x", padx=0)

        selected_col = "#323232"
        unselected_col = "#242424"

        # Section we'll use to change between different devices
        device_icon = tk.Label(topbar_container, bg=unselected_col, image=root.device_image)
        device_icon.pack(side="left")
        device_icon.bind("<Enter>", lambda e: on_enter_menu(e, app, "device","#161616"))
        device_icon.bind("<Leave>", lambda e: on_leave_menu(e, app, "device"))

        # Icons attached to the right are the app icons
        settings_icon = tk.Label(topbar_container, bg=selected_col if app == "settings" else unselected_col, image=root.settings_image)
        sd_icon = tk.Label(topbar_container, bg=selected_col if app == "sd" else unselected_col, image=root.sd_image)
        connect_icon = tk.Label(topbar_container, bg=selected_col if app == "template" else unselected_col, image=root.connect_image)

        # Assign callbacks to click events
        #settings_icon.bind("<Button-1>", lambda e: on_icon_click("settings"))
        sd_icon.bind("<Button-1>", lambda e: on_icon_click("sd"))
        #connect_icon.bind("<Button-1>", lambda e: on_icon_click("template"))

        settings_icon.pack(side="right", padx=0)
        settings_icon.bind("<Enter>", lambda e: on_enter_menu(e, app, "settings"))
        settings_icon.bind("<Leave>", lambda e: on_leave_menu(e, app, "settings"))

        sd_icon.pack(side="right", padx=0)
        sd_icon.bind("<Enter>", lambda e: on_enter_menu(e, app, "sd"))
        sd_icon.bind("<Leave>", lambda e: on_leave_menu(e, app, "sd"))

        connect_icon.pack(side="right", padx=0)
        connect_icon.bind("<Enter>", lambda e: on_enter_menu(e, app, "template"))
        connect_icon.bind("<Leave>", lambda e: on_leave_menu(e, app, "template"))

    generate_top_bar()

    def generate_bottom_bar():
        bottombar_container = tk.Frame(root, bg="#282828", height=9, pady=0)
        bottombar_container.pack(side='bottom', fill="x", padx=0)

    generate_bottom_bar()
