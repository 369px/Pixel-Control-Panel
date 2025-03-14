import requests, os, zipfile, threading, asyncio, subprocess, time
import zipfile, py7zr

from apps.sd_flasher.update import get_latest_release_link
from apps.sd_flasher.format import start_formatting

def start_installing(sd_selector, display, dropped_file):
    # Start download on a different thread

    def call_download():
        _install_update(sd_selector, display, dropped_file)

    download_thread = threading.Thread(target=start_formatting, args=(sd_selector, display, call_download))
    download_thread.start()


def _install_update(sd_selector, display, dropped_file):
    if dropped_file is not None:
        display.message("Installing " + dropped_file)
        # unzip_file(sd_selector, dropped_file, display)

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
            update_interval = 9 * 1024 * 1024  # 9MB
            last_update = 0
            start_time = time.time()  # Tempo di inizio per calcolare la velocità e il tempo rimanente

            # Funzione per calcolare il tempo rimanente
            def update_progress():
                nonlocal downloaded_size
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    speed = downloaded_size / elapsed_time  # Velocità di download in byte/s
                    remaining_size = total_size - downloaded_size
                    remaining_time = remaining_size / speed if speed > 0 else 0
                    remaining_minutes = remaining_time / 60  # Tempo rimanente in minuti

                    # Mostra il progresso
                    display.message(f"{downloaded_size / (1024 * 1024):.0f}/{total_size / (1024 * 1024):.0f} MB\n"
                                    f"{int(remaining_minutes)} minutes left...")

            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # Aggiorna la terminale ogni volta che sono stati scaricati almeno 9 MB
                        if downloaded_size - last_update >= update_interval:
                            update_progress()  # Chiamata per mostrare il progresso
                            last_update = downloaded_size

            display.message("Download completed, unzipping!")
            # unzip_file(sd_selector, local_filename, display)
            download_thread = threading.Thread(target=unzip_file, args=(sd_selector, local_filename, display))
            download_thread.start()

        except Exception as e:
            display.message("Exception: "+str(e))


def unzip_file(sd_selector, local_filename, display):
    try:
        display.message("Unzipping file...")
        extract_path = os.path.join(sd_selector[0].get())

        if not os.path.exists(extract_path):
            os.makedirs(extract_path)

        display.message("Checking if file is .zip or .7z...")

        # Funzione per calcolare il tempo rimanente e il progresso
        def update_progress(total_size, extracted_size, start_time, last_update_time):
            # Calcola tempo trascorso e velocità di estrazione
            elapsed_time = time.time() - start_time
            speed = extracted_size / elapsed_time if elapsed_time > 0 else 0
            remaining_size = total_size - extracted_size
            remaining_time = remaining_size / speed if speed > 0 else 0
            remaining_mb = remaining_size / (1024 * 1024)  # MB rimanenti
            remaining_minutes = remaining_time / 60  # Tempo rimanente in minuti

            # Aggiorna solo se è passato abbastanza tempo (ad esempio ogni 3 secondi)
            if time.time() - last_update_time > 3:
                # Messaggio di progresso
                display.message(f"Unzipping file...\n{int(remaining_minutes)} minutes left\n"
                                f"{int(extracted_size / (1024 * 1024))}/{int(total_size / (1024 * 1024))} MB extracted")
                return time.time()  # Restituisci il tempo dell'ultimo aggiornamento
            return last_update_time

        # Estrazione file .zip
        if local_filename.endswith('.zip'):
            display.message("Unzipping .zip file...")
            with zipfile.ZipFile(local_filename, 'r') as z:
                total_size = sum([file.file_size for file in z.infolist()])  # Calcola la dimensione totale
                extracted_size = 0
                start_time = time.time()
                last_update_time = start_time

                for file in z.infolist():
                    z.extract(file, extract_path)
                    extracted_size += file.file_size
                    last_update_time = update_progress(total_size, extracted_size, start_time, last_update_time)

        # Estrazione file .7z
        elif local_filename.endswith('.7z'):
            display.message("Unzipping .7z file...")
            with py7zr.SevenZipFile(local_filename, mode='r') as z:
                total_size = sum([file.uncompressed for file in z.list()])  # Calcola la dimensione totale
                extracted_size = 0
                start_time = time.time()
                last_update_time = start_time

                for file in z.list():
                    z.extract(targets=[file.filename], path=extract_path)  # file.filename è il nome del file
                    extracted_size += file.uncompressed  # file.size è la dimensione
                    last_update_time = update_progress(total_size, extracted_size, start_time, last_update_time)

        else:
            raise ValueError("File format not supported")

        # Rimuovere il file dopo l'estrazione

        os.remove(local_filename)
        # TODO: EJECT
        # eject_sd(sd_selector[0].get(), sd_selector[0], sd_selector, display)
        display.message("Done! Enjoy your spruce\nand check for firmware updates!")
    except Exception as e:
        display.message("Exception:"+str(e))
