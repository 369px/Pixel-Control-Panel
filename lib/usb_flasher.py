import subprocess
import os
import time

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
        
        # Prima smonta il volume
        print(f"Smontaggio del volume {drive_letter}...")
        if not self.dismount_volume(drive_letter):
            print("Attenzione: Impossibile smontare il volume. Provo comunque a procedere...")
        
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
