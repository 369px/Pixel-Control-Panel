import lib.gui.style as ui
import platform

def window_manager(root):
    ui.window()  # Center window at startup

    root.overrideredirect(True)

    if platform.system() == "Winows":
        import win32gui, win32con, win32api

        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)


    #root.attributes('-topmost', True) # force app on top.
