# lib/gui_context.py
# used to manage context and remove need of passing "root" everytime
# call this:
    #
    #  root = context.get_root()
    #
# in a function to automatically get the root from the context

import tkinter as tk

class GUIContext:
    def __init__(self):
        self.root = None

    def set_root(self, root):
        self.root = root

    def get_root(self):
        if not self.root:
            raise RuntimeError("Root has not been set!")
        return self.root


# Create a globale istance to manage context
context = GUIContext()
