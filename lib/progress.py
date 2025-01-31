class ProgressHandler:
    def __init__(self, zipfile, display):
        self.zipfile = zipfile
        self.display = display
        self.total_files = len(self.zipfile.namelist())
        self.extracted_files = 0
        self.last_update = 0
        # Aggiorniamo ogni 3.69%
        self.update_interval = max(1, int(self.total_files / 27.1))

    def extract_with_progress(self, member, path):
        self.zipfile.extract(member, path)
        self.extracted_files += 1
        
        # Aggiorna il display solo ogni update_interval files
        if (self.extracted_files - self.last_update) >= self.update_interval:
            progress = (self.extracted_files / self.total_files) * 100
            self.display.message(f"Excrating: {progress:.1f}% ({self.extracted_files}/{self.total_files} files)")
            self.last_update = self.extracted_files