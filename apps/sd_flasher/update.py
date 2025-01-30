import py7zr, threading
from pathlib import Path
import lib.gui.style as ui
from tkinter import filedialog
import requests
import os  # For checking file existence
from lib.sd_card import format_sd_card
import lib.spruce as spruce

# Global to store update file path
cached_file_path = None

# use spruce.download_file(url)

def start_update(sd_selector, display):
    # Start download on a different thread
    download_thread = threading.Thread(target=_download_update, args=(display,))
    download_thread.start()

def get_latest_release_link(display):
    # File url containing last release link information
    url = "https://raw.githubusercontent.com/spruceUI/spruceui.github.io/refs/heads/main/OTA/spruce"

    try:
        # Download file content
        response = requests.get(url)
        response.raise_for_status()  # Verify errors in request

        # Find row that contains 'RELEASE_LINK='
        for line in response.text.splitlines():
            if line.startswith("RELEASE_LINK="):
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

def _download_update(display):
    global cached_file_path

    # Check if the file already exists
    if cached_file_path and os.path.exists(cached_file_path):
        display.message("Update already downloaded.")
        return  # Skip download if the file already exists

    display.message("Downloading update...")

    # URL of file to download
    file_url = "https://github.com/spruceUI/spruceOS/releases/download/v3.2.0/spruceV3.2.0.7z"

    # Determine the user's folder path
    user_folder = Path.home() / ".spruce_updates"
    user_folder.mkdir(parents=True, exist_ok=True)

    # Save the file with the original name in the user's folder
    file_name = file_url.split("/")[-1]
    cached_file_path = user_folder / file_name

    try:
        # Download the file with progress tracking
        with requests.get(file_url, stream=True) as response:
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

                        # Update the terminal only if 3 MBs have been downloaded
                        if downloaded_size - last_update >= update_interval:
                            display.message(f"{downloaded_size / (1024 * 1024):.0f}/{total_size / (1024 * 1024):.0f} MB")
                            last_update = downloaded_size

        display.message("Download completed!")

    except requests.exceptions.RequestException as e:
        display.message(f"Error during download: {e}")

# Function to get the cached file path
def get_cached_file_path():
    global cached_file_path
    if cached_file_path:
        return cached_file_path
    else:
        return None

# Function to extract the 7z file
def extract_update(display):
    global cached_file_path

    if not cached_file_path or not str(cached_file_path).endswith(".7z"):
        display.message("No valid file available for extraction.")
        return

    try:
        with py7zr.SevenZipFile(cached_file_path, mode="r") as archive:
            extract_path = filedialog.askdirectory()
            if extract_path:
                archive.extractall(path=extract_path)
                display.message(f"Files extracted to {extract_path}.")
            else:
                display.message("Extraction canceled.")
    except py7zr.Bad7zFile:
        display.message("Invalid 7z file.")
