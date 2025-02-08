from PIL import Image, ImageTk
from lib.gui.context import context
import tkinter as tk
import tkinter.font as tkfont
from tkinterdnd2 import TkinterDnD, DND_FILES
import textwrap

# Subclass for custom Canvas that includes 'text_items' and other stuff
class TerminalCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bd=0, highlightthickness=0)  # Remove borders
        # Initialize 'text_items' as an empty list
        self.text_items = []
        self.cancelled = False  # Flag to cancel the action
        self.cancel_container = None  # Cancel button container
        self.confirm_container = None  # Confirm button container
        self.input_entry = None
        self.dropped_file = None

    def confirmation(self, message, event):
        '''
        Shows a confirmation message at the bottom-right of the canvas with two buttons:
        - "Cancel" with a Cancel icon
        - "Confirm" with a Confirm icon
        '''
        self.destroy_elements()
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
        cancel_img = tk.Label(self.cancel_container, image=cancel_img_tk, bg="#323232")
        cancel_img.pack(side="left")
        cancel_text = tk.Label(self.cancel_container, text="Cancel", font=("Arial", 12), fg="#7c6f64",bg="#323232")
        cancel_text.pack(side="left")

        confirm_img_tk = ImageTk.PhotoImage(confirm_image_resized)
        self.confirm_container = tk.Frame(self, bd=0)  # Confirm button container
        confirm_img = tk.Label(self.confirm_container, image=confirm_img_tk, bg="#323232")
        confirm_img.pack(side="left")
        confirm_text = tk.Label(self.confirm_container, text="Confirm", font=("Arial", 12), fg="#7c6f64",bg="#323232")
        confirm_text.pack(side="left")

        self.confirm_container.place(x=width - 71, y=height - 22, anchor="nw")

        # Save references to avoid garbage collection
        root.cancel_img_tk = cancel_img_tk
        root.confirm_img_tk = confirm_img_tk

        # Activate button click events
        self.cancel_container.bind("<Button-1>", lambda e: self._on_cancel())

        # Pass the file path when confirming
        self.confirm_container.bind("<Button-1>", lambda e: self._on_confirm(event))

        # Activate keyboard click events [Cancel (B) / Confirm (A)]
        root.bind("<b>", lambda e: self._on_cancel())
        root.bind("<a>", lambda e: self._on_confirm(event))

        # Set up file drop handling for drag-and-drop event
        _setup_file_drop(self,event)


    def _on_confirm(self, event):
        '''Handler for confirm action'''
        if self.cancelled:
            print("Action was cancelled earlier, nothing will happen.")
            return  # Don't execute anything if user clicked cancel

        if self.dropped_file:
            self.message(f"Action confirmed with file: {self.dropped_file}")
            print(f"Action confirmed with file: {self.dropped_file}")
        else:
            self.message("Action confirmed!")
            print("Action confirmed")

        event()  # Call the passed event handler, potentially with the file path

    def _on_cancel(self):
        '''Handler for cancel action'''


        if self.cancelled:
            print("Action was cancelled earlier, nothing will happen.")
            return  # Don't execute anything if user clicked cancel

        self.cancelled = True  # set flag to True when action is cancelled

        self.destroy_elements()

        print("Action cancelled")  # Log or perform any action upon cancellation.

    def destroy_elements(self):
        if self.cancel_container:
            self.cancel_container.destroy()
        if self.confirm_container:
            self.confirm_container.destroy()
        if self.input_entry:
            self.input_entry.destroy()
            return

        # Clear the message and remove buttons
        self.message("")

        # Unbind keyboard keys (Cancel - 'B' and Confirm - 'A')
        root = context.get_root()
        root.unbind("<b>")
        root.unbind("<a>")
        root.unbind("<Return>")

        # Unbind <<Drop>> event from root widget to disable drop functionality
        print("Unbinding <<Drop>> event...")
        root.dnd_bind('<<Drop>>', None)  # Unbind the drop event

        print("Elements destroyed and events unbound.")

    def user_input(self, message: str, callback, type="text", x=1, y=1):
        """
        Displays a message and an input container (Entry) to the user,
        Returns input only when user clicks "Enter".

        Args:
        - message (str): message to view
        - callback (function): function to call when user clicks enter
        - x (int) (optional): text x position
        - y (int) (optional): text y position
        """
        self.destroy_elements()
        self.cancelled = False
        width = self.winfo_width()
        height = self.winfo_height()

        # Creates a font for the message
        font_size = 14
        font = tkfont.Font(family="Arial", size=font_size)

        # Creates the message
        self.message(message, x, y)

        # Create input field for password (showing "*" characters for security)
        self.input_var = tk.StringVar()
        if type == "text":
            self.input_entry = tk.Entry(self, textvariable=self.input_var, font=("Arial", font_size), bd=1, highlightthickness=1)
        else:
            self.input_entry = tk.Entry(self, textvariable=self.input_var, font=("Arial", font_size), bd=1, highlightthickness=1, show='*')  # Hide text with '*'

        self.input_entry.place(x=width // 2, y=y + 125, anchor="center")

        # callback function that runs when user clicks "Enter"
        def on_enter(event):
            user_input = self.input_var.get()
            self.destroy_elements()
            callback(user_input)  # runs callback with user input

        # Bind per la pressione del tasto "Enter"
        self.input_entry.bind("<Return>", on_enter)


        def set_focus_when_clicked():
            if self.input_entry:
                #il codice entra qui dentro ma focus e focus set non funzionano
                self.input_entry.focus()
                self.input_entry.focus_set()

        self.input_entry.bind("<Button-1>", lambda e: set_focus_when_clicked())

        # Impostare il focus sull'input per facilitare la digitazione
        self.input_entry.focus()

    def message(self, message: str, x=1, y=1):
        '''
        Clears the display container and shows a new message.

        Args:
        - message (str): the string you want to display
        - x (int) (optional): x position of the text
        - y (int) (optional): y position of the text
        '''
        self.cancelled = False
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
    terminal_canvas = TerminalCanvas(root, height=155, bg="#323232")

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

def _setup_file_drop(self, confirm_event):
    '''Sets up the drag-and-drop event listener.'''

    def on_file_drop(event):
        """Handle the dropped file."""
        if self.dropped_file:  # Check if a file was already dropped
            print(f"File already dropped: {self.dropped_file}... that's weird... line 285 lib/gui/terminal.py")
        else:
            self.dropped_file = event.data  # Store the dropped file path
            print(f"File dropped: {self.dropped_file}")

        # Trigger the confirmation with the file path
        confirm_event(self.dropped_file)  # Pass the dropped file to the confirmation handler

    # Register drop target and bind event to root
    root = context.get_root()
    root.drop_target_register(DND_FILES)
    print("Registering <<Drop>> event...")
    root.dnd_bind('<<Drop>>', on_file_drop)  # Bind drop event
