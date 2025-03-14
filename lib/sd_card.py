import os, platform, subprocess, tempfile
import tkinter as tk
import ctypes
from tkinter import simpledialog, messagebox
import lib.gui.style as ui
import re
import threading

def detect_sd_card():
    """Detect connected SD Cards."""
    devices = []
    if platform.system() == "Windows":
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in range(26):  # Check from A to Z
            if bitmask & (1 << letter):
                drive_letter = f"{chr(65 + letter)}:\\"
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_letter)
                if drive_type == 2:  # DRIVE_REMOVABLE == 2
                    try:
                        volume_name_buffer = ctypes.create_unicode_buffer(1024)
                        volume_serial = ctypes.c_ulong(0)
                        max_component_length = ctypes.c_ulong(0)
                        file_system_flags = ctypes.c_ulong(0)
                        file_system_name_buffer = ctypes.create_unicode_buffer(1024)
                        
                        if ctypes.windll.kernel32.GetVolumeInformationW(
                            drive_letter,
                            volume_name_buffer,
                            ctypes.sizeof(volume_name_buffer),
                            ctypes.byref(volume_serial),
                            ctypes.byref(max_component_length),
                            ctypes.byref(file_system_flags),
                            file_system_name_buffer,
                            ctypes.sizeof(file_system_name_buffer)
                        ):
                            label = volume_name_buffer.value
                            # If there is a label, show both letter and label
                            if label:
                                devices.append(f"{drive_letter[0]}:\\ ({label})")
                            else:
                                devices.append(drive_letter)
                        else:
                            devices.append(drive_letter)
                    except Exception as e:
                        print(f"Error getting volume name: {e}")
                        devices.append(drive_letter)
    elif platform.system() == "Darwin":  # macOS
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
    system = platform.system()

    if system == "Windows":
        try:
            drive_letter = volume_path.split(" ")[0]
            command = f"""
            $driveLetter = '{drive_letter[0]}'
            $removableDrives = Get-WmiObject -Query "SELECT * FROM Win32_DiskDrive WHERE InterfaceType='USB'"
            foreach ($drive in $removableDrives) {{
                $partitions = Get-WmiObject -Query "ASSOCIATORS OF {{Win32_DiskDrive.DeviceID='$($drive.DeviceID)'}} WHERE AssocClass=Win32_DiskDriveToDiskPartition"
                foreach ($partition in $partitions) {{
                    $logicalDisks = Get-WmiObject -Query "ASSOCIATORS OF {{Win32_DiskPartition.DeviceID='$($partition.DeviceID)'}} WHERE AssocClass=Win32_LogicalDiskToPartition"
                    foreach ($logicalDisk in $logicalDisks) {{
                        if ($logicalDisk.DeviceID -eq '{drive_letter[0]}') {{
                            return $drive.PNPDeviceID
                        }}
                    }}
                }}
            }}
            """
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, shell=True)
            
            if result.returncode != 0:
                print(f"Error in PowerShell command: {result.stderr}")
                return None
            
            return result.stdout.strip()
        except Exception as e:
            print(f"Error during retrieving device identifier: {e}")
            return None
    return None


def refresh_sd_devices(sd_select, sd_dropdown, identifier):
    sd_devices = detect_sd_card() or ["Click to refresh"]
    if sd_devices[0] == "Click to refresh" or sd_devices[0] == "None" :
        selected_sd = "Click to refresh"
    else:
        selected_sd = get_volume_name(identifier)
    menu = sd_dropdown['menu']
    menu.delete(0, 'end')
    for device in sd_devices:
        if device != None:
            menu.add_command(label=device, command=tk._setit(sd_select, device))
    sd_select.set(selected_sd)


def eject_sd(sd_device, sd_select, sd_dropdown, terminal):
    system_os = platform.system()

    if system_os == "Windows" and "(" in sd_device:
        drive_letter = sd_device.split(" ")[0]
    else:
        drive_letter = sd_device

    if sd_device != "Click to refresh":
        try:
            if system_os == "Windows":
                # Modified PowerShell command to properly exit after ejection
                script = f"""
                (New-Object -comObject Shell.Application).Namespace(17).ParseName(\"{drive_letter[0]}:\").InvokeVerb(\"Eject\")
                Start-Sleep -Seconds 1
                exit
                """
                
                # Use CREATE_NO_WINDOW to avoid GUI freezing
                result = subprocess.run(
                    ["powershell", "-Command", script], 
                    capture_output=True, 
                    text=True, 
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                if result.returncode == 0:
                    terminal.message(f"{drive_letter} successfully ejected.")
                else:
                    terminal.message(f"Error ejecting {drive_letter}: {result.stderr}")

            elif system_os == "Linux":
                os.system(f"umount {sd_device}")
                print(f"{sd_device} correctly ejected.")
                terminal.message(f"{sd_device} correctly ejected.")
            elif system_os == "Darwin":
                os.system(f"diskutil unmount {sd_device}")
                print(f"{sd_device} correctly ejected.")
                terminal.message(f"{sd_device} correctly ejected.")
            else:
                print(f"{system_os} OS not supported for disk ejection.")
                return False
            
            refresh_sd_devices(sd_select, sd_dropdown, get_disk_identifier(sd_device))
        except Exception as e:
            print(f"Error trying to eject {sd_device}: {e}")
            terminal.message(f"Error trying to eject {sd_device}: {e}")
    else:
        print("No SD found to eject.")
        terminal.message("No SD found to eject.")

def get_volume_name(disk_identifier):
    """
    RETURN NAME OF VOLUME ASSOCIED WITH DISK.

    Args:
        disk_identifier (str): identifier disk (es. '/dev/disk4', '/dev/sdb', 'D:')

    Returns:
        str: name of volume, or None if not found.
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
            print(f"disk_identifier[0]: {disk_identifier}")
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
            raise NotImplementedError(f"Platform not yet supported: {system}")

    except Exception as e:
        print(f"Error trying to get name volume of: {e}")

    return None

def check_password(password: str):
    """verify password with sudo"""
    try:
        result = subprocess.run(
            f"echo {password} | sudo -S -v",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True  # correct Password 
        else:
            return False  # wrong Password
    except Exception:
        return False

import traceback
def format_sd_card(sd_path, display, callback, sd_selector):
    """Automatically format SD Card."""
    os_type = platform.system()
    # print(sd_path)
    if sd_selector[0].get() == "Click to refresh":
        display.message("Formatting ??? to FAT32… did you plug-in an sd?")
        return False
    try:
        if os_type == "Windows":
            # Chiedi all'utente il nome del volume
            def on_volume_name_enter(volume_name):
                if not volume_name or len(volume_name.strip()) == 0:
                    messagebox.showerror("Error", "Volume name cannot be empty!")
                    return
                volume_name = volume_name.upper()  # Converti il nome in maiuscolo per evitare errori
                identifier = get_disk_identifier(volume_name)

                if not identifier:
                    messagebox.showerror("Error", "Unable to get disk identifier.")
                    return

                # Crea lo script di formattazione
                script = f"""
                select volume {sd_path[0]}
                format fs=fat32 quick label={volume_name}
                exit
                """
                
                try:
                    # Scrivi ed esegui lo script diskpart
                    with open("format_script.txt", "w") as script_file:
                        script_file.write(script)
                    
                    # Esegui diskpart
                    result = subprocess.run("diskpart /s format_script.txt", check=True, shell=True, capture_output=True, text=True)
                    
                    # Debug: stampa l'output di diskpart
                    print(f"Diskpart Output (stdout): {result.stdout}")
                    print(f"Diskpart Output (stderr): {result.stderr}")
                    
                    os.remove("format_script.txt")
                    display.message(f"Formatting completed!\nYour SD card has been formatted with the name '{volume_name}'!")
                    
                    # Chiamata al callback
                    try:
                        callback_thread = threading.Thread(target=callback)
                        callback_thread.start()
                    except:
                        traceback.print_exc()
                    return True

                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"Error while formatting: {e}")
                    print(f"Error while formatting: {e}")
                    return False

            # Chiedi all'utente di inserire un nome valido per il volume
            display.user_input("Enter the name for your new volume:", on_volume_name_enter)
        elif os_type == "Darwin":
            # Get disk identifier for macOS
            disk_identifier = get_disk_identifier(sd_path)
            if disk_identifier:
                def on_password_enter(password: str):
                    if not check_password(password):  # Controlla se la password è valida
                        display.message("Error, incorrect password! Please try again.")
                        return
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
                            result = subprocess.run(format_command, check=True, shell=True, capture_output=True, text=True)
                            refresh_sd_devices(sd_selector[0], sd_selector[1], disk_identifier)
                            display.message(f"Formatting completed!\nYour SD card has been formatted with the name '{v}'!")
                            try:
                                callback_thread = threading.Thread(target=callback)
                                callback_thread.start()
                            except:
                                traceback.print_exc()
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
            try:
                callback_thread = threading.Thread(target=callback)
                callback_thread.start()
            except:
                traceback.print_exc()
            return True
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error while formatting: {e}")
        print(e.stderr)  # Show detailed error
        return False

def run_powershell_script(command):
    """Esegui uno script PowerShell in background senza aprire la finestra PowerShell."""
    
    # Crea un file temporaneo per il comando PowerShell
    with tempfile.NamedTemporaryFile(suffix=".ps1", delete=False) as temp_file:
        temp_file.write(command.encode("utf-8"))
        temp_file.close()  # Chiudiamo il file temporaneo per poterlo eseguire

        # Imposta la politica di esecuzione per consentire l'esecuzione di script non firmati
        set_policy_command = "Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force"
        
        try:
            # Esegui il comando PowerShell
            subprocess.run(
                ["powershell", "-Command", set_policy_command],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Esegui lo script PowerShell in background senza finestra
            result = subprocess.run(
                ["powershell.exe", "-ExecutionPolicy", "Unrestricted", "-File", temp_file.name],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Stampa l'output e gli errori (se ci sono)
            if result.returncode != 0:
                print(f"PowerShell Error: {result.stderr}")
                raise Exception(f"Error executing PowerShell script: {result.stderr}")

        except Exception as e:
            print(f"Error during script execution: {e}")
        finally:
            # Rimuovi il file temporaneo dopo l'esecuzione
            os.remove(temp_file.name)

