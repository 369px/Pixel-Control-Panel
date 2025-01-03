#OUTDATED, PLEASE IGNORE
'''
# First thing you need to do when making an app is import these files
# from the gui library (still WIP, may change in the future)
from lib.gui import style as ui, terminal

# Then add a _main(root) function which will be where you make your GUI
def _main(root):

    # The first thing I suggest you to have is a display where you can
    # output messgaes to the user, create it by adding this line:
    display = terminal.create() # "lib/gui/terminal.py" for more info

    # To add a button just do this
    # this will be a stock button that does nothing
    button1 = ui.create_list_btn()

    # If you just pass a string inside it you can customize the label
    button2 = ui.create_list_btn("Custom label")

    # To add an event to it, you can do it by passing a "command" attribute
    # and giving it a custom function after the "lambda:" part.
    # Here we just use "display.message" to prompt a message on the
    # display me made earlier. Click button 3 and see what it does.
    button3 = ui.create_list_btn(
        text="Click to show message on terminal",
        command=lambda: display.message("Displaying messages is easy!")
    )

    # buttons have other attributes you can pass to customize them
    # here's all of them
    button4 = ui.create_list_btn(
        text="Click to show message on terminal",
        command=lambda: display.message("Displaying messages is easy!")
    )
'''
