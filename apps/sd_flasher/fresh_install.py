''' from wiki:
Windows (10):

Formatting your microSD card:

    Insert your microSD card into your computer.
    Open Rufus.
    Select your card from the top most drop down menu.
    Change “Boot selection” to “Non bootable”.
    Change “File system” to FAT32.
    If you want, name the drive in “Volume label”.
    Press Start, there will be a pop-up warning you that all data will be lost, press OK.

Installation:

    In File Explorer, navigate to the downloaded “spruce.vX.X.zip” file.
    Right-click it, select “Extract all...” and extract the contents directly onto your microSD card.
    When this is complete, right click on the microSD card and select “Eject” to safely remove it.
    Insert the microSD card into the device and turn it on.

Mac:

Formatting your microSD card:

    Insert your microSD card into your Mac.
    Open Disk Utility.
    Select your microSD card.
    At the top of the window, click Erase.
    Name the card.
    Under Format select MS-DOS (FAT32).
    Click Erase.
    When finished, click Done

Installation:

    Open Finder.
    SHIOW HIDDEN FILES by pressing Command + Shift + . (Period).
    Navigate to the “spruce.vX.X.zip” and extract it.
    Copy/Paste the entire extracted contents onto your microSD card.
    Use an App like CleanEject (https://www.javawa.nl/cleaneject_en.html) to eject and clean the junk .dot files from your microSD card.

Chrome:

Formatting your microSD card:

    Insert your microSD card into your computer.
    Open the “Files” app.
    Navigate to your microSD card.
    Right-click (double finger tap) on your card.
    Select “Format device”.
    Name the card.
    In “Format” select FAT32.
    Click “Erase and Format”.
    Click the Eject icon to the right of the drive name and remove the card.
    Reinsert the card (mine bugged out on me if I didn't do this and renamed all the files adding a “ (1)” to the end).

Installation:

    In the “Files” app navigate to the downloaded “spruce.vX.X.X.zip” file.
    Open the file, this might take a second to load.
    Press Control+A to select all files.
    Right-click (double finger tap).
    Select “Copy”.
    Navigate to your microSD card (it will be blank).
    Right-click (double finger tap).
    Select “Paste”.
    When the files are done pasting, click on the Eject icon to the right of the drive name.
    Remove the microSD card and insert it into your A30.

Linux:

There are just too many distros to get into a lot of detail with Linux.

    Format your microSD card to FAT32, I used the standard disk utility on Ubuntu.
    Extract the “spruce.vX.X.X” file.
    Open the extracted folder and SHOW HIDDEN FILES.
    Copy and Paste the contents of the extracted folder onto the microSD card.
    When complete, eject the microSD card and insert it into your A30. Linux Note:

Ubuntu, at least for me, has the .Config and .Temp_Update folders hidden, you need these files.
Common issue!
The .tmp_update folder is very important and without it spruce just isn't going to work properly. If you are having issues, please check to see that this folder is present on your microSD card.
'''

import requests, os, zipfile, threading, asyncio, subprocess, time

from apps.sd_flasher.update import get_latest_release_link
from lib.sd_card import format_sd_card, get_volume_by_letter

def start_installing(sd_selector, display):

    # Step 1: Get the selected SD card path
    print("select sd...")
    sd_card_path = sd_selector[0].get()

    if not sd_card_path or sd_card_path == "Plug in and select":
        display.message("Please select a valid SD card.")
        return  # Stop the process if no SD card is selected

    # Step 2: Format the SD card to FAT32
    try:
        display.message(f"Formatting {sd_card_path} to FAT32...")

        # Call format_sd_card and pass None as callback, because we don't need to flash anything
        format_sd_card(sd_card_path, display, None, sd_selector)
    except Exception as e:
        display.message(f"Error formatting SD card: {e}")
        print(f"Error formatting SD card: {e}")
        return  # Stop the process if formatting fails

    # Start download on a different thread
    download_thread = threading.Thread(target=_download_update, args=(sd_selector, display))
    download_thread.start()

def _download_update(sd_selector, display): 
    try: 
        local_filename = os.path.join(sd_selector[0].get(), 'spruce.zip')

        print("Start download...")

        response = requests.get(get_latest_release_link(display), stream=True)
        response.raise_for_status()


        total_size = int(response.headers.get("Content-Length", 0))
        downloaded_size = 0

        chunk_size = 1024  
        update_interval = 3 * 1024 * 1024  
        last_update = 0

            # Scarica il file a blocchi
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    # Aggiorna la terminale ogni volta che sono stati scaricati almeno 3 MB
                    if downloaded_size - last_update >= update_interval:
                        display.message(f"{downloaded_size / (1024 * 1024):.0f}/{total_size / (1024 * 1024):.0f} MB")
                        last_update = downloaded_size

        display.message("Download completed, init unzip!")

        # Estrazione del file ZIP
        extract_path = os.path.join(sd_selector[0].get(), 'spruce')

        if not os.path.exists(extract_path):
            os.makedirs(extract_path)

        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        print(f"Extraction complete in {extract_path}.")
    
    except Exception as e: 
        print("Exception:", e)