import tkinter as tk
from UI.gui import create_gui

import APP.sd_flasher._main

page = "sd"

def main():
    root = tk.Tk()

    create_gui(root)

    #Calling APP (currently it's the only one we have)
    APP.sd_flasher._main._main(root)

    root.mainloop()

if __name__ == "__main__":
    main()
