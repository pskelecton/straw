import configparser
import os
pa = os.path.abspath('./conf.env')
a = configparser.ConfigParser()
a.read(pa, encoding="utf-8")
sec = a._sections
conf = sec.get('aaaa')
print(conf)