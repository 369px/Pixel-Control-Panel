import tkinter as tk
import threading

from lib.gui import create_gui
from lib.debug import print_system_info
import APP.sd_flasher._main

page = "sd"

def main():
    root = tk.Tk()

    # Start a separate thread to print system info
    info_thread = threading.Thread(target=print_system_info, daemon=True)
    info_thread.start()

    create_gui(root, page)

    # Calling APP (currently it's the only one we have)
    if page == "sd":
        APP.sd_flasher._main._main(root)

    root.mainloop()

if __name__ == "__main__":
    main()
