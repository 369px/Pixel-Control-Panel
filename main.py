import tkinter as tk
import threading, platform, os, sys, ctypes
import lib.gui.style as ui
from lib.gui.context import context
import apps.sd_flasher._main as sd_app
import apps.settings._main as settings_app
import apps.template._main as template_app
from lib.spruce import app, window_geometry, device
from tkinterdnd2 import TkinterDnD
import lib.window_manager as winman

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def generate_page(root):
    if app == "sd":
        sd_app._main(root)
    elif app == "settings":
        settings_app._main(root)
    elif app=="template":
        #template_app._main(root)
        return

def set_app(new_app, root=None):
    global app, window_geometry
    app = new_app

    if root is None:
        root = tk._default_root  # Restore root if it isn't passed

    # Save the current geometry
    window_geometry = root.geometry()

    # Delete all existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Regenerate the interface
    ui.create_gui(root, app, set_app)
    generate_page(root)

    # Restore the window geometry
    if window_geometry:
        root.geometry(window_geometry)

def main():
    if platform.system() == 'Windows':
        if not is_admin():
            # Usa pythonw.exe per evitare la finestra del terminale
            pythonw_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
            if not os.path.exists(pythonw_path):
                pythonw_path = "pythonw.exe"  # Assicurati che pythonw.exe sia nel PATH

            # Rilancia il programma come amministratore senza aprire il terminale
            ctypes.windll.shell32.ShellExecuteW(None, "runas", pythonw_path, " ".join(sys.argv), None, 1)
            sys.exit()
    
    root = TkinterDnD.Tk()
    context.set_root(root)  # Set root global context

    # Start a separate thread to print system info
    # uncomment next 2 lines to print cpu and memory usage in terminal
    #info_thread = threading.Thread(target=print_system_info, args=(page,), daemon=True)
    #info_thread.start()

    winman.window_manager(root)

    ui.create_gui(root, app, lambda new_app: set_app(new_app, root))
    generate_page(root)
    #ui.draw_after_page(root)

    root.mainloop()

if __name__ == "__main__":
    main()
