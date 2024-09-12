import sys
from functools import wraps

sys.path.insert(0, 'pypdf')
from pypdf import PdfReader


# Reads pdf file and returns list of all lines in it, but removes all data in each line up until
# student index and removes room name at the end of each line, if there is any
def readPdf(filePath):
    if filePath == "":
        return list()
    if filePath[0] == "\"":
        filePath = filePath[1:-1]
    try:
        pdfReader = PdfReader(filePath)
    except Exception:
        return ["Ovo nije fajl sa rezultatima", ]
    text = []
    if len(pdfReader.pages) > 30:
        return ["Ovo nije fajl sa rezultatima.", ]
    for page in pdfReader.pages:
        s = page.extract_text().split("\n")
        for line in s:
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
    if len(text) == 0:
        return ["Ovo nije fajl sa rezultatima.", ]
    return text
