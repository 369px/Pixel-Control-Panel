import py7zr, zipfile, threading, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import lib.gui.style as ui
from tkinter import filedialog
import requests, time
import os  # For checking file existence
from lib.sd_card import format_sd_card, eject_sd
import lib.spruce as spruce
from datetime import datetime

# Global to store update file path
cached_file_path = None
install_complete = False  # Flag to track installation state

def begin_updating(sd_selector, display):
    # Step 1: Perform the backup first
    display.message("Starting backup process...")
    backup_files(sd_selector, display)

    # Step 2: Start download of the update file in a separate thread
    download_thread = threading.Thread(target=_start_update, args=(sd_selector, display))
    download_thread.start()

def backup_files(sd_selector, display):
    # This function will execute the backup steps
    backup_dir = os.path.join(sd_selector[0].get(), "backups")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Define the folders to back up
    folders_to_backup = [
        "/mnt/SDCARD/App/Syncthing/config",
        "/mnt/SDCARD/App/PICO/bin",
        "/mnt/SDCARD/App/SSH/sshkeys",
        "/mnt/SDCARD/Emu/PICO8/.lexaloffle",
        "/mnt/SDCARD/RetroArch/retroarch.cfg",
        "/mnt/SDCARD/RetroArch/.retroarch/config",
        "/mnt/SDCARD/Emu/NDS/savestates",
        "/mnt/SDCARD/.config/ppsspp/PSP/SAVEDATA",
        "/mnt/SDCARD/.config/ppsspp/PSP/PPSSPP_STATE",
        "/mnt/SDCARD/.config/ppsspp/PSP/SYSTEM",
        "/mnt/SDCARD/App/spruceRestore/.lastUpdate",
        "/mnt/SDCARD/Emu/PICO8/bin",
        "/mnt/SDCARD/Emu/.emu_setup/n64_controller/Custom.rmp",
        "/mnt/SDCARD/Emu/.emu_setup/overrides",
        "/mnt/SDCARD/Emu/NDS/backup",
        "/mnt/SDCARD/Emu/NDS/config",
        "/mnt/SDCARD/Emu/NDS/resources/settings.json",
        "/mnt/SDCARD/RetroArch/.retroarch/overlay",
        "/mnt/SDCARD/spruce/bin/SSH/sshkeys",
        "/mnt/SDCARD/spruce/bin/Syncthing/config",
        "/mnt/SDCARD/spruce/settings/gs_list",
        "/mnt/SDCARD/spruce/settings/spruce.cfg"
    ]

    # Create the backup archive
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}.7z"
    backup_path = os.path.join(backup_dir, backup_filename)

    # Backup the files
    with py7zr.SevenZipFile(backup_path, mode='w') as archive:
        for folder in folders_to_backup:
            if os.path.exists(folder):
                archive.write(folder, os.path.basename(folder))
            else:
                display.message(f"Warning: {folder} does not exist, skipping...")

    display.message(f"Backup completed! Backup file: {backup_filename}")

def _start_update(sd_selector, display):
    global install_complete

    if display.dropped_file is not None:
        display.message("Installing " + display.dropped_file)
        download_thread = threading.Thread(target=extract_update, args=(sd_selector, display, display.dropped_file))
        download_thread.start()
    else:
        if cached_file_path:
            # If the update is already available
            local_filename = cached_file_path
            display.message(f"Using cached update file: {local_filename}")
        else:
            # Download latest release
            local_filename = os.path.join(sd_selector[0].get(), 'update.zip')
            display.message("Starting download...")

            update_url = get_latest_release_link(display)
            try:
                response = requests.get(update_url, stream=True)
                response.raise_for_status()
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded_size = 0

                with open(local_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)

                display.message("Download completed, extracting now...")
            except Exception as e:
                display.message(f"Error downloading the update: {str(e)}")
                return

        # Step 3: Perform the installation of the update
        install_complete = False  # Reset the flag
        download_thread = threading.Thread(target=extract_update, args=(sd_selector, display, local_filename))
        download_thread.start()

def extract_update(sd_selector, display, cached_file_path):
    try:
        sd_path = sd_selector[0].get()
        display.message(f"Starting extraction at {sd_path}")

        # List of excluded directories (folders to merge with)
        excluded_dirs = ['Roms', 'Saves', 'BIOS']

        # Ensure cached_file_path is set correctly
        if cached_file_path is None or not os.path.exists(cached_file_path):
            display.message("Error: Cached file path is invalid or not found.")
            return

        # Step 1: Delete folders at the root level (excluding specified directories)
        for root, dirs, files in os.walk(sd_path, topdown=False):
            if root == sd_path:  # Only look at the root directory
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    if dir not in excluded_dirs:  # Don't delete excluded folders
                        display.message(f"Deleting folder: {dir_path}")
                        try:
                            shutil.rmtree(dir_path, ignore_errors=True)
                        except OSError:
                            pass

        # Step 2: Delete files at the root level (but not inside excluded directories)
        for root, dirs, files in os.walk(sd_path, topdown=False):
            if root == sd_path:  # Only delete files at the root directory
                for file in files:
                    file_path = os.path.join(root, file)
                    if not any(os.path.commonpath([file_path, os.path.join(sd_path, ex_dir)]) == os.path.join(sd_path, ex_dir) for ex_dir in excluded_dirs):
                        display.message(f"Deleting file: {file_path}")
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass

        display.message("Old files have been deleted!\nExtracting update...\nIt may take some time...")

        # Step 3: Extract the downloaded file (whether it's a .zip or .7z)
        if cached_file_path.lower().endswith('.zip'):
            # Handle .zip files using extractall
            with zipfile.ZipFile(cached_file_path, 'r') as zip_ref:
                zip_ref.extractall(sd_path)  # Extract all files
            display.message(f"Update extracted to {sd_path}")

        elif cached_file_path.lower().endswith('.7z'):
            # Handle .7z files using extractall
            with py7zr.SevenZipFile(cached_file_path, mode='r') as archive:
                archive.extractall(sd_path)  # Extract all files
            display.message(f"Update extracted to {sd_path}")

        else:
            display.message("Error: Unsupported file format. Only .zip and .7z files are supported.")
            return

        # Step 4: Merge the files into the Roms, Saves, and BIOS directories
        for root, dirs, files in os.walk(sd_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)

                # Skip files in the excluded directories (Roms, Saves, BIOS)
                if any(os.path.commonpath([file_path, os.path.join(sd_path, ex_dir)]) == os.path.join(sd_path, ex_dir) for ex_dir in excluded_dirs):
                    continue

                # Merge the files into the Roms, Saves, and BIOS directories
                for dir in excluded_dirs:
                    dir_path = os.path.join(sd_path, dir)
                    if dir in dirs:
                        target_file_path = os.path.join(dir_path, file)

                        # Check if the file already exists
                        if os.path.exists(target_file_path):
                            # Compare modification dates (timestamps)
                            existing_mod_time = os.path.getmtime(target_file_path)
                            new_mod_time = os.path.getmtime(file_path)

                            if existing_mod_time == new_mod_time:
                                # Skip if the file is the same (no overwrite)
                                display.message(f"Skipping file: {file} (no changes)")
                            else:
                                # Overwrite if the file is newer
                                display.message(f"Overwriting file: {file} in {dir_path}")
                                shutil.copy2(file_path, target_file_path)
                        else:
                            # If file doesn't exist, just copy it
                            display.message(f"Copying new file: {file} to {dir_path}")
                            shutil.copy2(file_path, target_file_path)

        display.message("Update completed successfully!")

    except Exception as e:
        display.message(f"Error during update extraction: {str(e)}")
        raise


















# HELPER FUNCTIONS (to move elsewhere)
def get_latest_release_link(display,type="user"):
    # File url containing last release link information
    url = "https://raw.githubusercontent.com/spruceUI/spruceui.github.io/refs/heads/main/OTA/spruce"

    if type=="user":
        file_to_download = "RELEASE_LINK="
    else:
        file_to_download = "NIGHTLY_LINK="

    try:
        # Download file content
        response = requests.get(url)
        response.raise_for_status()  # Verify errors in request

        # Find row that contains 'RELEASE_LINK='
        for line in response.text.splitlines():
            if line.startswith(file_to_download):
                # Extract link from row
                release_link = line.split("=", 1)[1].strip()
                return release_link.replace("7z", "zip")

        # If not found, return this
        display.message("RELEASE LINK not found in GH repo...")

        return "RELEASE_LINK not found in the file."

    except requests.exceptions.RequestException as e:
        display.message("Error while fetching update info file...")
        # Handle request errors
        return f"Error while fetching the file: {e}"

# Function to get the cached file path
def get_cached_file_path():
    global cached_file_path
    if cached_file_path:
        return cached_file_path
    else:
        return None
