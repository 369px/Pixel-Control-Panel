import tkinter as tk

# Functions to manage hovering on elements
def on_enter(e):
    e.widget.config(bg="#ebdbb2")

def on_leave(e):
    e.widget.config(bg="#282828")

def create_gui(root):
    root.title("spruceUI Control Panel")

    def fix_window(width=300, height=339):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width/2)-(width/2)
        y = (screen_height/2)-(height/2)
        root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    fix_window()

    root.resizable(False, False)

    # Set app background color
    root.configure(bg="#282828")

    # Set app icon
    icon = tk.PhotoImage(file="res/icon.png")
    root.iconphoto(False, icon)

    # Keep references to images to avoid garbage collection
    root.device_image = tk.PhotoImage(file="res/miyooa30.png")
    root.settings_image = tk.PhotoImage(file="res/settings-uns.png")

    def generate_top_bar():
        topbar_container = tk.Frame(root, bg="#282828", height=25, pady=0)
        topbar_container.pack(side='top', fill="x", padx=0)

        # Add left image to top bar
        device_icon = tk.Label(topbar_container, bg="#282828", image=root.device_image)
        device_icon.pack(side="left")
        device_icon.bind("<Enter>", on_enter)
        device_icon.bind("<Leave>", on_leave)

        # Add right image to top bar
        settings_icon = tk.Label(topbar_container, bg="#282828", image=root.settings_image)
        settings_icon.pack(side="right", padx=0)
        settings_icon.bind("<Enter>", on_enter)
        settings_icon.bind("<Leave>", on_leave)

    generate_top_bar()
