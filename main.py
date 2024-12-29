import tkinter as tk
import threading

import lib.gui
from lib.debug import print_system_info
import apps.sd_flasher._main as sd_app

# Global variables
global page  # Variable that stores the current page in a string
page = "sd"  # We boot up showing the sd_flasher app
window_geometry = None  # To store the current window geometry

def generate_page(root):
    if page == "sd":
        sd_app._main(root)
    elif page == "settings":
        return

def set_page(new_page, root=None):
    global page, window_geometry
    page = new_page
    print(f"Page changed to {page}")  # Debugging

    if root is None:
        root = tk._default_root  # Restore root if it isn't passed. Not recommended but it works!

    # Save the current geometry of the window
    window_geometry = root.geometry()

    # Delete all existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Regenerate the interface
    lib.gui.create_gui(root, page, set_page)
    generate_page(root)

    # Restore the saved geometry
    if window_geometry:
        root.geometry(window_geometry)

def main():
    root = tk.Tk()

    # Start a separate thread to print system info
    # uncomment next 2 lines to print cpu and memory usage in terminal
    #info_thread = threading.Thread(target=print_system_info, args=(page,), daemon=True)
    #info_thread.start()

    lib.gui.fix_window(root) #center window at startup
    lib.gui.create_gui(root, page, lambda new_page: set_page(new_page, root))
    generate_page(root)

    root.mainloop()

if __name__ == "__main__":
    main()
