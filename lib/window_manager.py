import lib.gui.style as ui
import platform

def window_manager(root):
    ui.window()
    root.overrideredirect(True)

    if platform.system() == "Windows":
        def set_taskbar_icon():
            import win32gui, win32con, win32api
            hwnd = win32gui.GetForegroundWindow()
            style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            style |= win32con.WS_EX_APPWINDOW
            win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

        root.after(10, set_taskbar_icon)
