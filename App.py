# For copying to clipboard, not needed anymore
""""  from Clipboard import copyToClipboard  """

from Pdf import *
from InOut import *
from Expression import *
from MenuButton import *

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import ctypes

sys.path.insert(0, 'pyglet')
import pyglet

# Pyglet doesn't show intended font without this
pyglet.options['win32_gdi_font'] = True
pyglet.font.add_directory('Sen/static')

# Some fonts used for widgets
SettingsFont = ('Sen', 15)
NormalFont = ('Courier', 11)

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
def onAppLoading():
    global yearAdm, year, listOfResults, subjects, students, espb
    yearAdm, year, espb = loadSettings()
    listOfResults = loadListOfResults()
    subjects = loadSubjects()


# Saving data when closing app
def onAppClosing(self):
    self.destroy()
    saveSettings(yearAdm, year, espb)
    saveListOfResults(listOfResults)


def copyPaste(event):
    try:
        clipboardData = app.clipboard_get()
        event.widget.insert(tk.INSERT, clipboardData)
        event.widget.edit_separator()
    except tk.TclError:
        pass


def rowConfigure(self, n, l1):
    for i in range(n):
        self.rowconfigure(i, weight=l1[i])


def columnConfigure(self, n, l1):
    for i in range(n):
        self.columnconfigure(i, weight=l1[i])


# Main app class
class tkinterApp(tk.Tk):
    def showPage(self, Page):
        page = self.pages[Page]
        page.tkraise()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Hides window until it fully loads
        self.withdraw()

        wp = 0.86  # percentage of width of the screen
        hp = 0.72  # percentage of height of the screen

        # calculates size of screen without taskbar
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.SystemParametersInfoA(48, 0, ctypes.byref(rect), 0)
        fw = rect.right - rect.left
        fh = rect.bottom - rect.top
        setWindowSize(int(fw * wp), int(fh * hp))

        self.geometry("%dx%d+%d+%d" % (windowWidth, windowHeight, (fw - windowWidth) / 2, (fh - windowHeight) / 2))
        self.minsize(1300, 600)
        self.iconbitmap("images/icon.ico")
        self.title("Result Manager")
        onAppLoading()
        self.protocol("WM_DELETE_WINDOW", func=lambda: onAppClosing(self))

        rowConfigure(self, 2, [1, 1000])
        columnConfigure(self, 4, [1, 1, 1, 1])

        self.radio1 = MenuButton(self, text='Lista', command=lambda: showCurrentPage(1))
        self.radio1.grid(row=0, column=0, sticky="nsew")

        self.radio2 = MenuButton(self, text='Rokovi', command=lambda: showCurrentPage(2))
        self.radio2.grid(row=0, column=1, sticky="nsew")

        self.radio3 = MenuButton(self, text='Dodaj rok', command=lambda: showCurrentPage(3))
        self.radio3.grid(row=0, column=2, sticky="nsew")

        self.radio4 = MenuButton(self, text='Podešavanja', command=lambda: showCurrentPage(4))
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
            self.showPage(Pages[currentPageNumber - 1])

        showCurrentPage(3)
        # Shows window after 20 ms so that user can't see other widgets
        self.after(20, func=lambda: self.deiconify())


# Page class for showing students ranked
class Page1(tk.Frame):
    def loadPage1(self):
        self.textbox.grid_remove()
        self.textbox.config(state=tk.NORMAL)
        global students
        students = loadResults(listOfResults, subjects, espb)
        self.textbox.delete("1.0", tk.END)
        header = ([" Br     Indeks", ] + [f"{x:>{4}}" for x in subjects[(year - 1) * 2 + 1]]
                  + [f"{x:>{4}}" for x in subjects[(year - 1) * 2 + 2]] + ["Koeficijent", ])
        data1 = []
        if type(students) is tuple:
            self.textbox.insert(tk.END, "Greška sa rezultatom " + students[1][students[1].rindex("/") + 1:]
                                + ". Ne možemo da prikažemo listu dok svi rezultati nisu dobro uneti.\n")
            self.textbox.grid(row=0, column=0, sticky="nsew")
            self.textbox.config(state=tk.DISABLED)
            return

        self.textbox.insert(tk.END, "  ".join(header) + "\n")
        yr = str(yearAdm)
        br = 1
        for student in sorted(students, key=lambda x: -students[x]["coef"]):
            if yr in student:
                data1.append(["{:>3d}".format(br), student] +
                             ["{:>4}".format(students[student].get(x.strip(), "  ")) for x in header[1:-1]]
                             + ["{:>5.2f}".format(students[student]["coef"]), ])
                br += 1
        for item in data1:
            self.textbox.insert(tk.END, "  ".join(item) + "\n")
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.config(state=tk.DISABLED)

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        rowConfigure(self, 2, [50, 1])
        columnConfigure(self, 2, [1, 0])

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        rowConfigure(self.container, 2, [1000, 1])
        columnConfigure(self.container, 2, [1000, 1])

        self.scrollbarx = ttk.Scrollbar(self.container, orient=tk.HORIZONTAL)
        self.scrollbary = ttk.Scrollbar(self.container)
        self.textbox = tk.Text(self.container, xscrollcommand=self.scrollbarx.set, wrap="none",
                               font=NormalFont, yscrollcommand=self.scrollbary.set)

        self.scrollbarx.configure(command=self.textbox.xview)
        self.scrollbary.configure(command=self.textbox.yview)

        self.scrollbarx.grid(row=1, column=0, sticky="nsew")
        self.scrollbary.grid(row=0, column=1, sticky="nsew")

        self.loadPage1()


# Page class for seeing, changing and deleting saved results
class Page2(tk.Frame):

    def loadResultsToPage2(self):
        self.listbox1.delete(0, tk.END)
        self.listbox2.delete("1.0", tk.END)
        global oldIndPage2
        oldIndPage2 = -1
        for r in listOfResults:
            self.listbox1.insert(tk.END, r)

    def changeToSelectedResult(self):
        ind = self.listbox1.curselection()
        global oldIndPage2
        if ind and ind[0] != oldIndPage2:
            oldIndPage2 = ind[0]
            self.listbox2.delete("1.0", tk.END)
            r = loadResult(self.listbox1.get(ind[0]))
            for line in r:
                self.listbox2.insert(tk.END, line + "\n")
            app.pages[Page1].loadPage1()

    def removeResult(self):
        ind = self.listbox1.curselection()
        if not ind:
            messagebox.showerror("Greška", "Niste izabrali rok koji želite da obrišete.")
            return
        shouldDelRes = messagebox.askyesno("Potvrdite radnju", "Da li želite da izbrišete izabrani rok?")

        if shouldDelRes:
            resFileName = self.listbox1.get(ind[0])
            deleteFile(resFileName)
            listOfResults.remove(resFileName)
            self.loadResultsToPage2()
            self.listbox2.delete("1.0", tk.END)
            app.pages[Page1].loadPage1()
            messagebox.showinfo("Obaveštenje", "Izabrani fajl je obrisan.")

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background='black')

        rowConfigure(self, 2, [200, 1])
        columnConfigure(self, 4, [3, 1, 1, 1])

        # listbox1 is for showing which results were saved
        container1 = tk.Frame(self)
        container1.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        rowConfigure(container1, 2, [200, 1])
        columnConfigure(container1, 2, [200, 1])

        scrollbarx1 = ttk.Scrollbar(container1, orient=tk.HORIZONTAL)
        scrollbary1 = ttk.Scrollbar(container1)
        self.listbox1 = tk.Listbox(container1, xscrollcommand=scrollbarx1.set, font=NormalFont,
                                   yscrollcommand=scrollbary1.set, activestyle="none")
        scrollbarx1.configure(command=self.listbox1.xview)
        scrollbary1.configure(command=self.listbox1.yview)

        self.listbox1.grid(row=0, column=0, sticky="nsew")
        scrollbarx1.grid(row=1, column=0, sticky="nsew")
        scrollbary1.grid(row=0, column=1, sticky="nsew")

        # used to track if different listbox1 item is selected, so that unnecessary result loads aren't done
        global oldIndPage2
        oldIndPage2 = -1

        self.listbox1.bind("<<ListboxSelect>>", lambda event: self.changeToSelectedResult())

        # listbox2 is for showing selected result
        container2 = tk.Frame(self)
        container2.grid(row=0, column=1, columnspan=3, padx=20, pady=10, sticky="nsew")

        rowConfigure(container2, 2, [200, 1])
        columnConfigure(container2, 2, [200, 1])

        scrollbarx2 = ttk.Scrollbar(container2, orient=tk.HORIZONTAL)
        scrollbary2 = ttk.Scrollbar(container2)
        self.listbox2 = tk.Text(container2, width=10, xscrollcommand=scrollbarx2.set, font=NormalFont, wrap="none",
                                yscrollcommand=scrollbary2.set, undo=True)

        scrollbarx2.configure(command=self.listbox2.xview)
        scrollbary2.configure(command=self.listbox2.yview)

        self.listbox2.grid(row=0, column=0, sticky="nsew")
        scrollbarx2.grid(row=1, column=0, sticky="nsew")
        scrollbary2.grid(row=0, column=1, sticky="nsew")
        self.loadResultsToPage2()

        self.listbox2.bind('<Control-v>', copyPaste)

        style = ttk.Style()
        style.configure('TButton', font=SettingsFont, focuscolor='None', activebackground='white')
        style.map('TButton',
                  background=[('focus', 'white')])

        btnRemoveResult = ttk.Button(self, text="Ukloni rok", style="TButton", command=lambda: self.removeResult())
        btnRemoveResult.grid(row=1, column=3, pady=20, sticky="w")

        def alterResult():
            ind = oldIndPage2
            if ind == -1:
                messagebox.showerror("Greška", "Niste izabrali rok koji želite da izmenite.")
                return
            res = self.listbox2.get("1.0", tk.END)
            resFileName = self.listbox1.get(ind)
            if len(res) == 0:
                messagebox.showerror("Greška", "Ne možete da izmenite rok na ovaj način.")
                return
            shouldAltRes = messagebox.askyesno("Potvrdite radnju", "Da li želite da izmenite "
                                               + resFileName[resFileName.rindex("/") + 1:] + " ?")
            if shouldAltRes:
                saveResult(resFileName, res)
                messagebox.showinfo("Obaveštenje", "Izabrani fajl je izmenjen.")
                app.pages[Page1].loadPage1()

        btnAlterResult = ttk.Button(self, text="Izmeni rok", style="TButton", command=alterResult)
        btnAlterResult.grid(row=1, column=1, pady=20, sticky="e")


# Page class for adding results
class Page3(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background='black')

        Font = ("Sen", 12)

        rowConfigure(self, 8, [10, 10, 10, 10, 10, 30, 100, 10])
        columnConfigure(self, 4, [50, 1, 1, 6])

        container = tk.Frame(self)
        container.grid(row=0, column=0, rowspan=7, padx=10, pady=10, sticky="nsew")

        rowConfigure(container, 2, [1000, 1])
        columnConfigure(container, 2, [1000, 1])

        scrollbarx = ttk.Scrollbar(container, orient=tk.HORIZONTAL)
        scrollbary = ttk.Scrollbar(container)
        textbox = tk.Text(container, wrap="none", xscrollcommand=scrollbarx.set,
                          font=NormalFont, yscrollcommand=scrollbary.set, width=10, height=1, undo=True)
        scrollbarx.configure(command=textbox.xview)
        scrollbary.configure(command=textbox.yview)

        textbox.grid(row=0, column=0, sticky="nsew")
        scrollbarx.grid(row=1, column=0, sticky="nsew")
        scrollbary.grid(row=0, column=1, sticky="nsew")
        content = ""

        textbox.bind('<Control-v>', copyPaste)

        def chooseFile():
            global filePath
            fp = filedialog.askopenfilename(title="Izaberite fajl", filetypes=(("PDF files", "*.pdf"),))
            if fp == "":
                return
            filePath = fp
            textbox.delete("1.0", tk.END)
            nonlocal content
            content = readPdf(filePath)
            for l1 in content:
                textbox.insert(tk.END, l1 + "\n")

        style1 = ttk.Style()
        style1.configure('C1.TButton', font=SettingsFont)

        btnFileChoose = ttk.Button(self, text="Izaberite fajl", style="C1.TButton", command=chooseFile)
        btnFileChoose.grid(row=7, column=0, padx=10, pady=10, sticky="n")

        lblSemester = tk.Label(self, font=Font, bg='black', fg='white', text="Semestar")
        lblSemester.grid(row=1, column=2, sticky="e")

        cmbSemester = ttk.Combobox(self, font=Font, width=12)
        cmbSemester.grid(row=1, column=3, padx=5, pady=10)
        semesters = ["1. semestar", "2. semestar", "3. semestar", "4. semestar",
                     "5. semestar", "6. semestar", "7. semestar", "8. semestar"]
        cmbSemester["values"] = semesters
        cmbSemester.state(["readonly"])
        cmbSemester.current(0)

        lblSubject = tk.Label(self, font=Font, bg='black', fg='white', text="Predmet")
        lblSubject.grid(row=2, column=2, sticky="e")

        cmbSubject = ttk.Combobox(self, font=Font, width=12)
        cmbSubject.grid(row=2, column=3, padx=10, pady=10)
        cmbSubject["values"] = subjects[1]
        cmbSubject.state(["readonly"])

        lblExamPeriod = tk.Label(self, font=Font, bg='black', fg='white', text="Rok")
        lblExamPeriod.grid(row=3, column=2, sticky="e")

        cmbExamPeriod = ttk.Combobox(self, font=Font, width=12)
        cmbExamPeriod.grid(row=3, column=3, padx=10, pady=10)
        cmbExamPeriod["values"] = ["januar", "februar", "jun", "jul", "avgust", "septembar"]
        cmbExamPeriod.state(["readonly"])

        def onSemesterChange(event):
            ind = cmbSemester.current()
            if ind % 2 == 0:
                cmbSubject["values"] = subjects[ind + 1]
            else:
                cmbSubject["values"] = subjects[ind + 1] + [str((ind + 1) // 2) + ". godina", ]
            cmbSubject.set("")
            cmbExamPeriod.set("")

        cmbSemester.bind("<<ComboboxSelected>>", onSemesterChange)

        def addResult():
            if cmbSubject.current() == -1:
                messagebox.showerror("Obaveštenje", "Niste izabrali predmet.")
                return
            if cmbSemester.current() == -1:
                messagebox.showerror("Obaveštenje", "Niste izabrali semestar.")
                return
            subject = cmbSubject.get()
            textboxText = textbox.get("1.0", tk.END)
            # Dodavanje liste, a ne rezultata
            if "godina" in subject:
                fileName = "files/results/" + subject + ".txt"
                if fileName in listOfResults:
                    messagebox.showerror("Obaveštenje", "Vec ste dodali listu za " + subject[0] + ". godinu.")
                    return
                if saveResult(fileName, textboxText) == 1:
                    textbox.delete("1.0", tk.END)
                    cmbSubject.set("")
                    listOfResults.append(fileName)
                    app.pages[Page1].loadPage1()
                    app.pages[Page2].loadResultsToPage2()
                    messagebox.showinfo("Obaveštenje", "Rezultat roka je uspešno dodat.")
                else:
                    messagebox.showerror("Obaveštenje",
                                         "Ova lista nije u dobrom formatu. Format je( ... Indeks ... Ocena ...).")
                return
            if cmbExamPeriod.current() == -1:
                messagebox.showerror("Obaveštenje", "Niste izabrali rok.")
                return
            if len(textboxText) < 11:
                messagebox.showerror("Obaveštenje", "Niste uneli važeći rok.")
                return
            examPeriod = cmbExamPeriod.get()[:3]
            fileName = "files/results/" + subject + "-" + examPeriod + "-"
            num = 1
            while fileName + str(num) + ".txt" in listOfResults:
                num += 1
            fileName += str(num) + ".txt"
            if saveResult(fileName, textboxText) == 1:
                textbox.delete("1.0", tk.END)
                cmbSubject.set("")
                listOfResults.append(fileName)
                app.pages[Page1].loadPage1()
                app.pages[Page2].loadResultsToPage2()
                messagebox.showinfo("Obaveštenje", "Rezultat roka je uspešno dodat.")
            else:
                messagebox.showerror("Obaveštenje",
                                     "Ovi razultati nisu u dobrom formatu. Format je( ... Indeks ... Ocena ...).")

        btnAddResult = ttk.Button(self, text="Dodaj rok", style="C1.TButton", command=addResult)
        btnAddResult.grid(row=7, column=2, columnspan=2, padx=10, pady=10, sticky="n")

        # Advanced options for adding results
        container1 = tk.Frame(self, background='black', borderwidth=2, relief=tk.RIDGE)
        # container1.grid(row=5, column=2, columnspan=2, padx=20, pady=20, sticky="nsew")

        rowConfigure(container1, 3, [1, 1, 1])
        columnConfigure(container1, 3, [1, 3, 3])

        def showInfo():
            messagebox.showinfo("Info", "Napredne opcije omogućavaju pravljenje novih rezultata od "
                                        "postojećih. Uslovi se odvajaju zarezom, a dostupna je i funkcija count.\n"
                                        "Primeri:\n"
                                        "'P2>6' - Svi studenti koji su dobili ocenu veću od 6 iz Programiranja 2\n"
                                        "'count(P2>7,Mat1,Pp2=8)>1' - Svi studenti koji su položili Programiranje 2 "
                                        "sa ocenom većom od 7 ili položili Matematiku 1 ili dobili ocenu 8 iz "
                                        "Praktikuma iz programiranja 2, ali su postigli bar 2 od ove 3 stvari.\n"
                                        "Napomena: operatori <= i >= nisu dozvoljeni, ako se ne stavi uslov za predmet "
                                        "podrazumeva se da se gleda da li je ocena > 5, a ako se ne stavi uslov za"
                                        " count podrazumeva se da se gleda da li je bar jedan uslov tačan.")

        style3 = ttk.Style()
        style3.configure("C1.TLabel", background="#005FB8", anchor='center', height=1, foreground='white',
                         font=('Calibri', 12))
        btnInfo = ttk.Button(container1, style="C1.TLabel", text="i", width=1, command=showInfo)
        btnInfo.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        lblOptions = tk.Label(container1, text="Napredne opcije", bg='black', fg='white', font=("Sen", 15))
        lblOptions.grid(row=0, column=0, columnspan=2, sticky="new")

        lblExpression = tk.Label(container1, text="Izraz", bg='black', fg='white', font=("Sen", 12))
        lblExpression.grid(row=1, column=0)

        txtExpression = ttk.Entry(container1, font=('Calibri', 12))
        txtExpression.grid(row=1, column=1, columnspan=2, padx=15, sticky="ew")

        lblGrade = tk.Label(container1, text="Ocena", bg='black', fg='white', font=("Sen", 12))
        lblGrade.grid(row=2, column=0)

        cmbGrade = ttk.Combobox(container1, width=5, font=("Sen", 12))
        cmbGrade.grid(row=2, column=1, columnspan=2, padx=15, sticky="w")
        cmbGrade["values"] = ["6", "7", "8", "9", "10"]
        cmbGrade.state(["readonly"])

        def addList():
            if type(students) is tuple:
                messagebox.showerror("Obaveštenje", "Neki dodat rok nije ispravan.")
                return
            if len(students) == 0:
                messagebox.showerror("Obaveštenje", "Nijedan rok nije dodat.")
                return
            if cmbGrade.current() == -1:
                messagebox.showerror("Obaveštenje", "Niste uneli ocenu koju zelite da svi na listi dobiju.")
                return
            txt = txtExpression.get()
            if txt == "":
                messagebox.showerror("Obaveštenje", "Niste uneli izraz za pravljenje liste.")
                return
            grade = cmbGrade.current() + 6
            newtxt = evaluateExpression(txt, students, grade)
            if newtxt == "f":
                messagebox.showerror("Obaveštenje", "Izraz nije dobar.")
                return
            if newtxt == "":
                messagebox.showerror("Obaveštenje", "Izraz nije dobar ili nema studenta sa datim osobinama.")
                return
            textbox.delete("1.0", tk.END)
            textbox.insert(tk.END, newtxt)
            messagebox.showinfo("Obaveštenje", "Lista je napravljena.")

        style1 = ttk.Style()
        style1.configure('C2.TButton', font=("Sen", 10))

        btnAdd = ttk.Button(container1, text="Napravi listu", style="C2.TButton", command=addList)
        btnAdd.grid(row=2, column=2)

        self.moreOptions = tk.BooleanVar()

        def onCheck():
            if self.moreOptions.get():
                container1.grid(row=5, column=2, columnspan=2, padx=20, pady=20, sticky="nsew")
            else:
                container1.grid_remove()

        style2 = ttk.Style()
        style2.configure('TCheckbutton', background='black', foreground='white', font=("Sen", 12))

        chkMoreOptions = ttk.Checkbutton(self, text="Napredne opcije", variable=self.moreOptions, command=onCheck)
        chkMoreOptions.grid(row=4, column=2, columnspan=2, pady=15)


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
            messagebox.showerror("Obaveštenje", "Neki podatak nije dobro unet.")
            return
        if int(es) == 0:
            messagebox.showerror("Obaveštenje", "Espb ne može biti 0.")
            return
        yearAdm = int(yA)
        year = self.cmbYear.current() + 1
        espb = int(es)
        app.pages[Page1].loadPage1()
        messagebox.showinfo("Obaveštenje", "Sačuvali ste podešavanja.")

    def onSettingsLoaded(self):
        self.txtYearAdm.insert(tk.END, str(yearAdm))
        self.cmbYear.current(year - 1)
        self.txtEspb.insert(tk.END, str(espb))

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background='black')
        rowConfigure(self, 7, [1, 1, 1, 1, 4, 1, 5])
        columnConfigure(self, 4, [3, 2, 3, 5])

        self.lblYearAdm = tk.Label(self, text="Godina upisa", bg='black', fg='white', font=SettingsFont)
        self.lblYearAdm.grid(row=1, column=1, padx=20, sticky="e")

        self.txtYearAdm = ttk.Entry(self, font=SettingsFont)
        self.txtYearAdm.grid(row=1, column=2, sticky="w")

        self.lblYear = tk.Label(self, text="Godina", bg='black', fg='white', font=SettingsFont)
        self.lblYear.grid(row=2, column=1, padx=20, sticky="e")

        self.cmbYear = ttk.Combobox(self, font=SettingsFont, width=18)
        self.cmbYear.grid(row=2, column=2, sticky="w")
        years = ["1. godina", "2.godina", "3. godina", "4. godina"]
        self.cmbYear["values"] = years
        self.cmbYear.state(["readonly"])
        self.cmbYear.current(0)

        self.lblEspb = tk.Label(self, text="Espb", bg='black', fg='white', font=SettingsFont)
        self.lblEspb.grid(row=3, column=1, padx=20, sticky="e")

        self.txtEspb = ttk.Entry(self, font=SettingsFont)
        self.txtEspb.grid(row=3, column=2, sticky="w")

        style = ttk.Style()
        style.configure('TButton', font=SettingsFont, focuscolor='None', activebackground='white')
        style.map('TButton')
        btnSave = ttk.Button(self, text="Sačuvaj", style="TButton", command=lambda: self.BtnSave())
        btnSave.grid(row=6, column=1, columnspan=2)

        self.onSettingsLoaded()


app = tkinterApp()
app.mainloop()
