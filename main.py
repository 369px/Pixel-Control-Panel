import tkinter as tk
import threading

from lib.gui import create_gui
from lib.debug import print_system_info
import APP.sd_flasher._main

page = "sd" # we boot up showing the sd_flasher app
# TODO: if device is connected through samba, show another app (it means a30 is on)

def generate_page(root):
    if page == "sd":
        APP.sd_flasher._main._main(root)

def main():
    root = tk.Tk()

    # Start a separate thread to print system info
    info_thread = threading.Thread(target=print_system_info, daemon=True)
    info_thread.start()


    create_gui(root, page)
    generate_page(root)

    root.mainloop()

if __name__ == "__main__":
    main()
