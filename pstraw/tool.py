
# 字符串true和false转bool型的True和False
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

# bool型的True和False转字符串的True和False
def Bool2Str(boolVar):
    if bool(boolVar):
        return "True"
    else:
        return "False"

# 字符串转整型
def Str2Int(intVar):
    return int(intVar)

# 整型转字符串
def Int2Str(intVar):
    return str(int(intVar))

# 获取第一个不为空的变量
def VarGet(*args):
    for arg in args:
        if arg != None:
            return arg
    return None