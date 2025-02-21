import requests, os, zipfile, threading, asyncio, subprocess, time
import zipfile, py7zr

from apps.sd_flasher.update import get_latest_release_link
from apps.sd_flasher.format import start_formatting

from lib.sd_card import format_sd_card, get_volume_by_letter, eject_sd

def start_installing(sd_selector, display, dropped_file):
    # Start download on a different thread

    def call_download():
        _install_update(sd_selector, display, dropped_file)

    download_thread = threading.Thread(target=start_formatting, args=(sd_selector, display, call_download))
    download_thread.start()


def _install_update(sd_selector, display,dropped_file):
    if dropped_file != None:
        display.message("Installing "+ dropped_file)
        #unzip_file(sd_selector,dropped_file,display)

        download_thread = threading.Thread(target=unzip_file, args=(sd_selector, dropped_file, display))
        download_thread.start()

    else:
        try:
            local_filename = os.path.join(sd_selector[0].get(), 'spruce.zip')

            display.message("Starting download...")

            response = requests.get(get_latest_release_link(display), stream=True)
            response.raise_for_status()


            total_size = int(response.headers.get("Content-Length", 0))
            downloaded_size = 0

            chunk_size = 1024
            update_interval = 9 * 1024 * 1024
            last_update = 0

            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # Aggiorna la terminale ogni volta che sono stati scaricati almeno 3 MB
                        if downloaded_size - last_update >= update_interval:
                            display.message(f"{downloaded_size / (1024 * 1024):.0f}/{total_size / (1024 * 1024):.0f} MB")
                            last_update = downloaded_size

            display.message("Download completed, unzipping!")
            #unzip_file(sd_selector,local_filename,display)
            download_thread = threading.Thread(target=unzip_file, args=(sd_selector, dropped_file, display))
            download_thread.start()

        except Exception as e:
            display.message("Exception:", e)


def unzip_file(sd_selector, local_filename,display):
    display.message("Unzipping file...")
    extract_path = os.path.join(sd_selector[0].get())

    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    display.message("Checking if file is .zip or .7z...")
    if local_filename.endswith('.zip'):
        display.message("Unzippung .zip file...")
        with zipfile.ZipFile(local_filename, 'r') as z:
            z.extractall(path=extract_path)
    elif local_filename.endswith('.7z'):
        display.message("Unzippung .7z file... Be patient\nit can take some time...")
        with py7zr.SevenZipFile(local_filename, mode='r') as z:
            z.extractall(path=extract_path)
    else:
        raise ValueError("File format not supported")

    try:
        os.remove(local_filename)
        # TODO: EJECT
        #eject_sd(sd_selector[0].get(), sd_selector[0], sd_selector, display)
        display.message("Done! Enjoy your spruce\nand check for firmware updates!")
    except:
        pass
