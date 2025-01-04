import os
import platform
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
import lib.gui.style as ui
import re

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
    """Returns disk identifier for given volume path."""
    result = subprocess.run(['diskutil', 'info', volume_path], capture_output=True, text=True)

    # Search for line containing device identifier
    for line in result.stdout.splitlines():
        if "Device Identifier" in line:
            return line.split(":")[1].strip()

    return None

def refresh_sd_devices(sd_select, sd_dropdown):
    sd_devices = detect_sd_card() or ["Plug in and select"]

    menu = sd_dropdown['menu']
    menu.delete(0, 'end')

    for device in sd_devices:
        menu.add_command(label=device, command=tk._setit(sd_select, device))

    sd_select.set(sd_devices[0])

def eject_sd(sd_device, sd_select, sd_dropdown, terminal):
    system_os = platform.system()
    if sd_device != "Plug in and select":
        try:
            if system_os == "Linux":
                os.system(f"umount {sd_device}")
                print(f"{sd_device} successfully unmounted on Linux.")
                terminal.message(f"{sd_device} successfully unmounted on Linux.")
            elif system_os == "Darwin":
                os.system(f"diskutil unmount {sd_device}")
                print(f"{sd_device} successfully unmounted on macOS.")
            elif system_os == "Windows":
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

def format_sd_card(sd_path, display, callback):
    """Automatically format SD Card."""
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
            callback()  # Call the callback after successful formatting
            return True

        if os_type == "Darwin":
            # Get disk identifier for macOS
            disk_identifier = get_disk_identifier(sd_path)
            if disk_identifier:
                def on_password_enter(password: str):
                    # Chiediamo all'utente di inserire un nome valido per il nuovo volume
                    def on_volume_name_enter(volume_name):
                        if not volume_name or len(volume_name.strip()) == 0:
                            messagebox.showerror("Error", "Volume name cannot be empty!")
                            return
                        v = volume_name.upper()  # turn uppercase to avoid errors
                        # Regex to capture the disk part (e.g., disk2 from disk2s55)
                        match = re.match(r'([a-zA-Z]+\d+)', disk_identifier.split(' ')[-1])
                        if match:
                            disk_command = f"diskutil eraseDisk FAT32 \"{v}\" MBRFormat /dev/{match.group(1)}"
                            format_command = f"echo {password} | sudo -S {disk_command}"
                            print(f"Running command: {format_command}")
                            result = subprocess.run(format_command, check=True, shell=True, capture_output=True, text=True)
                            print(result.stdout)  # Debug output
                            display.message(f"Formatting completed!\nYour SD card has been formatted with the name '{v}'!")
                            callback()  # Call the callback after successful formatting
                            return True
                        else:
                            messagebox.showerror("Error", "Unable to parse disk identifier correctly.")
                            return False

                    # Chiediamo all'utente il nome del volume
                    display.user_input("Enter the name for your new volume:", on_volume_name_enter)

                display.user_input("Enter password to give\nControl Panel permission to\nformat your SD card:", on_password_enter)

            else:
                messagebox.showerror("Error", "Unable to find the disk identifier.")
                return False

        elif os_type == "Linux":
            subprocess.run(["sudo", "mkfs.vfat", "-F", "32", sd_path], check=True)
            callback()  # Call the callback after successful formatting
            return True

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error while formatting: {e}")
        print(e.stderr)  # Show detailed error
        return False
