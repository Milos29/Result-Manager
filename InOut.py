import os
from datetime import date


# Returns list of all result file paths
def loadListOfResults() -> list:
    lst = list()
    filePath = os.path.join("files", "listOfResults.txt")

    with open(filePath, "r", encoding="utf-8") as f:
        for line in f.readlines():
            lst.append(line.strip())

    return lst


# Returns yearAdm(year of admission),year(which year of studies), number of espb that user entered
def loadSettings() -> tuple:
    filePath = os.path.join("files", "settings.txt")

    with open(filePath, "r") as f:
        s = [x.strip() for x in f.readlines()]

        if len(s) < 3:
            return date.today().year, 1, 60

        badInput = [False, False, False]
        defaultSettings = date.today().year, 1, 60

        for i in range(3):
            if len(s[i]) == 0:
                return defaultSettings

            for c in s[i]:
                if not c.isdigit():
                    badInput[i] = True
                    break

        settings = list(defaultSettings)

        for i in range(3):
            if not badInput[i]:
                settings[i] = int(s[i])
        return tuple(settings)


# Returns dictionary of all subjects and their data
def loadSubjects() -> dict:
    subjects = dict()

    for i in range(1, 9):
        subjects[i] = list()

    filePath = os.path.join("files", "subjects.txt")

    with open(filePath, "r") as f:
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
def saveListOfResults(lst: list) -> None:
    filePath = os.path.join("files", "listOfResults.txt")

    with open(filePath, "w", encoding="utf-8") as f:
        for line in lst:
            print(line, file=f)


# Saves yearAdm(year of admission),year(which year of studies), number of espb that user entered
def saveSettings(yearAdm: int, year: int, espb: int) -> None:
    filePath = os.path.join("files", "settings.txt")

    with open(filePath, "w", encoding="utf-8") as f:
        print(yearAdm, file=f)
        print(year, file=f)
        print(espb, file=f)


# Saves result to a given file
def saveResult(fileName: str, lst: str) -> int:
    text = []

    for line in lst.split("\n"):
        line = line.strip()
        endInd = max(indexOfLastCharThatSatisfies(line, str.isdigit), 0)
        line = line[:endInd + 1]

        for word in ["соба", "ЕТФ"]:
            if word in line:
                line = line[:line.index(word) - 1]

        # Assumes all indexes are less than 1000
        if ":" not in line and '/0' in line and line[-1].isdigit():
            text.append(line[line.index("/0") - 4:])

    if len(text) == 0:
        return -1

    with open(fileName, "w", encoding="utf-8") as f:
        for line in text:
            print(line, file=f)
    return 1


# Returns dictionary of dictionaries which can be accessed like students[studentIndex][Subject]
def loadResults(listOfResults1: list, subjects: dict, espb: int):
    students = dict()
    listOfResults = listOfResults1.copy()
    l1 = [-1, ] * 5
    pom1 = 0

    for i in range(1, 5):
        try:
            ind = listOfResults.index(os.path.join("files", "results", str(i) + ". godina.txt"))
            listOfResults.pop(ind)
            l1[i] = ind
            pom1 = i
        except ValueError:
            continue

    for i in range(4, 0, -1):
        if l1[i] != -1:
            fileName = os.path.join("files", "results", str(i) + ". godina.txt")
            result = loadResultsFile(fileName)

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

                students[ind]["coef"] = i * 60 * coef
            break

    examPeriod = {"jan": 1, "feb": 2, "jun": 3, "jul": 4, "avg": 5, "sep": 6}
    listOfResults.sort(key=lambda x: -examPeriod[x[-9:-6]])

    for fileName in listOfResults:
        subNick = os.path.basename(fileName)
        subNick = subNick[:subNick.index('-')]
        yr = (subjects[subNick]["semester"] + 1) // 2
        results = loadResultsFile(fileName)
        coef = 1
        subSemInAYear = (subjects[subNick]["semester"] + 1) % 2 + 1

        if examPeriod[fileName[-9:-6]] == subSemInAYear * 2 or examPeriod[fileName[-9:-6]] == subSemInAYear * 2 - 1:
            coef = 1.1

        for line in results:
            line = line.replace("\t", " ").strip()
            line = line.split(" ")
            ind = line[0]

            if len(ind) != 9 or ind[0] != "2" or ind[4] != "/":
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


# Returns results from a given file
def loadResultsFile(fileName: str) -> list:
    lst = []

    with open(fileName, "r", encoding="utf-8") as f:
        for line in f.readlines():
            lst.append(line.strip())

        return lst


# Deletes given file
def deleteFile(fileName: str) -> None:
    if os.path.exists(fileName):
        os.remove(fileName)


# Returns -1 if there is no such character
def indexOfLastCharThatSatisfies(s: str, f) -> int:
    for i in range(len(s) - 1, -1, -1):
        if f(s[i]):
            return i

    return -1
