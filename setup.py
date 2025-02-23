from setuptools import setup

APP = ['main.py']  # Sostituisci con il nome del tuo script
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'res/icon.png'  # Icona dell'app, opzionale
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
