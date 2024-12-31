'''
In this file you'll find some useful variables
and functions you may need elsewhere.

To use these just import this file like this:

                import lib.spruce as spruce

Then you can call any function like this:

                spruce.any_function()

Or get global variable like this:

                spruce.app                # returns string of current app
'''

app = "sd" # Stores the name of the app we're currently on
device = "a30" # Stores the name of the currently selected device
terminal = None # Stores a terminal. TODO: make it a vector
window_geometry = None # Stores window information

#importing things we need to make these functions work
import os
import requests
from pathlib import Path
import tkinter as tk


def download_file(url, path):
    """
    Downloads a file from the given URL and saves it in the specified path.
    The path is relative to the user's home directory, inside the '.spruce_cp' folder.

    Args:
    - url (str): The URL to download the file from.
    - path (str): The relative path to save the file within the '.spruce_cp' directory.

    Returns:
    - str: The full path where the file was saved, or an error message if the download fails.
    """
    # Define the base directory as the .spruce_cp folder inside the user's home directory
    download_dir = Path.home() / ".spruce_cp"

    # Ensure the directory exists
    download_dir.mkdir(parents=True, exist_ok=True)

    # Combine the specified path with the directory
    file_path = download_dir / path

    try:
        # Make an HTTP GET request to download the file
        with requests.get(url, stream=True) as response:
            # Raise an error if the request was not successful
            response.raise_for_status()

            # Write the content to the file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

        return str(file_path)

    except requests.exceptions.RequestException as e:
        return f"Error downloading file: {e}"
