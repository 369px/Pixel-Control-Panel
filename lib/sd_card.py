import os
import platform
import subprocess
from tkinter import messagebox

def detect_sd_card():
    """Detect connected SD Cards."""
    devices = []
    if platform.system() == "Windows":
        drives = [f"{chr(letter)}:\\" for letter in range(65, 91) if os.path.exists(f"{chr(letter)}:\\")]
        for drive in drives:
            if "Removable" in os.popen(f"vol {drive}").read():
                devices.append(drive)
    elif platform.system() == "Darwin":
        volumes = [os.path.join("/Volumes", d) for d in os.listdir("/Volumes") if os.path.ismount(os.path.join("/Volumes", d))]
        devices.extend(volumes)
    elif platform.system() == "Linux":
        user = os.getenv("USER", "default_user")
        media_path = f"/media/{user}"
        if os.path.exists(media_path):
            devices.extend([os.path.join(media_path, d) for d in os.listdir(media_path)])
    return devices

def get_disk_identifier(volume_path):
    result = subprocess.run(['diskutil', 'info', volume_path], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith('   Device Identifier'):
            return line.split(':')[1].strip()
    return None

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
