
from PIL import Image, ImageTk
from lib.gui.context import context
import lib.gui.style as ui
import tkinter as tk
import tkinter.font as tkfont
import textwrap

# Subclass for custom Canvas that includes 'text_items' and other stuff
# To look like a spruce device
class TerminalCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # Inizializza 'text_items' come una lista vuota
        self.text_items = []

    def confirmation(self,message):
        '''
        Shows a confirmation message.
        '''
        self.message(message)
        yes = tk.Frame(self)
        yes.pack(fill="none", expand=False, side="left")
        label = tk.Label(yes, text="Yes")
        label.pack(fill="both", expand=True)

    def message(self, message: str, x=1, y=1):
        '''
        Clears the display container and shows a new message.

        Args:
        - message (str): the string you want to display
        - x (int) (optional): x position of the text
        - y (int) (optional): y position of the text
        '''
        width = self.winfo_width()
        height = self.winfo_height()

        # Create a font object to measure text width
        font_size = 12
        font = tkfont.Font(family="Arial", size=font_size)

        # Calculate max number of chars per line based on max width
        char_width = font.measure("a")
        max_width = width
        max_chars_per_line = max_width // char_width

        # Split message by \n and wrap each line
        lines = message.split("\n")
        wrapped_lines = []
        for line in lines:
            wrapped_lines.extend(textwrap.wrap(line, width=max_chars_per_line))

        # Delete previous text if it exists
        if hasattr(self, 'text_items') and self.text_items:
            for item in self.text_items:
                self.delete(item)

        # Center text block
        block_height = len(wrapped_lines) * font_size
        y_start = (height // 2) - (block_height // 2)

        # Draw each row centered
        self.text_items = []
        for i, line in enumerate(wrapped_lines):
            y_line = y_start + i * font_size
            text_item = self.create_text(
                width // 2, y_line, text=line, font=("Arial", font_size), fill="#ebdbb2", anchor="center"
            )
            self.text_items.append(text_item)

def create(container_side="top"):
    '''
    Creates a display container that simulates a spruce device, use this to display messages to the user like it is a terminal (with append_terminal_message).

    Args:
    - side (str) (optional): set to "bottom" to move the element to the bottom

    Returns:
    - Canvas: A container used as a terminal to display messages
    '''
    root = context.get_root()

    # Creazione del canvas personalizzato (usando la sottoclasse TerminalCanvas)
    terminal_canvas = TerminalCanvas(root, height=155)

    if container_side == "bottom":
        terminal_canvas.pack(fill="x", expand=True, side=container_side)
    else:
        terminal_canvas.pack(fill="x", expand=True, side="top")

    # Load and display the logo image
    logo_image = Image.open("res/gui/terminal_bg.png")
    resized_image = logo_image.resize((155, 155))

    root.logo_img = ImageTk.PhotoImage(resized_image)  # Store the reference in root
    terminal_canvas.create_image(75, 0, anchor="nw", image=root.logo_img)  # Posiziona l'immagine in alto a sinistra

    return terminal_canvas
