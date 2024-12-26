import tkinter as tk
import threading

from lib.gui import create_gui
from lib.debug import print_system_info
import APP.sd_flasher._main

global page  # Variable that stores the current page in a string
page = "sd"  # We boot up showing the sd_flasher app

def generate_page(root):
    if page == "sd":
        APP.sd_flasher._main._main(root)
    elif page == "settings":
        return

def set_page(new_page, root=None):
    global page
    page = new_page
    print(f"Page changed to {page}")  # Debugging

    if root is None:
        root = tk._default_root  # restore root if it isn't passed. not recommended but it works!

    # Delete all existent widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Regenerate interface
    create_gui(root, page, set_page)
    generate_page(root)



def main():
    root = tk.Tk()

    # Start a separate thread to print system info
    # uncomment next 2 lines to print cpu and memory usage in terminal
    # info_thread = threading.Thread(target=print_system_info, daemon=True)
    # info_thread.start()

    create_gui(root, page, lambda new_page: set_page(new_page, root))
    generate_page(root)

    root.mainloop()

if __name__ == "__main__":
    main()
