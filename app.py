from pdf import *

from InOut import *

from clipboard import copyToClipboard

from ButtonRadiobutton import *

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import ctypes

# Some fonts used for widgets
FONT1 = ("Segoe UI", 35)
SettingsFont = ('Segoe UI', 15)
SettingsFontSmaller = ('Segoe UI', 10)
ListFont = ('Arial', 10)

windowWidth = 0
windowHeight = 0
currentPageNumber = 0
filePath = ""

listOfResults = list()
yearAdm = 0
year = 0
espb = 1
subjects = dict()
students = dict()


# Sets global window size variables
def setWindowSize(wt, ht):
    global windowWidth, windowHeight
    windowWidth = wt
    windowHeight = ht


# Loading data when loading app
def on_app_loading():
    global yearAdm, year, listOfResults, subjects, students, espb
    yearAdm, year, espb = loadSettings()
    listOfResults = loadListOfResults()
    subjects = loadSubjects()


# Saving data when closing app
def on_app_closing(self):
    self.destroy()
    saveSettings(yearAdm, year, espb)
    saveListOfResults(listOfResults)


# Main app class
class tkinterApp(tk.Tk):
    def show_page(self, Page):
        page = self.pages[Page]
        page.tkraise()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Hides window until it fully loads
        self.withdraw()
        wp = 0.839  # percentage of width of the screen
        hp = 0.7  # percentage of height of the screen

        # calculates size of screen without taskbar
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.SystemParametersInfoA(48, 0, ctypes.byref(rect), 0)
        fw = rect.right - rect.left
        fh = rect.bottom - rect.top

        setWindowSize(int(fw * wp), int(fh * hp))
        self.geometry("%dx%d+%d+%d" % (windowWidth, windowHeight, (fw - windowWidth) / 2, (fh - windowHeight) / 2))
        self.minsize(1300, 600)
        self.iconbitmap("images/icon1.ico")
        self.title("Lista")
        on_app_loading()
        self.protocol("WM_DELETE_WINDOW", func=lambda: on_app_closing(self))

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1000)

        for i in range(4):
            self.columnconfigure(i, weight=1)

        self.radio1 = ButtonRadiobutton(self, text='Lista', command=lambda: showCurrentPage(1))
        self.radio1.grid(row=0, column=0, sticky="nsew")

        self.radio2 = ButtonRadiobutton(self, text='Rokovi', command=lambda: showCurrentPage(2))
        self.radio2.grid(row=0, column=1, sticky="nsew")

        self.radio3 = ButtonRadiobutton(self, text='Dodaj rok', command=lambda: showCurrentPage(3))
        self.radio3.grid(row=0, column=2, sticky="nsew")

        self.radio4 = ButtonRadiobutton(self, text='Podesavanja', command=lambda: showCurrentPage(4))
        self.radio4.grid(row=0, column=3, sticky="nsew")

        rbs = [self.radio1, self.radio2, self.radio3, self.radio4]
        Pages = [Page1, Page2, Page3, Page4]

        self.pages = {}

        for Page in Pages:
            page = Page(self)
            self.pages[Page] = page
            page.grid(row=1, column=0, columnspan=4, sticky="nsew")

        def showCurrentPage(val):
            if val < 1 or val > 4:
                val = 1
            global currentPageNumber
            if currentPageNumber == val:
                return
            rbs[currentPageNumber - 1].unselectBtn()
            rbs[val - 1].selectBtn()
            currentPageNumber = val
            self.show_page(Pages[currentPageNumber - 1])

        showCurrentPage(1)
        # Shows window after 20 ms so that user can't see other widgets
        self.after(20, func=lambda: self.deiconify())


# Page class for showing students ranked
class Page1(tk.Frame):
    def loadPage1(self):
        self.listbox.grid_remove()
        global students
        students = loadResults(listOfResults, subjects, espb)
        for row in self.listbox.get_children():
            self.listbox.delete(row)
        self.columns = (("", "Indeks") + tuple(
            [f"{x:{4}}" for x in subjects[(year - 1) * 2 + 1]] + [f"{x:{4}}" for x in subjects[(year - 1) * 2 + 2]])
                        + ("Koef",))
        cw = [35, 85] + [len(x.strip()) * 9 for x in self.columns[2:]]
        self.listbox.configure(columns=self.columns)
        for ind, column in enumerate(self.columns):
            self.listbox.heading(column, anchor="w", text=column)
            self.listbox.column(column, anchor="w", width=cw[ind])
        data1 = []
        if type(students) is tuple:
            self.lblAlert.configure(text="Greska sa rezultatom " + students[1][students[1].rindex("/") + 1:]
                                         + ". Ne mozemo da prikazemo listu dok svi rezultati nisu dobro uneti.")
            self.listbox.grid(row=0, column=0, sticky="nsew")
            return
        else:
            self.lblAlert.configure(text="")
        yr = str(yearAdm)
        for student in sorted(students, key=lambda x: -students[x]["coef"]):
            if yr in student:
                data1.append((student,) +
                             tuple([students[student].get(x.strip(), "") for x in self.columns[2:-1]])
                             + (students[student]["coef"],))
        ind = 1
        for item in data1:
            koef = "{:5.2f}".format(item[-1])
            self.listbox.insert("", tk.END, values=(ind,) + item[:-1] + (koef,))
            ind += 1
        self.listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.update()

        style = ttk.Style()
        style.configure('Custom.TEntry', foreground='blue', background='lightyellow', borderwidth=2)

        self.rowconfigure(0, weight=50)
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=50)
        self.columnconfigure(1, weight=1)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.update_idletasks()

        self.container.rowconfigure(0, weight=1000)
        self.container.rowconfigure(1, weight=1)

        self.container.columnconfigure(0, weight=1000)
        self.container.columnconfigure(1, weight=1)

        self.scrollbarx = ttk.Scrollbar(self.container, orient=tk.HORIZONTAL)
        self.scrollbary = ttk.Scrollbar(self.container)
        self.listbox = ttk.Treeview(self.container, xscrollcommand=self.scrollbarx.set,
                                    yscrollcommand=self.scrollbary.set, show="headings")

        self.lblAlert = tk.Label(self, font=("Segoe UI", 12), text="")
        self.lblAlert.grid(row=1, column=0, pady=10, columnspan=2, sticky="new")

        self.scrollbarx.configure(command=self.listbox.xview)
        self.scrollbary.configure(command=self.listbox.yview)

        self.listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.scrollbarx.grid(row=1, column=0, sticky="nsew")
        self.scrollbary.grid(row=0, column=1, sticky="nsew")
        self.listbox.heading("#0", text="")

        ListStyle = ttk.Style()
        ListStyle.configure("Treeview", font=ListFont)
        ListStyle.configure("Treeview.Heading", font=ListFont + ("bold",))
        self.columns = tuple()

        def BtnClick():
            dataToCopy = []
            headers = self.columns[1:]
            dataToCopy.append("      " + headers[0] + "        " + "   ".join(headers[1:-1]) + "  " + headers[-1])
            for item in self.listbox.get_children():
                row = self.listbox.item(item)["values"]
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
            self.btn.config(text="Copied", image=self.okicon)

        self.loadPage1()
        self.copyicon = tk.PhotoImage(file="images/copyicon.png")
        self.okicon = tk.PhotoImage(file="images/okicon.png")
        self.btn = tk.Button(self, text="Copy", image=self.copyicon, compound=tk.LEFT, background="darkgrey",
                             command=BtnClick)
        self.btn.grid(row=0, column=1, padx=10, pady=10, sticky="new")


# Page class for seeing, changing and de
# leting saved results
class Page2(tk.Frame):

    def loadResultsToPage2(self):
        self.listbox1.delete(0, tk.END)
        self.listbox2.delete("1.0", tk.END)
        global old_ind_page2
        old_ind_page2 = -1
        for r in listOfResults:
            self.listbox1.insert(tk.END, r)

    def changeToSelectedResult(self):
        ind = self.listbox1.curselection()
        global old_ind_page2
        if ind and ind[0] != old_ind_page2:
            old_ind_page2 = ind[0]
            self.listbox2.delete("1.0", tk.END)
            r = loadResult(self.listbox1.get(ind[0]))
            for line in r:
                self.listbox2.insert(tk.END, line + "\n")
            app.pages[Page1].loadPage1()

    def removeResult(self):
        ind = self.listbox1.curselection()
        if not ind:
            messagebox.showerror("Greska", "Niste izabrali rok koji zelite da obrisete.")
            return
        shouldDelRes = messagebox.askyesno("Potvrdite radnju", "Da li zelite da izbrisete izabrani rok?")

        if shouldDelRes:
            resFileName = self.listbox1.get(ind[0])
            deleteFile(resFileName)
            listOfResults.remove(resFileName)
            self.loadResultsToPage2()
            self.listbox2.delete("1.0", tk.END)
            app.pages[Page1].loadPage1()

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        Font2 = ("Arial", 10)

        self.rowconfigure(0, weight=200)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        pomlbl1 = tk.Label(self, text="")
        pomlbl1.grid(row=2, column=3)

        # listbox1 is for showing which results were saved
        container1 = tk.Frame(self)
        container1.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        container1.rowconfigure(0, weight=200)
        container1.rowconfigure(1, weight=1)
        container1.columnconfigure(0, weight=200)
        container1.columnconfigure(1, weight=1)

        scrollbarx1 = ttk.Scrollbar(container1, orient=tk.HORIZONTAL)
        scrollbary1 = ttk.Scrollbar(container1)
        self.listbox1 = tk.Listbox(container1, xscrollcommand=scrollbarx1.set, font=Font2,
                                   yscrollcommand=scrollbary1.set, activestyle="none")
        scrollbarx1.configure(command=self.listbox1.xview)
        scrollbary1.configure(command=self.listbox1.yview)

        self.listbox1.grid(row=0, column=0, sticky="nsew")
        scrollbarx1.grid(row=1, column=0, sticky="nsew")
        scrollbary1.grid(row=0, column=1, sticky="nsew")

        # used to track if different listbox1 item is selected, so that unnecessary result loads aren't done
        global old_ind_page2
        old_ind_page2 = -1

        self.listbox1.bind("<<ListboxSelect>>", lambda event: self.changeToSelectedResult())

        # listbox2 is for showing selected result
        container2 = tk.Frame(self)
        container2.grid(row=0, column=1, columnspan=3, padx=20, pady=10, sticky="nsew")

        container2.rowconfigure(0, weight=200)
        container2.rowconfigure(1, weight=1)
        container2.columnconfigure(0, weight=200)
        container2.columnconfigure(1, weight=1)

        scrollbarx2 = ttk.Scrollbar(container2, orient=tk.HORIZONTAL)
        scrollbary2 = ttk.Scrollbar(container2)
        self.listbox2 = tk.Text(container2, width=10, xscrollcommand=scrollbarx2.set, font=("Arial", 10), wrap="none",
                                yscrollcommand=scrollbary2.set, undo=True)
        scrollbarx2.configure(command=self.listbox2.xview)
        scrollbary2.configure(command=self.listbox2.yview)

        self.listbox2.grid(row=0, column=0, sticky="nsew")
        scrollbarx2.grid(row=1, column=0, sticky="nsew")
        scrollbary2.grid(row=0, column=1, sticky="nsew")
        self.loadResultsToPage2()

        style = ttk.Style()
        style.configure('TButton', font=SettingsFont, focuscolor='None', activebackground='white')
        style.map('TButton',
                  background=[('focus', 'white')])

        btnRemoveResult = ttk.Button(self, text="Ukloni rok", style="TButton", command=lambda: self.removeResult())
        btnRemoveResult.grid(row=1, column=3, pady=10, sticky="w")

        def alterResult():
            ind = old_ind_page2
            if ind == -1:
                messagebox.showerror("Greska", "Niste izabrali rok koji zelite da izmenite.")
                return
            res = self.listbox2.get("1.0", tk.END)
            resFileName = self.listbox1.get(ind)
            if len(res) == 0:
                messagebox.showerror("Greska", "Ne mozete da izmenite rok na ovaj nacin.")
                return
            shouldAltRes = messagebox.askyesno("Potvrdite radnju", "Da li zelite da izmenite "
                                               + resFileName[resFileName.rindex("/") + 1:] + " ?")
            if shouldAltRes:
                saveResult(resFileName, res)
                messagebox.showinfo("Obavesetenje", "Izabrani fajl je izmenjen.")
                app.pages[Page1].loadPage1()

        btnAlterResult = ttk.Button(self, text="Izmeni rok", style="TButton", command=alterResult)
        btnAlterResult.grid(row=1, column=1, pady=10, sticky="e")


# Page class for adding results
class Page3(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=10)
        self.rowconfigure(3, weight=10)
        self.rowconfigure(4, weight=300)
        self.rowconfigure(5, weight=10)

        self.columnconfigure(0, weight=30)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=8)
        self.columnconfigure(3, weight=12)

        Font2 = ("Arial", 10)
        container = tk.Frame(self)
        container.grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew")
        container.update_idletasks()

        container.rowconfigure(0, weight=1000)
        container.rowconfigure(1, weight=1)

        container.columnconfigure(0, weight=1000)
        container.columnconfigure(1, weight=1)

        style = ttk.Style()
        style.configure("Custom.Listbox", font=Font2)
        scrollbarx = ttk.Scrollbar(container, orient=tk.HORIZONTAL)
        scrollbary = ttk.Scrollbar(container)
        listbox = tk.Text(container, wrap="none", xscrollcommand=scrollbarx.set,
                          yscrollcommand=scrollbary.set, width=10, height=1, undo=True)
        scrollbarx.configure(command=listbox.xview)
        scrollbary.configure(command=listbox.yview)

        listbox.grid(row=0, column=0, sticky="nsew")
        scrollbarx.grid(row=1, column=0, sticky="nsew")
        scrollbary.grid(row=0, column=1, sticky="nsew")
        content = ""

        def chooseFile():
            global filePath
            fp = filedialog.askopenfilename(title="Izaberite fajl", filetypes=(("PDF files", "*.pdf"),))
            if fp == "":
                return
            filePath = fp
            listbox.delete("1.0", tk.END)
            nonlocal content
            content = read_pdf(filePath)
            for l1 in content:
                listbox.insert(tk.END, l1 + "\n")

        style1 = ttk.Style()
        style1.configure('TButton', font=SettingsFont, focuscolor='None', activebackground='white')
        style1.map('TButton', background=[('focus', 'white')])

        btnFileChoose = ttk.Button(self, text="Izaberite fajl", style="TButton", command=chooseFile)
        btnFileChoose.grid(row=5, column=0, padx=10, pady=10, sticky="n")

        lblSemester = tk.Label(self, font=SettingsFontSmaller, text="Semestar")
        lblSemester.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        cmbSemester = ttk.Combobox(self, font=SettingsFontSmaller, width=12)
        cmbSemester.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        semesters = ["1. semestar", "2. semestar", "3. semestar", "4. semestar",
                     "5. semestar", "6. semestar", "7. semestar", "8. semestar"]
        cmbSemester["values"] = semesters
        cmbSemester.state(["readonly"])
        cmbSemester.current(0)

        lblSubject = tk.Label(self, font=SettingsFontSmaller, text="Predmet")
        lblSubject.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        cmbSubject = ttk.Combobox(self, font=SettingsFontSmaller, width=12)
        cmbSubject.grid(row=2, column=3, padx=10, pady=10, sticky="w")
        cmbSubject["values"] = subjects[1]
        cmbSubject.state(["readonly"])

        lblTerm = tk.Label(self, font=SettingsFontSmaller, text="Rok")
        lblTerm.grid(row=3, column=2, padx=10, pady=10, sticky="e")

        cmbTerm = ttk.Combobox(self, font=SettingsFontSmaller, width=12)
        cmbTerm.grid(row=3, column=3, padx=10, pady=10, sticky="w")
        cmbTerm["values"] = ["januar", "februar", "jun", "jul", "avgust", "septembar"]
        cmbTerm.state(["readonly"])

        def on_semester_change(event):
            ind = cmbSemester.current()
            if ind % 2 == 0:
                cmbSubject["values"] = subjects[ind + 1]
            else:
                cmbSubject["values"] = subjects[ind + 1] + [str((ind + 1) // 2) + ". godina", ]
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
            subject = cmbSubject.get()
            listboxText = listbox.get("1.0", tk.END)
            # Dodavanje liste, a ne rezultata
            if "godina" in subject:
                fileName = "files/results/" + subject + ".txt"
                if fileName in listOfResults:
                    messagebox.showerror("Obavestenje", "Vec ste dodali listu za " + subject[0] + ". godinu.")
                    return
                if saveResult(fileName, listboxText) == 1:
                    listbox.delete("1.0", tk.END)
                    cmbSubject.set("")
                    listOfResults.append(fileName)
                    app.pages[Page1].loadPage1()
                    app.pages[Page2].loadResultsToPage2()
                    messagebox.showinfo("Obavestenje", "Rezultat roka je uspesno dodat.")
                else:
                    messagebox.showerror("Obavestenje",
                                         "Ova lista nije u dobrom formatu. Format je( ... Indeks ... Ocena ...).")
                return
            if cmbTerm.current() == -1:
                messagebox.showerror("Obavestenje", "Niste izabrali rok.")
                return
            if len(listboxText) < 11:
                messagebox.showerror("Obavestenje", "Niste uneli vazeci rok.")
                return
            term = cmbTerm.get()[:3]
            fileName = "files/results/" + subject + "-" + term + "-"
            num = 1
            while fileName + str(num) + ".txt" in listOfResults:
                num += 1
            fileName += str(num) + ".txt"
            if saveResult(fileName, listboxText) == 1:
                listbox.delete("1.0", tk.END)
                cmbSubject.set("")
                listOfResults.append(fileName)
                app.pages[Page1].loadPage1()
                app.pages[Page2].loadResultsToPage2()
                messagebox.showinfo("Obavestenje", "Rezultat roka je uspesno dodat.")
            else:
                messagebox.showerror("Obavestenje",
                                     "Ovi razultati nisu u dobrom formatu. Format je( ... Indeks ... Ocena ...).")

        btnAddResult = ttk.Button(self, text="Dodaj rok", style="TButton", command=addResult)
        btnAddResult.grid(row=5, column=2, columnspan=2, padx=10, pady=10, sticky="n")


# Settings page class
class Page4(tk.Frame):
    def BtnSave(self):
        global year, yearAdm, espb
        yA = self.txtYearAdm.get()
        es = self.txtEspb.get()
        badInput = False
        if len(yA) != 4 or yA[0] != '2':
            badInput = True
        for c in yA:
            if not c.isdigit():
                badInput = True
                break
        for c in es:
            if not c.isdigit():
                badInput = True
                break
        if badInput:
            messagebox.showerror("Obavestenje", "Neki podatak nije dobro unet.")
            return
        if int(es) == 0:
            messagebox.showerror("Obavestenje", "Espb ne moze biti 0.")
            return
        yearAdm = int(yA)
        year = self.cmbYear.current() + 1
        espb = int(es)
        app.pages[Page1].loadPage1()
        messagebox.showinfo("Obavestenje", "Sacuvali ste podesavanja.")

    def on_settings_loaded(self):
        self.txtYearAdm.insert(tk.END, str(yearAdm))
        self.cmbYear.current(year - 1)
        self.txtEspb.insert(tk.END, str(espb))

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        for i in range(16):
            self.columnconfigure(i, weight=1)
        for i in range(20):
            self.rowconfigure(i, weight=1)

        c, r = 5, 2
        self.lblYearAdm = tk.Label(self, text="Godina upisa", font=SettingsFont)
        self.lblYearAdm.grid(row=r, column=c, padx=20, sticky="e")

        self.txtYearAdm = ttk.Entry(self, font=SettingsFont)
        self.txtYearAdm.grid(row=r, column=c + 1, sticky="w")

        self.lblYear = tk.Label(self, text="Godina", font=SettingsFont)
        self.lblYear.grid(row=r + 1, column=c, padx=20, sticky="e")

        self.cmbYear = ttk.Combobox(self, font=SettingsFont, width=18)
        self.cmbYear.grid(row=r + 1, column=c + 1, sticky="w")
        years = ["1. godina", "2.godina", "3. godina", "4. godina"]
        self.cmbYear["values"] = years
        self.cmbYear.state(["readonly"])
        self.cmbYear.current(0)

        self.lblEspb = tk.Label(self, text="Espb", font=SettingsFont)
        self.lblEspb.grid(row=r + 2, column=c, padx=20, sticky="e")

        self.txtEspb = ttk.Entry(self, font=SettingsFont)
        self.txtEspb.grid(row=r + 2, column=c + 1, sticky="w")

        style = ttk.Style()
        style.configure('TButton', font=SettingsFont, focuscolor='None', activebackground='white')
        style.map('TButton',
                  background=[('focus', 'white')])
        btnSave = ttk.Button(self, text="Sacuvaj", style="TButton", command=lambda: self.BtnSave())
        btnSave.grid(row=10, column=c + 1, sticky="sw")

        self.on_settings_loaded()


app = tkinterApp()
app.mainloop()
