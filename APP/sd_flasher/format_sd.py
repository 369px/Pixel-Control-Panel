import os
import subprocess
import platform
from tkinter import messagebox
from APP.sd_flasher.detect_sd import get_disk_identifier

def format_sd_card(sd_path):
    """Automatically format SD Card"""
    os_type = platform.system()

    try:
        if os_type == "Windows":
            script = f"""
            select volume {sd_path[0]}
            format fs=fat32 quick
            exit
            """
            with open("format_script.txt", "w") as script_file:
                script_file.write(script)
            subprocess.run("diskpart /s format_script.txt", check=True, shell=True)
            os.remove("format_script.txt")

        if os_type == "Darwin":
            # Trova l'identificatore del disco per il volume
            disk_identifier = get_disk_identifier(sd_path)
            if disk_identifier:
                applescript_command = f'sudo diskutil eraseDisk FAT32 {disk_identifier} MBRFormat'
                subprocess.run(['osascript', '-e', applescript_command], check=True)
                messagebox.showinfo("Formatting completed", "Your SD card has been formatted correctly!")
            else:
                messagebox.showerror("Error", "Unable to find the disk identifier.")

        elif os_type == "Linux":
            subprocess.run(["sudo", "mkfs.vfat", "-F", "32", sd_path], check=True)

        messagebox.showinfo("Formatting completed", "Your SD card has been formatted correctly!")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error while formatting: {e}")
