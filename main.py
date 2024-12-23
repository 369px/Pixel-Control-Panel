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

    #Calling APP (currently it's the only one we have)
    APP.sd_flasher._main._main(root)

    root.mainloop()

if __name__ == "__main__":
    main()
