'''
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
