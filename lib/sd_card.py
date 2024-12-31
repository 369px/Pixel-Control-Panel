import os
import platform
import subprocess
from tkinter import messagebox
import tkinter
import lib.gui as ui

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

def refresh_sd_devices(sd_select, sd_dropdown):
    # Get updated SD devices
    sd_devices = detect_sd_card() or ["Plug in and select"]

    # Remove old devices from the dropdown
    menu = sd_dropdown['menu']
    menu.delete(0, 'end')

    # Add new devices to the dropdown
    for device in sd_devices:
        menu.add_command(label=device, command=tkinter._setit(sd_select, device))

    # Set the first item as selected
    sd_select.set(sd_devices[0])

def eject_sd(sd_device, sd_select, sd_dropdown, terminal):
    system_os = platform.system()  # Get the operating system
    if sd_device != "Plug in and select":
        try:
            if system_os == "Linux":
                # On Linux, use umount to unmount the SD card
                os.system(f"umount {sd_device}")
                print(f"{sd_device} successfully unmounted on Linux.")
                terminal.message(f"{sd_device} successfully unmounted on Linux.")
            elif system_os == "Darwin":
                # On macOS, use diskutil unmount to unmount the SD card
                os.system(f"diskutil unmount {sd_device}")
                print(f"{sd_device} successfully unmounted on macOS.")
            elif system_os == "Windows":
                # On Windows, use PowerShell to unmount the device
                # Assume the SD is a 'D:' type device; adjust the command based on the drive letter
                # Use "diskpart" to unmount the device or "mountvol" to unmount the drive letter
                os.system(f"mountvol {sd_device} /p")
                print(f"{sd_device} successfully unmounted on Windows.")
            else:
                print(f"Operating system {system_os} not supported for unmounting.")
                return False
        except Exception as e:
            print(f"Error unmounting {sd_device}: {e}")
            return False
    else:
        print("No SD found to unmount.")
        terminal.message("No SD found to unmount.")

    refresh_sd_devices(sd_select, sd_dropdown)


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
