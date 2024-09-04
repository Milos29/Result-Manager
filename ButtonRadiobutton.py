import tkinter as tk


# Button class used for changing pages
class ButtonRadiobutton(tk.Button):
    def selectBtn(self):
        self.config(background="lightblue")

    def unselectBtn(self):
        self.config(background="lightgrey")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(background='lightgrey', borderwidth=0, font=('Segoe UI', 10),
                    foreground='black', relief='flat', width=40)
