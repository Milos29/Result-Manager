from pdf import *

from InOut import *

from clipboard import copyToClipboard

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font

FONT1 = ("Verdana", 35)
SettingsFont = ('Verdana', 15)
SettingsFontSmaller = ('Verdana', 10)
ListFont = ('Arial', 10)

windowWidth = 0
windowHeight = 0
currentPageNumber = 0
filePath = ""

listOfResults = list()
data = dict()
yearAdm = 0
year = 0
subjects = dict()


def setWindowSize(wt, ht):
    global windowWidth, windowHeight
    windowWidth = wt
    windowHeight = ht


class tkinterApp(tk.Tk):
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        wp = 0.839  # procenat sirine ekrana
        hp = 0.7  # procenat duzine ekrana
        fw = self.winfo_screenwidth()
        fh = self.winfo_screenheight()
        setWindowSize(int(fw * wp), int(fh * hp))
        self.geometry("%dx%d+%d+%d" % (windowWidth, windowHeight, fw * (1 - wp) / 2, fh * (1 - hp) / 2))
        self.maxsize(windowWidth, windowHeight)
        self.minsize(windowWidth, windowHeight)
        self.iconbitmap("images/icon1.ico")
        self.title("Lista")

        def on_form_loaded():
            global yearAdm, year, listOfResults, subjects, data
            yearAdm, year = loadSettings()
            listOfResults = loadListOfResults()
            data = loadResults()
            subjects = loadSubjects()

        def on_closing():
            self.destroy()
            # ||||||||||||||||||||||||
            saveData(data)

            saveSettings(yearAdm, year)
            saveListOfResults(listOfResults)

        on_form_loaded()
        self.protocol("WM_DELETE_WINDOW", func=on_closing)

        container1 = tk.Frame(self)
        cnt1h = 30
        container1.place(height=cnt1h, width=fw)

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

        radio1 = ButtonRadiobutton(self, text='Lista', command=lambda: showCurrentPage(1))
        radio1.grid(row=0, column=0, padx=0, pady=0)

        radio2 = ButtonRadiobutton(self, text='Rokovi', command=lambda: showCurrentPage(2))
        radio2.grid(row=0, column=1, padx=0, pady=0)

        radio3 = ButtonRadiobutton(self, text='Dodaj rok', command=lambda: showCurrentPage(3))
        radio3.grid(row=0, column=2, padx=0, pady=0)

        radio4 = ButtonRadiobutton(self, text='Podesavanja', command=lambda: showCurrentPage(4))
        radio4.grid(row=0, column=3, padx=0, pady=0)

        rbs = [radio1, radio2, radio3, radio4]
        pages = [Page1, Page2, Page3, Page4]

        container = tk.Frame(self)
        container.place(height=fh - cnt1h, width=fw, y=cnt1h)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in pages:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        def showCurrentPage(val):
            if val < 1 or val > 4:
                val = 1
            global currentPageNumber
            if currentPageNumber == val:
                return
            rbs[currentPageNumber - 1].config(background='lightgrey')
            rbs[val - 1].config(background='lightblue')
            currentPageNumber = val
            self.show_frame(pages[currentPageNumber - 1])

        showCurrentPage(1)


class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.update()
        style = ttk.Style()
        style.configure('Custom.TEntry', foreground='blue', background='lightyellow', borderwidth=2)
        container = tk.Frame(self, width=600, height=400)
        container.place(x=0.02 * windowWidth, y=0.05 * windowHeight, w=windowWidth * 0.91, h=windowHeight * 0.8)
        container.update_idletasks()

        columns = ("", "Indeks") + tuple(
            [f"{x:{4}}" for x in subjects[(year - 1) * 2 + 1]] + [f"{x:{4}}" for x in subjects[(year - 1) * 2 + 2]]) + (
                      "Koeficijent",)
        cw = [35, 80] + (len(columns) - 3) * [60, ] + [100, ]

        scrollbarx = ttk.Scrollbar(container, orient=tk.HORIZONTAL)
        scrollbary = ttk.Scrollbar(container)
        listbox = ttk.Treeview(container, xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set, columns=columns,
                               show="headings")
        scrollbarx.configure(command=listbox.xview)
        scrollbary.configure(command=listbox.yview)
        scrlH = 20
        listbox.place(h=container.winfo_height() - scrlH, w=container.winfo_width() - scrlH, x=0, y=0)
        scrollbarx.place(h=scrlH, w=container.winfo_width() - scrlH, x=0, y=container.winfo_height() - scrlH)
        scrollbary.place(h=container.winfo_height() - scrlH, w=scrlH, x=container.winfo_width() - scrlH, y=0)
        for ind, column in enumerate(columns):
            listbox.heading(column, anchor="e", text=column)
            listbox.column(column, anchor="e", width=cw[ind])
        listbox.heading("#0", text="")

        ListStyle = ttk.Style()
        ListStyle.configure("Treeview", font=ListFont)
        ListStyle.configure("Treeview.Heading", font=ListFont + ("bold",))

        listbox.column(column="Koeficijent", width=int(container.winfo_width() - sum(cw[:-1]) - 22))

        data1 = [("23/0999", 10, 10, 10, 10, 10, 10, "", 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, "", "", "", 11.00),
                 ("23/0898", 9, 9, 9, 9, 9, 9, "", 9, 10, 10, 10, 10, 10, 10, 10, 10, "", 10, "", "", 10.45),
                 ("23/9293", 9, 9, 9, 9, 9, "", 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, "", "", "", 9.90), ]
        data1 *= 60

        data2 = data1.copy()
        ind = 1
        for item in data2:
            koef = "{:5.2f}".format(item[-1])
            listbox.insert("", tk.END, values=(ind,) + item[:-1] + (koef,))
            ind += 1

        def BtnClick():
            dataToCopy = []
            headers = columns[1:]
            dataToCopy.append("       " + "   ".join(headers))
            for item in listbox.get_children():
                row = listbox.item(item)["values"]
                for i1 in range(2, len(row) - 1):
                    if row[i1] != "":
                        row[i1] = "{:4d}".format(int(row[i1]))
                    else:
                        row[i1] = "    "
                row[0] = "{:3d}".format(int(row[0]))
                s = ""
                for r in row[:-1]:
                    r = str(r)
                    s += r + "   "
                s += "{:5.2f}".format(float(row[-1]))
                dataToCopy.append(s)
            data_str = "\n".join(dataToCopy)
            copyToClipboard(data_str)
            btn.config(text="Copied", image=self.okicon)

        self.copyicon = tk.PhotoImage(file="images/copyicon.png")
        self.okicon = tk.PhotoImage(file="images/okicon.png")
        btn = tk.Button(self, text="Copy", image=self.copyicon, compound=tk.LEFT, background="darkgrey",
                        command=BtnClick)
        btn.place(x=0.94 * windowWidth, y=0.01 * windowHeight, w=0.05 * windowWidth)


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Font2 = ("Arial", 10)
        container = tk.Frame(self, width=0.4 * windowWidth, height=0.7 * windowHeight)
        container.place(x=0.05 * windowWidth, y=0.05 * windowHeight)
        container.update_idletasks()

        style = ttk.Style()
        style.configure("Custom.Listbox", font=Font2)
        scrollbarx = ttk.Scrollbar(container, orient=tk.HORIZONTAL)
        scrollbary = ttk.Scrollbar(container)
        listbox = tk.Text(container, wrap="none", xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set)
        scrollbarx.configure(command=listbox.xview)
        scrollbary.configure(command=listbox.yview)
        scrlH = 20
        listbox.place(h=container.winfo_height() - scrlH, w=container.winfo_width() - scrlH, x=0, y=0)
        scrollbarx.place(h=scrlH, w=container.winfo_width() - scrlH, x=0, y=container.winfo_height() - scrlH)
        scrollbary.place(h=container.winfo_height() - scrlH, w=scrlH, x=container.winfo_width() - scrlH, y=0)
        content = ""

        def chooseFile():
            global filePath
            filePath = filedialog.askopenfilename(title="Izaberite fajl", filetypes=(("PDF files", "*.pdf"),))
            listbox.delete("1.0", tk.END)
            nonlocal content
            content = read_pdf(filePath)
            for l1 in content:
                listbox.insert(tk.END, l1 + "\n")

        btnFileChoose = ttk.Button(self, text="Izaberite fajl", command=chooseFile)
        btnFileChoose.place(x=0.2 * windowWidth, y=0.8 * windowHeight)

        lblSemester = tk.Label(self, font=SettingsFontSmaller, text="Semestar")
        lblSemester.place(x=0.5 * windowWidth, y=0.1 * windowHeight, w=100)

        cmbSemester = ttk.Combobox(self, font=SettingsFontSmaller)
        cmbSemester.place(x=0.5 * windowWidth + 100, y=0.1 * windowHeight, width=150, height=30)
        semesters = ["1. semestar", "2. semestar", "3. semestar", "4. semestar",
                     "5. semestar", "6. semestar", "7. semestar", "8. semestar"]
        cmbSemester["values"] = semesters
        cmbSemester.state(["readonly"])
        cmbSemester.current(0)

        lblSubject = tk.Label(self, font=SettingsFontSmaller, text="Predmet")
        lblSubject.place(x=0.5 * windowWidth, y=0.1 * windowHeight + 40, w=100)

        cmbSubject = ttk.Combobox(self, font=SettingsFontSmaller)
        cmbSubject.place(x=0.5 * windowWidth + 100, y=0.1 * windowHeight + 40, width=150, height=30)
        cmbSubject["values"] = subjects[1]
        cmbSubject.state(["readonly"])

        lblTerm = tk.Label(self, font=SettingsFontSmaller, text="Rok")
        lblTerm.place(x=0.5 * windowWidth + 10, y=0.1 * windowHeight + 80, w=100)

        cmbTerm = ttk.Combobox(self, font=SettingsFontSmaller)
        cmbTerm.place(x=0.5 * windowWidth + 100, y=0.1 * windowHeight + 80, width=150, height=30)
        cmbTerm["values"] = ["januar", "februar", "jun", "jul", "avgust", "septembar"]
        cmbTerm.state(["readonly"])

        def on_semester_change(event):
            ind = cmbSemester.current()
            cmbSubject["values"] = subjects[ind + 1]
            cmbSubject.set("")
            cmbTerm.set("")

        cmbSemester.bind("<<ComboboxSelected>>", on_semester_change)

        def addResult():
            if cmbSubject.current() == -1:
                messagebox.showerror("Obavestenje", "Niste izabrali predmet.")
                return
            if cmbSemester.current() == -1:
                messagebox.showerror("Obavestenje", "Niste izabrali semestar.")
                return
            if cmbTerm.current() == -1:
                messagebox.showerror("Obavestenje", "Niste izabrali rok.")
                return
            subject = cmbSubject.get()
            listboxText = listbox.get("1.0", tk.END)
            if len(listboxText) < 11:
                return
            listbox.delete("1.0", tk.END)
            cmbSubject.set("")
            term = cmbTerm.get()[:3]
            fileName = "files/results/" + subject + "-" + term + "-"
            num = 1
            while fileName + str(num) + ".txt" in listOfResults:
                num += 1
            fileName += str(num) + ".txt"
            if saveResult(fileName, listboxText) == 1:
                listOfResults.append(fileName)
            #
            #
            #
            #
            # Treba rok da se doda
            #
            #
            #
            #
            #
            #
            #

        btnAddResult = tk.Button(self, text="Dodaj rok", font=SettingsFont, command=addResult)
        btnAddResult.place(x=0.7 * windowWidth, y=550)


class Page4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lblYearAdm = tk.Label(self, text="Godina upisa", font=SettingsFont)
        lblYearAdm.place(x=10, y=10)

        txtYearAdm = tk.Entry(self, font=SettingsFont)
        txtYearAdm.place(x=200, y=10, width=120, height=30)

        lblYear = tk.Label(self, text="Godina", font=SettingsFont)
        lblYear.place(x=30, y=60)

        cmbYear = ttk.Combobox(self, font=SettingsFontSmaller)
        cmbYear.place(x=200, y=60, width=120, height=30)
        years = ["1. godina", "2.godina", "3. godina", "4. godina"]
        cmbYear["values"] = years
        cmbYear.state(["readonly"])
        cmbYear.current(0)

        def BtnSave():
            global year, yearAdm
            yA = txtYearAdm.get()
            badInput = False
            if len(yA) != 4 or yA[0] != '2':
                badInput = True
            for c in yA:
                if not c.isdigit():
                    badInput = True
                    break
            if badInput:
                messagebox.showerror("Obavestenje", "Neki podatak nije dobro unet.")
                return
            yearAdm = int(yA)
            year = cmbYear.current() + 1

        btnSave = tk.Button(self, text="Sacuvaj", font=SettingsFont, command=BtnSave)
        btnSave.place(x=700, y=550)

        def on_settings_loaded():
            txtYearAdm.insert(tk.END, str(yearAdm))
            cmbYear.current(year - 1)

        on_settings_loaded()


app = tkinterApp()
app.mainloop()
