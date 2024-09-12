import os
from datetime import date


# Returns list of all result file paths
def loadListOfResults():
    lst = list()
    with open("files/listOfResults.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            lst.append(line.strip())
    return lst


# Returns yearAdm(year of admission),year(which year of studies), number of espb that user entered
def loadSettings():
    with open("files/settings.txt", "r") as f:
        s = [x.strip() for x in f.readlines()]
        if len(s) < 3:
            return date.today().year, 1, 60
        badInput0 = False
        badInput1 = False
        badInput2 = False
        if len(s[0]) == 0 or len(s[1]) == 0 or len(s[2]) == 0:
            return date.today().year, 1, 60
        for c in s[0]:
            if not c.isdigit():
                badInput0 = True
                break
        for c in s[1]:
            if not c.isdigit():
                badInput1 = True
                break
        for c in s[2]:
            if not c.isdigit():
                badInput2 = True
                break
        a = date.today().year
        b = 1
        c = 60
        if not badInput0:
            a = int(s[0])
        if not badInput1:
            b = int(s[1])
        if not badInput2:
            c = int(s[2])
        return a, b, c


# Returns dictionary of all subjects and their data
def loadSubjects():
    subjects = dict()
    for i in range(1, 9):
        subjects[i] = list()
    with open("files/subjects.txt", "r") as f:
        for line in f.readlines()[1:]:
            line = line.strip().split(",")
            subName = line[0].strip()
            espb = int(line[1])
            subSem = int(line[2])
            comp = line[3].strip()
            nick = line[4].strip()
            subjects[subSem] = subjects[subSem] + [nick, ]
            subjects[nick] = dict()
            subjects[nick]["espb"] = espb
            subjects[nick]["compulsory"] = comp
            subjects[nick]["semester"] = subSem
            subjects[nick]["name"] = subName
    return subjects


# Saves all result filepaths
def saveListOfResults(lst):
    with open("files/listOfResults.txt", "w", encoding="utf-8") as f:
        for line in lst:
            print(line, file=f)


# Saves yearAdm(year of admission),year(which year of studies), number of espb that user entered
def saveSettings(yearAdm, year, espb):
    with open("files/settings.txt", "w", encoding="utf-8") as f:
        print(yearAdm, file=f)
        print(year, file=f)
        print(espb, file=f)


# Saves result to a given file
def saveResult(fileName, lst):
    text = []
    for line in lst.split("\n"):
        line = line.strip()
        # endInd = len(line) - 1
        # while endInd > 0 and not (line[endInd].isdigit()):
        #     endInd -= 1
        # line = line[:endInd + 1]
        if "соба" in line:
            line = line[:line.index("соба") - 1]
        if "ЕТФ" in line:
            line = line[:line.index("ЕТФ") - 1]
        if ":" not in line and '/0' in line:
            if line[4] == '/':
                text.append(line)
            else:
                text.append(line[line.index("/") - 4:])
    if len(text) == 0:
        return -1
    with open(fileName, "w", encoding="utf-8") as f:
        for line in text:
            print(line, file=f)
    return 1


# Returns dictionary of dictionaries which can be accessed like students[studentIndex][Subject]
def loadResults(listOfResults1, subjects, espb):
    students = dict()
    listOfResults = listOfResults1.copy()
    l1 = [-1, ] * 5
    pom1 = 0
    for i in range(1, 5):
        try:
            ind = listOfResults.index("files/results/" + str(i) + ". godina.txt")
            listOfResults.pop(ind)
            l1[i] = ind
            pom1 = i
        except ValueError:
            continue

    for i in range(4, 0, -1):
        if l1[i] != -1:
            fileName = "files/results/" + str(i) + ". godina.txt"
            result = loadResult(fileName)
            for line in result:
                line = line.replace("\t", " ").strip()
                line = line.split(" ")
                ind = line[0]
                if len(ind) != 9 or ind[0] != "2" or ind[4] != "/":
                    return -1, fileName
                try:
                    coef = float(line[-1])
                except ValueError:
                    return -1, fileName
                if ind not in students:
                    students[ind] = dict()
                    students[ind]["coef"] = 0.0
                students[ind]["coef"] += i * 60 * coef
            break

    term = {"jan": 1, "feb": 2, "jun": 3, "jul": 4, "avg": 5, "sep": 6}
    listOfResults.sort(key=lambda x: -term[x[-9:-6]])
    for fileName in listOfResults:
        subNick = fileName[fileName.rindex('/') + 1:fileName.index('-')]
        yr = (subjects[subNick]["semester"] + 1) // 2
        result = loadResult(fileName)
        coef = 1
        subSemInAYear = (subjects[subNick]["semester"] + 1) % 2 + 1
        if term[fileName[-9:-6]] == subSemInAYear * 2 or term[fileName[-9:-6]] == subSemInAYear * 2 - 1:
            coef = 1.1
        for line in result:
            line = line.replace("\t", " ").strip()
            line = line.split(" ")
            ind = line[0]
            if len(ind) != 9 or ind[0] != "2" or ind[4] != "/":
                print(line)
                return -1, fileName
            try:
                grade = int(line[-1])
            except ValueError:
                return -1, fileName
            if ind not in students and grade > 4:
                students[ind] = dict()
                students[ind]["coef"] = 0.0
            if grade > 4 and subNick not in students[ind]:
                students[ind][subNick] = grade
                if yr > pom1:
                    students[ind]["coef"] += coef * grade * subjects[subNick]["espb"]
    for ind in students:
        students[ind]["coef"] /= espb
    return students


# Returns result from a given file
def loadResult(fileName):
    lst = []
    with open(fileName, "r", encoding="utf-8") as f:
        for line in f.readlines():
            lst.append(line.strip())
        return lst


# Deletes given file
def deleteFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
