import sys
import functools

sys.path.insert(0, 'PyPDF2')
import PyPDF2


# Reads pdf file and returns list of all lines in it, but removes all
# data in each line up until student index and removes room name at the end of each line, if there is any
def read_pdf(file_path):
    if file_path == "":
        return list()
    if file_path[0] == "\"":
        file_path = file_path[1:-1]
    with open(file_path, 'rb') as file:
        try:
            pdf_reader = PyPDF2.PdfReader(file)
        except PyPDF2.errors.PdfReadError:
            return ["Ovo nije fajl sa rezultatima.", ]
        text = []
        if len(pdf_reader.pages) > 30:
            return ["Ovo nije fajl sa rezultatima.", ]
        for page in pdf_reader.pages:
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
                if ":" not in line and '2023/0' in line and line[-1].isdigit():
                    if line[4] == '/':
                        text.append(line)
                    else:
                        text.append(line[line.index("/") - 4:])
    text.sort()
    if len(text) == 0:
        return ["Ovo nije fajl sa rezultatima.", ]
    return text
