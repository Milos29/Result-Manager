import tkinter as tk
from tkinter import ttk

titleBarColor = "#F3F3F3"


class LongMessageBox(tk.Toplevel):
    def onClose(self):
        self.destroy()

    def startMove(self, event):
        self.x = event.x
        self.y = event.y

    def move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.geometry(f"+{self.winfo_x() + dx}+{self.winfo_y() + dy}")

    def __init__(self, width: int, height: int, x: int, y: int, title: str) -> None:
        super().__init__()
        self.resizable(False, False)

        self.overrideredirect(True)
        self.geometry("%dx%d+%d+%d" % (width, height, x, y))

        self.transient()
        self.grab_set()

        titleBar = tk.Frame(self, bg=titleBarColor, height=40, relief="raised", bd=0)
        titleBar.pack(fill="x")
        titleBar.pack_propagate(False)

        titleLabel = tk.Label(titleBar, text=title, bg=titleBarColor, fg="black")
        titleLabel.pack(side="left", padx=20)

        titleBar.bind("<Button-1>", self.startMove)
        titleBar.bind("<B1-Motion>", self.move)

        titleLabel.bind("<Button-1>", self.startMove)
        titleLabel.bind("<B1-Motion>", self.move)

        closeButton = tk.Button(titleBar, text="✕", height=30, bg=titleBarColor, fg="black",
                                bd=0, command=self.onClose, activebackground="red", activeforeground="white")
        closeButton.pack(side="right", ipadx=15)

        def onHover(e):
            closeButton["bg"] = "red"
            closeButton["fg"] = "white"

        def onLeave(e):
            closeButton["bg"] = titleBarColor
            closeButton["fg"] = "black"

        closeButton.bind("<Enter>", onHover)
        closeButton.bind("<Leave>", onLeave)


def showLongInfo(width: int, height: int, x: int, y: int, title: str, msg: str) -> None:
    window = LongMessageBox(width, height, x, y, title)

    text = tk.Text(window, wrap="word")
    text.insert("1.0", msg)
    text.config(state="disabled")
    text.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(window, command=text.yview)
    scrollbar.pack(side="right", fill="y", pady=10)
    text.config(yscrollcommand=scrollbar.set)
