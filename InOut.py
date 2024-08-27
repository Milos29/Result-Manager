import os
from datetime import date

# Returns list of all result filepaths
def loadListOfResults():
    lst = list()
    with open("files/listOfResults.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            lst.append(line.strip())
    return lst


# Returns yearAdm(year of admission),year(which year of studies)
def loadSettings():
    with open("files/settings.txt", "r") as f:
        s = f.readlines()
        if len(s) < 2:
            return date.today().year, 1
        else:
            return int(s[0]), int(s[1])

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
        for l in lst:
            print(l, file=f)


# Saves settings like yearAdm(year of admission),year(which year of studies)
def saveSettings(yearAdm, year):
    with open("files/settings.txt", "w", encoding="utf-8") as f:
        print(yearAdm, file=f)
        print(year, file=f)


# Saves result to a given file
def saveResult(fileName, lst):
    text = []
    endInd = 0
    for line in lst.split("\n"):
        endInd = len(line) - 1
        while endInd > 0 and not (line[endInd].isdigit()):
            endInd -= 1
        line = line[:endInd + 1]
        if "соба" in line:
            line = line[:line.index("соба") - 1]
        if "ЕТФ" in line:
            line = line[:line.index("ЕТФ") - 1]
        if ":" not in line and '/0' in line and line[-1].isdigit():
            if line[4] == '/':
                text.append(line)
            else:
                text.append(line[line.index("/") - 4:])
    text.sort()
    if len(text) == 0:
        return -1
    with open(fileName, "w", encoding="utf-8") as f:
        for line in text:
            print(line, file=f)
    return 1


def loadResults1(lst):
    students = dict()


# Returns result from a given file
def getResult(fileName):
    lst = []
    with open(fileName, "r", encoding="utf-8") as f:
        for line in f.readlines():
            lst.append(line.strip())
        return lst

# Returns given file
def deleteFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
