import tkinter as tk


# Button class used for changing pages
class ButtonRadiobutton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(
            font=('Verdana', 10),
            # activebackground='lightgrey',
            background='lightgrey',
            foreground='black',
            borderwidth=0,
            width=36
        )
