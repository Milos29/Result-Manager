from math import inf


# Returns string made by modifying txt that can be used by built-in function eval() to evaluate it
def modifyExpression(txt):
    lst = []
    badTxt = (";", 1)

    while 1:
        try:
            i = txt.index("count")
        except ValueError:
            break

        if txt[i + 5] != "(":
            return badTxt

        j = i + 6
        opCnt = 1

        while j < len(txt):
            if txt[j] == "(":
                opCnt += 1
            if txt[j] == ")":
                opCnt -= 1
            if opCnt == 0:
                break
            j += 1

        if j == len(txt):
            return badTxt

        lst.append(txt[i + 6:j])
        txt = txt[:i] + "COUNT" + txt[j + 1:]

    txt = [x for x in txt.split(",") if x != ""]

    for cond in range(len(txt)):
        i = inf

        for c in ["<", ">", "="]:
            if c in txt[cond]:
                j = txt[cond].index(c)
                if j < i:
                    i = j

        if i == inf:
            if "COUNT" == txt[cond][:5]:
                txt[cond] = txt[cond] + ">0"
            else:
                txt[cond] = txt[cond] + ">5"

            i = len(txt[cond]) - 2
        else:
            try:
                float(txt[cond][i + 1:])
            except ValueError:
                return badTxt

        txt[cond] = txt[cond].replace("=", "==")

        if "COUNT" == txt[cond][:5]:
            txt[cond] = "sum(" + str(modifyExpression(lst[0])[0]) + ")" + txt[cond][5:]
            lst = lst[1:]
        else:
            txt[cond] = "students[student].get(\"" + txt[cond][:i] + "\",1)" + txt[cond][i:]

    return txt, len(txt)


# Evaluates expression and returns string of all students that satisfy all conditions
def evaluateExpression(txt, students, grade):
    grade = str(grade)
    newtxt = ""
    txtcpy = txt
    okChars = [",", "<", "=", ">", "(", ")", '.']
    txt = ''.join([c for c in txtcpy if c.isdigit() or c.isalpha() or c in okChars])

    countCnt1 = txt.count("count")
    countCnt2 = txtcpy.lower().count("count")

    if countCnt1 != countCnt2:
        return "f"

    try:
        txt, len1 = modifyExpression(txt)
        txt = "sum(" + str(txt) + ")==" + str(len1)
        txt = txt.replace("\\", "")
        txt = txt.replace("\'", "")
        print(txt)

        if ";" in txt:
            return "f"

        cnt = 1

        for student in sorted(students, key=lambda x: -students[x]["coef"]):
            if eval(txt):
                newtxt += "{:>3d}".format(cnt) + " " + student + " " + grade + "\n"
                cnt += 1

    except Exception:
        return "f"

    return newtxt
