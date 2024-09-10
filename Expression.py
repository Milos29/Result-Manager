def evalCOUNT(txt):
    print("evalCount ulaz", txt)
    lst = []
    badTxt = (";", 1)
    while 1:
        try:
            i = txt.index("count")
        except ValueError:
            break
        print(txt, lst, i)
        if txt[i + 5] != "(":
            return badTxt
        j = i + 6
        brLevih = 1
        while j < len(txt):
            if txt[j] == "(":
                brLevih += 1
            if txt[j] == ")":
                brLevih -= 1
            if brLevih == 0:
                break
            j += 1
        if j == len(txt):
            return badTxt
        lst.append(txt[i + 6:j])
        txt = txt[:i] + "COUNT" + txt[j + 1:]
    txt = txt.split(",")
    txt = [x for x in txt if x != ""]
    for cond in range(len(txt)):
        i = 1000000
        if "<" in txt[cond]:
            j = txt[cond].index("<")
            if j < i:
                i = j
        if ">" in txt[cond]:
            j = txt[cond].index(">")
            if j < i:
                i = j
        if "=" in txt[cond]:
            j = txt[cond].index("=")
            if j < i:
                i = j
        if i == 1000000:
            if "COUNT" == txt[cond][:5]:
                txt[cond] = txt[cond] + ">0"
            else:
                txt[cond] = txt[cond] + ">5"
            i = len(txt[cond]) - 2
        else:
            try:
                int(txt[cond][i + 1:])
            except ValueError:
                return badTxt
        txt[cond] = txt[cond].replace("=", "==")
        if "COUNT" == txt[cond][:5]:
            txt[cond] = "sum(" + str(evalCOUNT(lst[0])[0]) + ")" + txt[cond][5:]
            lst = lst[1:]
        else:
            txt[cond] = "students[student].get(\"" + txt[cond][:i] + "\",1)" + txt[cond][i:]
    return txt, len(txt)


# Evaluates expression and returns string of all students that satisfy all conditions
def evaluateExpression(txt, students, grade):
    grade = str(grade)
    newtxt = ""
    txtcpy = txt
    txt = ""
    okChars = [",", "<", "=", ">", "(", ")"]
    for c in txtcpy:
        if c.isdigit() or c.isalpha() or c in okChars:
            txt += c
    br = txt.count("count")
    br1 = txtcpy.lower().count("count")
    if br != br1:
        return "f"
    try:
        txt, l1 = evalCOUNT(txt)
        txt = "sum(" + str(txt) + ")==" + str(l1)
        txt = txt.replace("\\", "")
        txt = txt.replace("\'", "")
        if ";" in txt:
            return "f"
        br = 1
        for student in sorted(students, key=lambda x: -students[x]["coef"]):
            if eval(txt):
                newtxt += "{:>3d}".format(br) + " " + student + " " + grade + "\n"
                br += 1
    except Exception:
        return "f"
    return newtxt
