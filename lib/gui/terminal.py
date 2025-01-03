from PIL import Image, ImageTk
from lib.gui.context import context
import tkinter as tk
import tkinter.font as tkfont
import textwrap

# Subclass for custom Canvas that includes 'text_items' and other stuff
class TerminalCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # Initialize 'text_items' as an empty list
        self.text_items = []
        self.cancelled = False  # Flag to cancel  the action
        self.cancel_container = None  # Cancel button container
        self.confirm_container = None  # Confirm button container

    def confirmation(self, message, event):
        '''
        Shows a confirmation message at the bottom-right of the canvas with two buttons:
        - "Cancel" with a Cancel icon
        - "Confirm" with a Confirm icon
        '''
        self.cancelled = False  # Restore flag when new confirm message is called

        self.message(message)
        width = self.winfo_width()
        height = self.winfo_height()

        # Upload and resize Cancel and Confirm images
        cancel_image = Image.open("res/gui/icon-b.png")
        confirm_image = Image.open("res/gui/icon-a.png")
        cancel_image_resized = cancel_image.resize((16, 16))
        confirm_image_resized = confirm_image.resize((16, 16))

        # Convert images in PhotoImage objects compatible with Tkinter
        root = context.get_root()

        cancel_img_tk = ImageTk.PhotoImage(cancel_image_resized)
        self.cancel_container = tk.Frame(self, bd=0)  # Cancel button container
        self.cancel_container.place(x=width - 139, y=height - 22, anchor="nw")
        cancel_img = tk.Label(self.cancel_container, image=cancel_img_tk)
        cancel_img.pack(side="left")
        cancel_text = tk.Label(self.cancel_container, text="Cancel", font=("Arial", 12), fg="#7c6f64")
        cancel_text.pack(side="left")

        confirm_img_tk = ImageTk.PhotoImage(confirm_image_resized)
        self.confirm_container = tk.Frame(self, bd=0)  # Confirm button container
        confirm_img = tk.Label(self.confirm_container, image=confirm_img_tk)
        confirm_img.pack(side="left")
        confirm_text = tk.Label(self.confirm_container, text="Confirm", font=("Arial", 12), fg="#7c6f64")
        confirm_text.pack(side="left")

        self.confirm_container.place(x=width - 71, y=height - 22, anchor="nw")

        # Save references to avoid garbage collection
        root.cancel_img_tk = cancel_img_tk
        root.confirm_img_tk = confirm_img_tk

        # Activate button click events
        self.cancel_container.bind("<Button-1>", lambda e: self._on_cancel())
        self.confirm_container.bind("<Button-1>", lambda e: self._on_confirm(event))

        # Activate keyboard click events [Cancel (B) / Confirm (A)]
        root.bind("<b>", lambda e: self._on_cancel())
        root.bind("<a>", lambda e: self._on_confirm(event))


    def _on_cancel(self):
            '''Handler for cancel action'''
            if self.cancelled:
                print("Action was cancelled earlier, nothing will happen.")
                return  # Don't execute anything if user clicked cancel

            self.cancelled = True  # set flag on True when action is cancelled
            print("Action cancelled")  # Log or perform any action upon cancellation.
            #self.destroy()
            self.message("")

            # Remove cancel and confirm buttons
            if self.cancel_container:
                self.cancel_container.destroy()
            if self.confirm_container:
                self.confirm_container.destroy()

            # Recreate terminal as default (gotta look into this)
            #self.recreate_terminal()

    def _on_confirm(self, event):
        '''Handler for confirm action'''
        if self.cancelled:
            print("Action was cancelled earlier, nothing will happen.")
            return  # Don't execute anything if user clicked cancel
        self.message("Action confirmed!")
        print("Action confirmed")  # Log or perform any action upon confirmation.
        event()

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
        font_size = 14
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

    def recreate_terminal(self):
        '''
        Recreate the terminal (without the confirmation buttons).
        '''
        root = context.get_root()

        # Custom canvas creation (using TerminalCanvas subclass)
        terminal_canvas = TerminalCanvas(root, height=155)

        # Pack the terminal to the top or bottom as needed
        terminal_canvas.pack(fill="both", expand=True, side="top", pady=2)

        # Load and display the logo image
        logo_image = Image.open("res/gui/terminal_bg.png")
        resized_image = logo_image.resize((155, 155))

        root.logo_img = ImageTk.PhotoImage(resized_image)  # Store the reference in root
        terminal_canvas.create_image(75, 10, anchor="nw", image=root.logo_img)

        return terminal_canvas

def create(container_side="top"):
    '''
    Creates a display container that simulates a spruce device, use this to display messages to the user like it is a terminal (with append_terminal_message).

    Args:
    - side (str) (optional): set to "bottom" to move the element to the bottom

    Returns:
    - Canvas: A container used as a terminal to display messages
    '''
    root = context.get_root()

    # Custom canvas creation (using TerminalCanvas subclass)
    terminal_canvas = TerminalCanvas(root, height=155)

    if container_side == "bottom":
        terminal_canvas.pack(fill="both", expand=True, side=container_side, pady=2)
    else:
        terminal_canvas.pack(fill="both", expand=True, side="top", pady=2)

    # Load and display the logo image
    logo_image = Image.open("res/gui/terminal_bg.png")
    resized_image = logo_image.resize((155, 155))

    root.logo_img = ImageTk.PhotoImage(resized_image)  # Store the reference in root
    terminal_canvas.create_image(75, 10, anchor="nw", image=root.logo_img)

    return terminal_canvas
