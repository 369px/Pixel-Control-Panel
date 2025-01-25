''' from wiki:
Unbricking an A30

    Download and Extract the Unbricker Image.

    Using Rufus, flash the Unbricker as a bootable image onto a fresh microSD card formatting it to FAT32.

'''

import py7zr, threading
from pathlib import Path
from lib import sd_card
import lib.gui.style as ui
from tkinter import filedialog
import requests
import os, platform
import subprocess

from lib.usb_flasher import USBFlasher

# Global to store update file path
cached_file_path = None

# Unbricker image download link
unbricker_download_link = "https://github.com/spruceUI/spruceOS/releases/download/UnbrickerImage/spi_burn_20240402.img"
file_name = "spi_burn_20240402.img"

# Function to flash the unbricker image
def flash_unbricker(sd_selector, display):
    # Start download on a different thread
    print("download..")
    download_thread = threading.Thread(target=_download_and_flash, args=(sd_selector, display))
    download_thread.start()

# Function to download and flash the unbricker image
def _download_and_flash(sd_selector, display):
    # Step 1: Check if the file is already downloaded
    print("real download..")
    user_folder = Path.home() / ".spruce_updates"
    user_folder.mkdir(parents=True, exist_ok=True)

    print("continuo download..")

    cached_file_path = user_folder / file_name
    if cached_file_path.exists():
        display.message("Unbricker image already downloaded.")
        print("Unbricker image already downloaded.")
    else:
        display.message("Downloading unbricker image file...")
        print("Downloading unbricker image file...")
        try:
            with requests.get(unbricker_download_link, stream=True) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded_size = 0
                chunk_size = 1024  # Chunk size in bytes
                update_interval = 3 * 1024 * 1024  # Update message every 3 MBs
                last_update = 0

                with open(cached_file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)

                            if downloaded_size - last_update >= update_interval:
                                display.message(f"{downloaded_size / (1024 * 1024):.0f}/{total_size / (1024 * 1024):.0f} MB")
                                last_update = downloaded_size

            display.message("Download completed!")
            print("Downloading completed...")
        except requests.exceptions.RequestException as e:
            display.message(f"Error during download: {e}")
            return  # Stop the process if download fails

    # Step 2: Get the selected SD card path
    print("select sd...")
    sd_card_path = sd_selector[0].get()

    if not sd_card_path or sd_card_path == "Plug in and select":
        display.message("Please select a valid SD card.")
        return  # Stop the process if no SD card is selected

    print("flash_unbricker_for_real...")
    def flash_unbricker_for_real():
        # Step 4: Flash the unbricker image onto the SD card
        try:
            display.message("Flashing unbricker image onto SD card...")
            flash_image_to_sd(sd_card_path, cached_file_path)
            display.message(f"Unbricker image successfully flashed to {sd_card_path}!")
        except Exception as e:
            display.message(f"Error flashing the unbricker image: {e}")
            return  # Stop the process if flashing fails

    # Step 3: Format the SD card to FAT32 (if necessary)
    try:
        display.message(f"Formatting {sd_card_path} to FAT32...")

        # Call format_sd_card and pass flash_unbricker_for_real as the callback
        if not sd_card.format_sd_card(sd_card_path, display, flash_unbricker_for_real):
            print(f"Error formatting SD card: {sd_card_path}")
            return  # Stop the process if formatting fails

        display.message(f"SD card {sd_card_path} formatted successfully!")

    except Exception as e:
        display.message(f"Error formatting SD card: {e}")
        print(f"Error formatting SD card: {e}")
        return  # Stop the process if formatting fails

# Function to flash the image to the SD card
def flash_image_to_sd(sd_card_path, image_path):
    system_os = platform.system()
    print(f"Flashing image on {system_os}")
    print(f"SD card path: {sd_card_path}")
    print(f"Image path: {image_path}")

    image_path = Path(image_path).resolve()  # Risolve i percorsi relativi

    try:
        if system_os == "Windows":            
            try:
                # Extract drive letter from sd_card_path
                if isinstance(sd_card_path, str):
                    drive_letter = sd_card_path[0] if sd_card_path else None
                else:
                    drive_letter = str(sd_card_path)[0] if str(sd_card_path) else None

                if not drive_letter:
                    raise ValueError("Invalid SD card path: unable to determine drive letter")

                # Initialize and use the flasher
                flasher = USBFlasher()
                success = flasher.flash(str(image_path), drive_letter)

                if not success:
                    raise RuntimeError("Flash operation failed")

                print("Flash completed successfully")
                return True
            except Exception as e:
                print(f"Error flashing image: {e}")

        elif system_os == "Darwin" or system_os == "Linux":
            # macOS/Linux: Use dd command
            device_path = sd_card.get_disk_identifier(sd_card_path)  # Adjust if necessary
            subprocess.run(f"sudo dd if={image_path} of={device_path} bs=4M status=progress", shell=True, check=True)
        else:
            raise OSError(f"Unsupported OS: {system_os}")

        # Sync the file system to ensure it's written to disk
        # subprocess.run(f"sync", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to flash image to {sd_card_path}: {str(e)}")  # Raise error if dd fails
