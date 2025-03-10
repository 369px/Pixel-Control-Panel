import lib.gui.style as ui
import platform
from ctypes import windll
import tkinter as tk

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
HWND_TOPMOST = -1

def set_app_windows(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    
    # Modifica lo stile della finestra per farla apparire sulla taskbar
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW  # Rimuovi il TOOLWINDOW
    style = style | WS_EX_APPWINDOW  # Aggiungi l'APPWINDOW
    windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    
    # Posiziona la finestra in cima a tutte le altre (topmost)
    windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, 0x0001)

    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

def window_manager(root):
    ui.window()
    root.overrideredirect(True)  # Rimuovi bordi e barra del titolo

    if platform.system() == "Windows":
        root.after(10, lambda: set_app_windows(root))