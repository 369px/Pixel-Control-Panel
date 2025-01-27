import subprocess
import os
import time
import psutil

class USBFlasher:
    def __init__(self, exe_path="lib/flashlib.exe"):
        self.exe_path = exe_path
        if not os.path.exists(exe_path):
            raise FileNotFoundError(f"Eseguibile non trovato: {exe_path}")


    def dismount_volume(self, drive_letter: str):
        """Smonta un volume Windows in modo sicuro."""
        try:
            # Rimuovi il : se presente
            drive_letter = drive_letter.rstrip(':')

            # Usa mountvol per smontare
            cmd = f'mountvol {drive_letter}: /P'
            subprocess.run(cmd, shell=True, check=True)
            time.sleep(2)  # Attendi che Windows completi l'operazione
            return True
        except subprocess.CalledProcessError:
            return False

    def flash(self, image_path: str, drive_letter: str) -> bool:
        if not os.path.exists(image_path):
            raise ValueError(f"Image file not found: {image_path}")

        drive_letter = drive_letter.strip().rstrip(':')

        # chiudi processi #
        for proc in psutil.process_iter(['pid', 'name', 'open_files']):
            try:
                # Controlla i file aperti dal processo
                open_files = proc.info.get('open_files')
                if open_files:
                    for file in open_files:
                        if file.path.startswith(drive_letter):
                            print(f"Processo trovato: {proc.info['name']} (PID: {proc.info['pid']}) sta utilizzando {file.path}")

                            # Termina il processo
                            os.kill(proc.info['pid'], 9)
                            print(f"Processo {proc.info['name']} terminato.")
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

        try:
            start_time = time.time()

            process = subprocess.Popen(
                [self.exe_path, image_path, drive_letter],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate(input="\n")
            elapsed = time.time() - start_time

            if "Scrittura completata" in stdout or "Write completed" in stdout:
                print(f"\nFlash completato in {elapsed:.2f} secondi!")
                return True
            else:
                print("Errore durante il flash:")
                print(stdout)
                if stderr:
                    print("Stderr:", stderr)
                return False

        except subprocess.CalledProcessError as e:
            print(f"Errore nell'esecuzione del programma: {e}")
            return False
        except Exception as e:
            print(f"Errore inaspettato: {e}")
            if hasattr(e, 'stderr'):
                print("Stderr:", e.stderr)
            return False

class USBFlasher_macos:
    def __init__(self, exe_path="lib/flashlib_mac"):
        self.exe_path = exe_path
        if not os.path.exists(exe_path):
            raise FileNotFoundError(f"Eseguibile non trovato: {exe_path}")

    def unmount_volume(self, device_path: str):
        """Smonta un volume su macOS in modo sicuro."""
        try:
            cmd = ['diskutil', 'unmountDisk', device_path]
            subprocess.run(cmd, check=True)
            time.sleep(2)  # Attendi che macOS completi l'operazione
            return True
        except subprocess.CalledProcessError:
            return False

    def flash(self, image_path: str, device_path: str) -> bool:
        if not os.path.exists(image_path):
            raise ValueError(f"File immagine non trovato: {image_path}")

        # Chiudi processi che potrebbero utilizzare il dispositivo
        for proc in psutil.process_iter(['pid', 'name', 'open_files']):
            try:
                open_files = proc.info.get('open_files')
                if open_files:
                    for file in open_files:
                        if file.path.startswith(device_path):
                            print(f"Processo trovato: {proc.info['name']} (PID: {proc.info['pid']}) sta utilizzando {file.path}")
                            os.kill(proc.info['pid'], 9)
                            print(f"Processo {proc.info['name']} terminato.")
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

        # Smonta il volume
        if not self.unmount_volume(device_path):
            print(f"Impossibile smontare il dispositivo: {device_path}")
            return False

        try:
            start_time = time.time()

            process = subprocess.Popen(
                [self.exe_path, image_path, device_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate(input="\n")
            elapsed = time.time() - start_time

            if "Scrittura completata" in stdout or "Write completed" in stdout:
                print(f"\nFlash completato in {elapsed:.2f} secondi!")
                return True
            else:
                print("Errore durante il flash:")
                print(stdout)
                if stderr:
                    print("Stderr:", stderr)
                return False

        except subprocess.CalledProcessError as e:
            print(f"Errore nell'esecuzione del programma: {e}")
            return False
        except Exception as e:
            print(f"Errore inaspettato: {e}")
            if hasattr(e, 'stderr'):
                print("Stderr:", e.stderr)
            return False
