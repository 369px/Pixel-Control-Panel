import os
import platform
import subprocess

def detect_sd_card():
    """Detect connected SD Cards."""
    devices = []
    if platform.system() == "Windows":
        drives = [f"{chr(letter)}:\\" for letter in range(65, 91) if os.path.exists(f"{chr(letter)}:\\")]
        for drive in drives:
            if "Removable" in os.popen(f"vol {drive}").read():
                devices.append(drive)
    elif platform.system() == "Darwin":
        volumes = [os.path.join("/Volumes", d) for d in os.listdir("/Volumes") if os.path.ismount(os.path.join("/Volumes", d))]
        devices.extend(volumes)
    elif platform.system() == "Linux":
        user = os.getenv("USER", "default_user")
        media_path = f"/media/{user}"
        if os.path.exists(media_path):
            devices.extend([os.path.join(media_path, d) for d in os.listdir(media_path)])
    return devices

def get_disk_identifier(volume_path):
    result = subprocess.run(['diskutil', 'info', volume_path], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith('   Device Identifier'):
            return line.split(':')[1].strip()
    return None
