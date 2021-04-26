# import configparser
# import os
# pa = os.path.abspath('./conf.env')
# a = configparser.ConfigParser()
# a.read(pa, encoding="utf-8")
# sec = a._sections
# conf = sec.get('aaaa')
# print(conf)

def aaa(*args,**kwargs):
    x = True
    def _aaa_(_fnname):
        print(x)
        def fun(*args,**kwargs):
            print(x)
            return _fnname(*args,**kwargs)
        return fun
    return _aaa_

@aaa()
def bbb():
    return None

bbb()