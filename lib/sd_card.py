import os
import platform
import subprocess
import tkinter as tk
import ctypes
from tkinter import simpledialog, messagebox
import lib.gui.style as ui
import re


def detect_sd_card():
    """Detect connected SD Cards."""
    devices = []
    if platform.system() == "Windows":
        # Windows specific logic
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in range(26):  # Check from A to Z
            if bitmask & (1 << letter):
                drive_letter = f"{chr(65 + letter)}:\\"
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_letter)
                if drive_type == 2:  # DRIVE_REMOVABLE == 2
                    devices.append(drive_letter)
    elif platform.system() == "Darwin":  # macOS
        # macOS specific logic
        volumes = [os.path.join("/Volumes", d) for d in os.listdir("/Volumes") if os.path.ismount(os.path.join("/Volumes", d))]
        devices.extend(volumes)
    elif platform.system() == "Linux":
        # Linux specific logic
        user = os.getenv("USER", "default_user")
        media_path = f"/media/{user}"
        if os.path.exists(media_path):
            devices.extend([os.path.join(media_path, d) for d in os.listdir(media_path)])
    return devices

def get_disk_identifier(volume_path):
    """Returns disk identifier for given volume path."""
    system = platform.system()

    if system == "Darwin":
        result = subprocess.run(['diskutil', 'info', volume_path], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Device Identifier" in line:
                return line.split(":")[1].strip()
    elif system == "Windows":
        # Windows: usa diskpart per ottenere il numero del disco
        try:
            # Get disk number using diskpart
            result = subprocess.run(['diskpart', '/s', 'get_disk_number.txt'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if volume_path in line:
                    # Extract disk number from the line
                    disk_num = line.split()[0]
                    return disk_num
        except Exception as e:
            print(f"Error getting disk number: {e}")
            return None
    return None

def get_volume_by_letter(letter):
    try:
        # Esegui il comando DiskPart per elencare i volumi
        diskpart_script = "list volume"

        process = subprocess.Popen(
            ["diskpart"], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )

        # Invia il comando al processo
        stdout, stderr = process.communicate(input=diskpart_script)

        if stderr:
            print(f"Errore: {stderr}")
            return None

        # Filtriamo l'output per ignorare intestazioni e altre righe non pertinenti
        volume_lines = []
        for line in stdout.splitlines():
            line = line.strip()
            if line and line.startswith("Volume"):  # Solo righe con informazioni sui volumi
                volume_lines.append(line)

        # Cerca la lettera specificata nei volumi
        for line in volume_lines:
            if letter in line:
                print(f"Volume trovato per {letter}: {line}")
                return line

        print(f"Volume con lettera {letter} non trovato.")
        return None

    except Exception as e:
        print(f"Errore: {str(e)}")
        return None

def refresh_sd_devices(sd_select, sd_dropdown, identifier):
    sd_devices = detect_sd_card() or ["Click to refresh"]
    if sd_devices[0] == "Click to refresh":
        selected_sd = "Click to refresh"
    else:
        selected_sd = get_volume_name(identifier)
    menu = sd_dropdown['menu']
    menu.delete(0, 'end')
    for device in sd_devices:
        menu.add_command(label=device, command=tk._setit(sd_select, device))
    sd_select.set(selected_sd)

def eject_sd(sd_device, sd_select, sd_dropdown, terminal):
    system_os = platform.system()
    identifier = get_disk_identifier(sd_device)
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

    refresh_sd_devices(sd_select, sd_dropdown, identifier)

def get_volume_name(disk_identifier):
    """
    RETURN NAME OF VOLUME ASSOCIED WITH DISK.

    Args:
        disk_identifier (str): identifier disk (es. '/dev/disk4', '/dev/sdb', 'D:')

    Returns:
        str: name of volume, or None is not found.
    """
    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            # Usa diskutil per ottenere informazioni sul disco
            result = subprocess.run(
                ["diskutil", "info", disk_identifier],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in result.stdout.splitlines():
                if "Volume Name" in line:
                    return "/Volumes/" + line.split(":")[1].strip()

        elif system == "Linux":
            # Usa lsblk per ottenere informazioni sul disco
            result = subprocess.run(
                ["lsblk", "-o", "NAME,LABEL", "-n", "-l", disk_identifier],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) == 2:  # Controlla che ci sia un'etichetta
                    return parts[1]

        elif system == "Windows":
            # Usa PowerShell per ottenere informazioni sul disco
            result = subprocess.run(
                [
                    "powershell", "-Command",
                    f"Get-Volume -DriveLetter {disk_identifier[0]} | Select-Object -ExpandProperty FileSystemLabel"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip()

        else:
            raise NotImplementedError(f"Piattaforma non supportata: {system}")

    except Exception as e:
        print(f"Errore nel recupero del nome del volume: {e}")

    return None

def format_sd_card(sd_path, display, callback, sd_selector):
    """Automatically format SD Card."""
    os_type = platform.system()
    # print(sd_path)
    try:
        if os_type == "Windows":
            # Chiedi all'utente il nome del volume
            def on_volume_name_enter(volume_name):
                if not volume_name or len(volume_name.strip()) == 0:
                    messagebox.showerror("Error", "Volume name cannot be empty!")
                    return
                volume_name = volume_name.upper()  # Converti in maiuscolo per evitare errori
                identifier = get_disk_identifier(volume_name)
                
                # Crea lo script di formattazione
                script = f"""
                select volume {sd_path[0]}
                format fs=fat32 quick label={volume_name} 
                exit
                """
                try:
                    # Scrivi e esegui il comando DiskPart
                    with open("format_script.txt", "w") as script_file:
                        script_file.write(script)
                    subprocess.run("diskpart /s format_script.txt", check=True, shell=True)
                    os.remove("format_script.txt")
                    # refresh_sd_devices(sd_selector[0], sd_selector[1], identifier)
                    display.message(f"Formatting completed!\nYour SD card has been formatted with the name '{volume_name}'!")
                    try:
                        callback()
                    except:
                        pass
                    return True
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"Error while formatting: {e}")
                    print(e.stderr)
                    return False

            # Chiedi il nome del volume
            display.user_input("Enter the name for your new volume:", on_volume_name_enter)

        elif os_type == "Darwin":
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
                            refresh_sd_devices(sd_selector[0], sd_selector[1], disk_identifier)
                            display.message(f"Formatting completed!\nYour SD card has been formatted with the name '{v}'!")
                            try:
                                callback()  # Call the callback after successful formatting
                            except:
                                pass
                            return True
                        else:
                            messagebox.showerror("Error", "Unable to parse disk identifier correctly.")
                            return False

                    # Chiediamo all'utente il nome del volume
                    display.user_input("Enter the name for your new volume:", on_volume_name_enter)

                display.user_input("Enter password to give\nControl Panel permission to\nformat your SD card:", on_password_enter, "password")

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
