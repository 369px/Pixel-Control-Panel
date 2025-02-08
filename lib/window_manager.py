import lib.gui.style as ui
import platform

def window_manager(root):
    ui.window()
    root.overrideredirect(True)

    if platform.system() == "Windows":
        import win32gui, win32con, win32api

        hwnd = win32gui.GetForegroundWindow()
        # Show app in taskbar
        style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        style = style | win32con.WS_EX_APPWINDOW
        win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
