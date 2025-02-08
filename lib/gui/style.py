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
import ctypes, platform

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
            self.container.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        else:
            # Use pack layout (top or bottom) if no grid_position
            if self.side == "bottom":
                self.container.pack(fill="both", expand=True, side="bottom")
            else:
                self.container.pack(fill="both", expand=True, side="top")

        # Create the label inside the container (acting as a button)
        label = tk.Label(self.container, text=self.text, bg=self.bg, fg=self.fg, font=self.font, width=20)
        label.pack(fill="both", expand=True,padx=0)

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
    sd_devices = sd.detect_sd_card() or ["Click to refresh"]
    sd_dropdown = tk.OptionMenu(container_sd, sd_select, *sd_devices)
    sd_dropdown.config(width=20, highlightthickness=0, bd=0)
    sd_dropdown.pack(side="right", pady=5, padx=(15,0))
    sd_select.set(sd_devices[0])

    identifier = sd.get_disk_identifier(sd_devices[0])
    sd_dropdown.bind("<Button-1>", lambda e: sd.refresh_sd_devices(sd_select, sd_dropdown, identifier))

    return sd_select, sd_dropdown

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

    transparent_color = "#ffffff"  # init transparent color
    window_color = "#242424"
    border_color="#181818"

    root_background = tk.Canvas(root, width=300,
                                height=369-42, bg="#282828",
                                bd=0, highlightthickness=0)

    root_background.place(x=0,y=21)


    # Set transparency based on platform
    if platform.system() == "Windows":
        root.attributes("-transparentcolor", '#369369')
        root.config(bg="#369369")
        transparent_color = "#369369"
    elif platform.system() == "Darwin":
        root.attributes("-transparent", True)
        root.config(bg="systemTransparent")
        transparent_color = "systemTransparent"

    # Set app icon
    icon = tk.PhotoImage(file="res/icon.png")
    root.iconphoto(False, icon)

    # Keep references to images to avoid garbage collection
    root.device_image = tk.PhotoImage(file="res/devices/miyooa30.png")
    root.settings_image = tk.PhotoImage(file="res/apps/settings-uns.png")
    root.sd_image = tk.PhotoImage(file="res/apps/sd.png")
    root.connect_image = tk.PhotoImage(file="res/apps/connect.png")

    # Variables for tracking the position
    drag_start_x = 0
    drag_start_y = 0

    def on_drag_start(event):
        nonlocal drag_start_x, drag_start_y
        drag_start_x = event.x_root
        drag_start_y = event.y_root
        event.widget.config(cursor="@res/gui/handGrab.cur")

    def on_drag_motion(event):
        nonlocal drag_start_x, drag_start_y
        delta_x = event.x_root - drag_start_x
        delta_y = event.y_root - drag_start_y
        # Move the window by the delta in the x and y directions
        root.geometry(f"+{root.winfo_x() + delta_x}+{root.winfo_y() + delta_y}")
        drag_start_x = event.x_root  # Update the drag start position to continue dragging
        drag_start_y = event.y_root

    def on_drag_end(event):
        # Reset the cursor when drag ends (when mouse button is released)
        event.widget.config(cursor="@res/gui/handNoGrab.cur")  # Reset cursor to 'handNoGrab.cur'


    def window_close_on_enter_hover(e):
        e.widget.config(cursor="@res/gui/handNoGrab.cur")  # Change to red

    def window_close_on_leave_hover(e):
        e.widget.config(cursor="arrow")  # Change to red


    def arc_border(canvas,x1,y1,x2,y2,sstart,eextent):
        canvas.create_arc(x1, y1, x2, y2, start=sstart, extent=eextent,fill=transparent_color, outline=border_color)


    def generate_window_bar():
        # Create the window bar container with transparent background
        window_bar = tk.Frame(bg=transparent_color, height=21, relief="flat")
        window_bar.pack(side="top", fill="x", padx=0, pady=0, anchor="n")

        # --- Open Arc Transparency (left side) ---
        open_arc_canvas = tk.Canvas(window_bar, width=21, height=21, bg=transparent_color, bd=0, highlightthickness=0)
        open_arc_canvas.pack(side="left", padx=0, anchor="nw")
        arc_border(open_arc_canvas,0-1,0-1,42-1,42-1, 90,180)
        open_arc_canvas.create_arc(0, 0, 42, 42, start=90, extent=180, fill=window_color, outline=transparent_color)

        # --- Close Button (right side) ---
        close_button_canvas = tk.Canvas(window_bar, width=21, height=21, bg=window_color, bd=0, highlightthickness=0)
        close_button_canvas.pack(side="left", padx=0)

        close_btn_border = close_button_canvas.create_line(-2,0,21,0,fill=border_color)

        # Draw the circular "X" button (initial gray color)
        close_circle_id = close_button_canvas.create_oval(2, 5, 14, 17, fill="#4a4a4a", outline="#242424")

        # Bind the click event to close the application
        close_button_canvas.bind("<Button-1>", lambda e: root.quit())

        # Hover effect for close button
        def close_on_enter_hover(e):
            close_button_canvas.itemconfig(close_circle_id, fill="#ff0000")
            e.widget.config(cursor="@res/gui/skull.cur")  # Change to red

        def close_on_leave_hover(e):
            close_button_canvas.itemconfig(close_circle_id, fill="#4a4a4a")  # Change back to gray

        close_button_canvas.bind("<Enter>", close_on_enter_hover)
        close_button_canvas.bind("<Leave>", close_on_leave_hover)

        # --- Closed Arc Transparency (right side) ---
        closed_arc_canvas = tk.Canvas(window_bar, width=21, height=21, bg=transparent_color, bd=0, highlightthickness=0)
        closed_arc_canvas.pack(side="right", padx=0)
        # Adjusting the arc to make it match the open arc in terms of curvature and positioning
        arc_border(closed_arc_canvas,-23+1,0-1,20+1,42-1, -90,180)
        closed_arc_canvas.create_arc(-23, 0, 20, 42, start=-90, extent=180, fill=window_color, outline=transparent_color)

        # Draggable part (adjusted)
        draggable_part = tk.Canvas(window_bar, height=21, bg=window_color, bd=0, highlightthickness=0)
        draggable_part.pack(side="left", fill="x", padx=0, expand=True)  # Allow it to expand and fill space

        draggable_border_top = draggable_part.create_line(-1, 0, 369, 0, fill=border_color)

        title_label = draggable_part.create_text(112, 11, text="Control Panel", fill="#777777", font=("Arial", 10, "bold"))

        draggable_part.bind("<ButtonPress-1>", on_drag_start)
        draggable_part.bind("<B1-Motion>", on_drag_motion)
        draggable_part.bind("<ButtonRelease-1>", on_drag_end)
        draggable_part.bind("<Enter>", window_close_on_enter_hover)
        draggable_part.bind("<Leave>", window_close_on_leave_hover)

        return window_bar  # Return the reference to the window_bar

    # Call the function to create the window bar
    window_bar = generate_window_bar()

    def generate_top_bar():
        topbar_container = tk.Frame(bg="#242424", height=25, pady=0)
        topbar_container.pack(side='top', fill="x", padx=0)

        selected_col = "#323232"
        unselected_col = "#242424"

        # Section we'll use to change between different devices
        device_icon = tk.Label(topbar_container, bg=unselected_col, image=root.device_image)
        device_icon.pack(side="left")
        device_icon.bind("<Enter>", lambda e: on_enter_menu(e, app, "device", "#161616"))
        device_icon.bind("<Leave>", lambda e: on_leave_menu(e, app, "device"))

        # Icons attached to the right are the app icons
        settings_icon = tk.Label(topbar_container, bg=selected_col if app == "settings" else unselected_col, image=root.settings_image)
        sd_icon = tk.Label(topbar_container, bg=selected_col if app == "sd" else unselected_col, image=root.sd_image)
        connect_icon = tk.Label(topbar_container, bg=selected_col if app == "template" else unselected_col, image=root.connect_image)

        # Assign callbacks to click events
        sd_icon.bind("<Button-1>", lambda e: on_icon_click("sd"))
        settings_icon.bind("<Button-1>", lambda e: on_icon_click("settings"))
        connect_icon.bind("<Button-1>", lambda e: on_icon_click("template"))

        settings_icon.pack(side="right", padx=0)
        sd_icon.pack(side="right", padx=0)
        connect_icon.pack(side="right", padx=0)

    generate_top_bar()

    def generate_bottom_bar():
        bottombar_container = tk.Frame(root, bg=transparent_color, height=21, pady=0)
        bottombar_container.pack(side='bottom', fill="x", padx=0)

        # --- Open Arc Transparency (left side) ---
        open_arc_canvas = tk.Canvas(bottombar_container, width=21, height=21, bg=transparent_color, bd=0, highlightthickness=0)
        open_arc_canvas.pack(side="left", padx=0)
        arc_border(open_arc_canvas,0-1,-25+1,41-1,19+1, 180,180)
        open_arc_canvas.create_arc(0, -25, 41, 19, start=180, extent=180, fill=window_color, outline=transparent_color)

        # --- Closed Arc Transparency (right side) ---
        closed_arc_canvas = tk.Canvas(bottombar_container, width=21, height=21, bg=transparent_color, bd=0, highlightthickness=0)
        closed_arc_canvas.pack(side="right", padx=0)
        arc_border(closed_arc_canvas,-21+1,-25+1,20+1,19+1, -180,180)
        closed_arc_canvas.create_arc(-21, -25, 20, 19, start=-180, extent=180, fill=window_color, outline=transparent_color)

        bottom_bar_window = tk.Canvas(bottombar_container, height=20, bg=window_color, bd=0,highlightthickness=0)
        bottom_bar_window.pack(side="right", padx=0, fill="x")

        draggable_border_bottom = bottom_bar_window.create_line(-1,19,369,19,fill=border_color)

        bottom_bar_window.bind("<ButtonPress-1>", on_drag_start)
        bottom_bar_window.bind("<B1-Motion>", on_drag_motion)
        bottom_bar_window.bind("<Enter>", window_close_on_enter_hover)
        bottom_bar_window.bind("<Leave>", window_close_on_leave_hover)
        bottom_bar_window.bind("<ButtonRelease-1>", on_drag_end)


    generate_bottom_bar()


def draw_after_page(root):
    border_left = tk.Canvas(root,width=1,height=100,bg="#121212",bd=0,highlightthickness=0)
    border_left.place(relx=0,rely=0,height=355,anchor="w")
