#import os
#import subprocess
#import platform
import tkinter as tk
#from tkinter import filedialog, messagebox
#from tkinter import *
#from PIL import Image, ImageTk
#import zipfile

import APP.sd_flasher._main
from UI.gui import create_gui

def main():
    root = tk.Tk()

    create_gui(root)

    APP.sd_flasher._main.main_cycle(root)

    root.mainloop()

if __name__ == "__main__":
    main()
