from pdf import *

from InOut import *

from clipboard import copyToClipboard

from ButtonRadiobutton import *

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Some fonts used for widgets
FONT1 = ("Verdana", 35)
SettingsFont = ('Verdana', 15)
SettingsFontSmaller = ('Verdana', 10)
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
        fw = self.winfo_screenwidth()
        fh = self.winfo_screenheight()
        setWindowSize(int(fw * wp), int(fh * hp))
        self.geometry("%dx%d+%d+%d" % (windowWidth, windowHeight, fw * (1 - wp) / 2, fh * (1 - hp) / 2))
        self.maxsize(windowWidth, windowHeight)
        self.minsize(windowWidth, windowHeight)
        self.iconbitmap("images/icon1.ico")
        self.title("Lista")
        on_app_loading()
        self.protocol("WM_DELETE_WINDOW", func=lambda: on_app_closing(self))

        # Container for holding ButtonRadiobuttons on top
        self.container1 = tk.Frame(self)
        cnt1h = 30
        self.container1.place(height=cnt1h, width=fw)

        self.radio1 = ButtonRadiobutton(self, text='Lista', command=lambda: showCurrentPage(1))
        self.radio1.grid(row=0, column=0, padx=0, pady=0)

        self.radio2 = ButtonRadiobutton(self, text='Rokovi', command=lambda: showCurrentPage(2))
        self.radio2.grid(row=0, column=1, padx=0, pady=0)

        self.radio3 = ButtonRadiobutton(self, text='Dodaj rok', command=lambda: showCurrentPage(3))
        self.radio3.grid(row=0, column=2, padx=0, pady=0)

        self.radio4 = ButtonRadiobutton(self, text='Podesavanja', command=lambda: showCurrentPage(4))
        self.radio4.grid(row=0, column=3, padx=0, pady=0)

        rbs = [self.radio1, self.radio2, self.radio3, self.radio4]
        Pages = [Page1, Page2, Page3, Page4]

        # Container for holding pages
        self.container = tk.Frame(self)
        self.container.place(height=fh - cnt1h, width=fw, y=cnt1h)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}

        for Page in Pages:
            page = Page(parent=self.container)
            self.pages[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        def showCurrentPage(val):
            if val < 1 or val > 4:
                val = 1
            global currentPageNumber
            if currentPageNumber == val:
                return
            rbs[currentPageNumber - 1].config(background='lightgrey')
            rbs[val - 1].config(background='lightblue')
            currentPageNumber = val
            self.show_page(Pages[currentPageNumber - 1])

        showCurrentPage(1)
        # Shows window after 20 ms so that user can't see other widgets
        self.after(20, func=lambda: self.deiconify())


# Page class for showing students ranked
class Page1(tk.Frame):
    def loadPage1(self):
        global students
        students = loadResults(listOfResults, subjects, espb)
        for row in self.listbox.get_children():
            self.listbox.delete(row)
        self.columns = (("", "Indeks") + tuple(
            [f"{x:{4}}" for x in subjects[(year - 1) * 2 + 1]] + [f"{x:{4}}" for x in subjects[(year - 1) * 2 + 2]])
                        + ("Koeficijent",))
        cw = [35, 85] + (len(self.columns) - 3) * [60, ] + [100, ]
        self.listbox.configure(columns=self.columns)
        for ind, column in enumerate(self.columns):
            self.listbox.heading(column, anchor="e", text=column)
            self.listbox.column(column, anchor="e", width=cw[ind])
        self.listbox.column(column="Koeficijent", width=int(self.container.winfo_width() - sum(cw[:-1]) - 22))
        data1 = []
        if type(students) is tuple:
            self.lblAlert.configure(text="Greska sa rezultatom " + students[1][students[1].rindex("/") + 1:]
                                         + ". Ne mozemo da prikazemo listu dok svi rezultati nisu dobro uneti.")
            return
        else:
            self.lblAlert.configure(text="")
        for student in sorted(students, key=lambda x: -students[x]["coef"]):
            data1.append((student,) + tuple([students[student].get(x.strip(), "") for x in self.columns[2:-1]])
                         + (students[student]["coef"],))
        ind = 1
        for item in data1:
            koef = "{:5.2f}".format(item[-1])
            self.listbox.insert("", tk.END, values=(ind,) + item[:-1] + (koef,))
            ind += 1

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.update()
        style = ttk.Style()
        style.configure('Custom.TEntry', foreground='blue', background='lightyellow', borderwidth=2)
        self.container = tk.Frame(self, width=600, height=400)
        self.container.place(x=0.02 * windowWidth, y=0.05 * windowHeight, w=windowWidth * 0.91, h=windowHeight * 0.8)
        self.container.update_idletasks()

        scrollbarx = ttk.Scrollbar(self.container, orient=tk.HORIZONTAL)
        scrollbary = ttk.Scrollbar(self.container)
        self.listbox = ttk.Treeview(self.container, xscrollcommand=scrollbarx.set,
                                    yscrollcommand=scrollbary.set, show="headings")

        self.lblAlert = tk.Label(self, font=("Verdana", 12), text="")
        self.lblAlert.place(x=0.1 * windowWidth, y=0.85 * windowHeight, w=1200)

        scrollbarx.configure(command=self.listbox.xview)
        scrollbary.configure(command=self.listbox.yview)
        scrlH = 20
        self.listbox.place(h=self.container.winfo_height() - scrlH, w=self.container.winfo_width() - scrlH, x=0, y=0)
        scrollbarx.place(h=scrlH, w=self.container.winfo_width() - scrlH, x=0, y=self.container.winfo_height() - scrlH)
        scrollbary.place(h=self.container.winfo_height() - scrlH, w=scrlH, x=self.container.winfo_width() - scrlH, y=0)
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
            btn.config(text="Copied", image=self.okicon)

        self.loadPage1()
        self.copyicon = tk.PhotoImage(file="images/copyicon.png")
        self.okicon = tk.PhotoImage(file="images/okicon.png")
        btn = tk.Button(self, text="Copy", image=self.copyicon, compound=tk.LEFT, background="darkgrey",
                        command=BtnClick)
        btn.place(x=0.94 * windowWidth, y=0.01 * windowHeight, w=0.05 * windowWidth)


# Page class for seeing, changing and deleting saved results
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

        # listbox1 is for showing which results were saved

        container1 = tk.Frame(self, width=0.3 * windowWidth, height=0.7 * windowHeight)
        container1.place(x=0.05 * windowWidth, y=0.05 * windowHeight)
        container1.update_idletasks()

        style = ttk.Style()
        style.configure("Custom.Listbox", font=Font2)
        scrollbarx1 = ttk.Scrollbar(container1, orient=tk.HORIZONTAL)
        scrollbary1 = ttk.Scrollbar(container1)
        self.listbox1 = tk.Listbox(container1, xscrollcommand=scrollbarx1.set,
                                   yscrollcommand=scrollbary1.set, activestyle="none")
        scrollbarx1.configure(command=self.listbox1.xview)
        scrollbary1.configure(command=self.listbox1.yview)
        scrlH = 20
        self.listbox1.place(h=container1.winfo_height() - scrlH, w=container1.winfo_width() - scrlH, x=0, y=0)
        scrollbarx1.place(h=scrlH, w=container1.winfo_width() - scrlH, x=0, y=container1.winfo_height() - scrlH)
        scrollbary1.place(h=container1.winfo_height() - scrlH, w=scrlH, x=container1.winfo_width() - scrlH, y=0)

        # used to track if different listbox1 item is selected, so that unnecessary result loads aren't done
        global old_ind_page2
        old_ind_page2 = -1

        self.listbox1.bind("<<ListboxSelect>>", lambda event: self.changeToSelectedResult())

        # listbox2 is for showing selected result
        container2 = tk.Frame(self, width=0.4 * windowWidth, height=0.7 * windowHeight)
        container2.place(x=0.45 * windowWidth, y=0.05 * windowHeight)
        container2.update_idletasks()

        scrollbarx2 = ttk.Scrollbar(container2, orient=tk.HORIZONTAL)
        scrollbary2 = ttk.Scrollbar(container2)
        self.listbox2 = tk.Text(container2, xscrollcommand=scrollbarx2.set, wrap="none",
                                yscrollcommand=scrollbary2.set, undo=True)
        scrollbarx2.configure(command=self.listbox2.xview)
        scrollbary2.configure(command=self.listbox2.yview)
        scrlH = 20
        self.listbox2.place(h=container2.winfo_height() - scrlH, w=container2.winfo_width() - scrlH, x=0, y=0)
        scrollbarx2.place(h=scrlH, w=container2.winfo_width() - scrlH, x=0, y=container2.winfo_height() - scrlH)
        scrollbary2.place(h=container2.winfo_height() - scrlH, w=scrlH, x=container2.winfo_width() - scrlH, y=0)

        self.loadResultsToPage2()

        btnRemoveResult = tk.Button(self, text="Ukloni rok", font=SettingsFont, command=lambda: self.removeResult())
        btnRemoveResult.place(x=0.85 * windowWidth, y=0.8 * windowHeight)

        def alterResult():
            ind = old_ind_page2
            if ind == -1:
                messagebox.showerror("Greska", "Niste izabrali rok koji zelite da izmenite.")
                return
            res = self.listbox2.get("1.0", tk.END)
            resFileName = self.listbox1.get(ind)
            if len(res) < 1:
                messagebox.showerror("Greska", "Ne mozete da izmenite rok na ovaj nacin.")
                return
            shouldAltRes = messagebox.askyesno("Potvrdite radnju", "Da li zelite da izmenite "
                                               + resFileName[resFileName.rindex("/") + 1:] + " ?")
            if shouldAltRes:
                saveResult(resFileName, res)
                messagebox.showinfo("Obavesetenje", "Izabrani fajl je izmenjen.")
                app.pages[Page1].loadPage1()

        btnAlterResult = tk.Button(self, text="Izmeni rok", font=SettingsFont, command=alterResult)
        btnAlterResult.place(x=0.72 * windowWidth, y=0.8 * windowHeight)


# Page class for adding results
class Page3(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        Font2 = ("Arial", 10)
        container = tk.Frame(self, width=0.4 * windowWidth, height=0.7 * windowHeight)
        container.place(x=0.05 * windowWidth, y=0.05 * windowHeight)
        container.update_idletasks()

        style = ttk.Style()
        style.configure("Custom.Listbox", font=Font2)
        scrollbarx = ttk.Scrollbar(container, orient=tk.HORIZONTAL)
        scrollbary = ttk.Scrollbar(container)
        listbox = tk.Text(container, wrap="none", xscrollcommand=scrollbarx.set,
                          yscrollcommand=scrollbary.set, undo=True)
        scrollbarx.configure(command=listbox.xview)
        scrollbary.configure(command=listbox.yview)
        scrlH = 20
        listbox.place(h=container.winfo_height() - scrlH, w=container.winfo_width() - scrlH, x=0, y=0)
        scrollbarx.place(h=scrlH, w=container.winfo_width() - scrlH, x=0, y=container.winfo_height() - scrlH)
        scrollbary.place(h=container.winfo_height() - scrlH, w=scrlH, x=container.winfo_width() - scrlH, y=0)
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
                messagebox.showerror("Obavestenje", "Niste uneli vazeci rok.")
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
                app.pages[Page1].loadPage1()
                app.pages[Page2].loadResultsToPage2()

            else:
                messagebox.showerror("Obavestenje", "Niste uneli vazeci rok.")

        btnAddResult = tk.Button(self, text="Dodaj rok", font=SettingsFont, command=addResult)
        btnAddResult.place(x=0.7 * windowWidth, y=550)


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

    def on_settings_loaded(self):
        self.txtYearAdm.insert(tk.END, str(yearAdm))
        self.cmbYear.current(year - 1)
        self.txtEspb.insert(tk.END, str(espb))

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.lblYearAdm = tk.Label(self, text="Godina upisa", font=SettingsFont)
        self.lblYearAdm.place(x=10, y=10)

        self.txtYearAdm = tk.Entry(self, font=SettingsFont)
        self.txtYearAdm.place(x=200, y=10, width=120, height=30)

        self.lblYear = tk.Label(self, text="Godina", font=SettingsFont)
        self.lblYear.place(x=30, y=60)

        self.cmbYear = ttk.Combobox(self, font=SettingsFontSmaller)
        self.cmbYear.place(x=200, y=60, width=120, height=30)
        years = ["1. godina", "2.godina", "3. godina", "4. godina"]
        self.cmbYear["values"] = years
        self.cmbYear.state(["readonly"])
        self.cmbYear.current(0)

        self.lblEspb = tk.Label(self, text="Espb", font=SettingsFont)
        self.lblEspb.place(x=20, y=110)

        self.txtEspb = tk.Entry(self, font=SettingsFont)
        self.txtEspb.place(x=200, y=110, width=120, height=30)

        btnSave = tk.Button(self, text="Sacuvaj", font=SettingsFont, command=lambda: self.BtnSave())
        btnSave.place(x=700, y=550)

        self.on_settings_loaded()


app = tkinterApp()
app.mainloop()
