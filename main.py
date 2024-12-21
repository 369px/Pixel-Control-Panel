import os
import subprocess
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile

def detect_sd_card():
    """Detect connected SD Card"""
    if platform.system() == "Windows":
        drives = [f"{chr(letter)}:\\" for letter in range(65, 91) if os.path.exists(f"{chr(letter)}:\\")]
        for drive in drives:
            if "Removable" in os.popen(f"vol {drive}").read():
                return drive
    elif platform.system() == "Darwin":
        return "/Volumes"
    elif platform.system() == "Linux":
        return "/media/" + os.getenv("USER")
    return None

def format_sd_card(sd_path):
    """Automatically format SD Card"""
    os_type = platform.system()

    try:
        if os_type == "Windows":
            # Commands to format on windows using diskpart
            script = f"""
            select volume {sd_path[0]}
            format fs=fat32 quick
            exit
            """
            with open("format_script.txt", "w") as script_file:
                script_file.write(script)

            subprocess.run("diskpart /s format_script.txt", check=True, shell=True)
            os.remove("format_script.txt")

        elif os_type == "Darwin":
            # Command to format on mac using diskutil
            subprocess.run(["diskutil", "eraseDisk", "FAT32", "SDCARD", "MBRFormat", sd_path], check=True)

        elif os_type == "Linux":
            # Command to format on Linux using mkfs
            subprocess.run(["sudo", "mkfs.vfat", "-F", "32", sd_path], check=True)

        messagebox.showinfo("Formatting completed", "Your SD card has been formatted correctly!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error while formatting: {e}")

def install_spruce(sd_path, zip_path):
    """Install Spruce OS on SD card"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(sd_path)
        messagebox.showinfo("Installation complete", "Spruce OS has been installed correctly!")
    except Exception as e:
        messagebox.showerror("Error", f"Error while installing: {e}")

def main():
    root = tk.Tk()
    root.title("spruceUI Control Panel")
    root.geometry("369x193")
    
    # Set app background color
    root.configure(bg="#282828")
    
    # Set app icon
    icon = tk.PhotoImage(file="res/icon.png")
    root.iconphoto(False, icon)

    # Function to manage hovering on elements
    def on_enter(e):
        e.widget.winfo_children()[0].config(fg="#282828")  # Cambia il colore del testo in nero
        e.widget.winfo_children()[0].config(bg="#ebdbb2")  # Ripristina il colore sfondo

    def on_leave(e):
        e.widget.winfo_children()[0].config(fg="#7c6f64")  # Ripristina il colore del testo a bianco
        e.widget.winfo_children()[0].config(bg="#282828")  # Ripristina il colore sfondo

    # Funzione per avviare l'installazione
    def start_installation():
        sd_path = detect_sd_card()
        if not sd_path:
            messagebox.showerror("Error", "SD card not found!")
            return

        zip_path = filedialog.askopenfilename(title="Select spruceOS ZIP file", filetypes=[("ZIP Files", "*.zip")])
        if not zip_path:
            return

        format_sd_card(sd_path)
        install_spruce(sd_path, zip_path)

    # Crea i container invece dei bottoni
    container1 = tk.Frame(root, height=50)
    container1.pack(fill="both", expand=True)
    container1.bind("<Enter>", on_enter)
    container1.bind("<Leave>", on_leave)
    
    label1 = tk.Label(container1, text="Install spruceUI", fg="#ebdbb2", font=("Arial", 16))
    label1.pack(fill="both", expand=True)
    label1.bind("<Button-1>", lambda e: start_installation())  # Aggiungi azione al clic

    container2 = tk.Frame(root, height=50)
    container2.pack(fill="both", expand=True)
    container2.bind("<Enter>", on_enter)
    container2.bind("<Leave>", on_leave)
    
    label2 = tk.Label(container2, text="Run unbricker", bg="#282828", fg="#ebdbb2", font=("Arial", 16))
    label2.pack(fill="both", expand=True)
    label2.bind("<Button-1>", lambda e: start_installation())  # Aggiungi azione al clic

    container3 = tk.Frame(root, bg="#282828", height=50)
    container3.pack(fill="both", expand=True)
    container3.bind("<Enter>", on_enter)
    container3.bind("<Leave>", on_leave)
    
    label3 = tk.Label(container3, text="Exit", fg="#ebdbb2", font=("Arial", 16))
    label3.pack(fill="both", expand=True)
    label3.bind("<Button-1>", lambda e: root.quit())  # Aggiungi azione al clic

    root.mainloop()

if __name__ == "__main__":
    main()