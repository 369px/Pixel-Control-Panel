''' from wiki:
Unbricking an A30

    Download and Extract the Unbricker Image.

    Using Rufus, flash the Unbricker as a bootable image onto a fresh microSD card formatting it to FAT32.

    Eject your card and insert it into your A30.

    Plug your A30 into a charger and power it on. The Miyoo boot logo will appear and then get fuzzy side to side slowly covering the entire screen. It is totally normal, it looks scary. DO NOT POWER IT OFF AT ANY POINT DURING THIS PROCESS. It will eventually turn itself off.

Screenshot 2024-11-20 175821

    Power on the A30.

    Install spruce (or reinsert your old spruce card) and update the Firmware (version 3.0.0 and above have a built in firmware updater app).

'''

from lib.sd_card import format_sd_card

def flash_unbricker():
    return
