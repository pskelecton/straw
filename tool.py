
def Str2Bool(boolVar):
    if type(boolVar) == str:
        if boolVar.lower() == 'true':
            return True
        elif boolVar.lower() == 'false':
            return False
        else:
            return bool(boolVar)
    else:
        return bool(boolVar)


def Bool2Str(boolVar):
    if bool(boolVar):
        return "True"
    else:
        return "False"


def Str2Int(intVar):
    return int(intVar)


def Int2Str(intVar):
    return str(int(intVar))
