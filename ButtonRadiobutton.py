import tkinter as tk

navy_blue = '#1D1D3A'
vibrant_blue = '#194AFE'
purple = '#6921B5'


# Button class used for changing pages
class ButtonRadiobutton(tk.Button):
    def selectBtn(self):
        self.config(background=vibrant_blue)

    def unselectBtn(self):
        self.config(background=navy_blue)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(background=navy_blue, borderwidth=0, font=("Sen",14,"bold"),
                    foreground='white', relief='flat', width=40)
