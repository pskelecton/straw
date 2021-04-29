from pstraw import Straw
from dataclasses import dataclass
from datetime import datetime
import os

case_dir = os.path.dirname(os.path.abspath(__file__))
# 实例化straw对象
db = Straw(
    DB_DRIVER='mysql', # 必须输入
    DB_DATABASE='straw_test', # 必须输入
    DB_USER='root', # 必须输入3306, # mysql默认值：3306 ， postgres默认值：5432
    DB_PASSWORD='root', # 必须输入
    DB_HOST='127.0.0.1', # 默认值：localhost
    DB_PORT='8071', # mysql默认值：3306 ， postgres默认值：5432
    SQL_PATH=os.path.join(case_dir,'.'),# 指定sql路径是当前目录，默认是./sql文件夹
)
'''
  创建一个结构体，用于保存数据对象
'''
@dataclass
class USER():
    ID: int
    NAME: str
    USERDESC: str

'''
  @db.sql注解：绑定一个sql方法
  -- SQL_TEMPLATE_TYPE = 1， 通过python字符串的%s占位符替换
'''
@db.sql(USER,SQL_NAME='dml',SQL_TEMPLATE_TYPE=1)
def TempType1():
    # 返回值类型是tuple，按位置顺序替换sql中的%s
    return ("('Chalk Test 5','Chalk Test 6')",)

'''
  @db.sql注解：绑定一个sql方法
  -- SQL_TEMPLATE_TYPE = 2， 通过参数{0} ~ {n}的形式接收内容
'''
@db.sql(USER,SQL_NAME='dml',SQL_TEMPLATE_TYPE=2)
def TempType2():
    # 返回值类型是tuple，以参数的形式传递到sql中
    return ("('Chalk Test 5','Chalk Test 6')","USERDESC")

'''
  @db.sql注解：绑定一个sql方法
  -- SQL_TEMPLATE_TYPE = 3， 字典键值匹配
  -- 例如  :USERDESC1 匹配@sql注解方法返回值{"USERDESC1":value1,"USERDESC2":value2}中的value1
'''
@db.sql(USER,SQL_NAME='dml',SQL_TEMPLATE_TYPE=3)
def TempType3():
    # 返回值类型是dict，按照dict的key来绑定
    return {"USERDESC1":"'Chalk Test 5'","USERDESC2":"'Chalk Test 6'"}

'''
  @db.sql注解：绑定一个sql方法
  -- SQL_TEMPLATE_TYPE = 4， 通过python字符串的%s占位符替换
'''
@db.sql(USER,SQL_NAME='dml',SQL_TEMPLATE_TYPE=4)
def TempType4():
    # 返回值类型是tuple，按位置顺序替换sql中的%s，自动填充引号
    # 组成的sql字符串：SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN ('Chalk Test 5','Chalk Test 6');
    return ("Chalk Test 5","Chalk Test 6")

'''
  @db.sql注解：绑定一个sql方法
  -- SQL_TEMPLATE_TYPE = 5， 通过参数{0} ~ {n}的形式接收内容
'''
@db.sql(USER,SQL_NAME='dml',SQL_TEMPLATE_TYPE=5)
def TempType5():
    # 返回值类型是tuple，以参数的形式传递到sql中，自动填充引号
    # 组成的sql字符串：SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN ('Chalk Test 5','Chalk Test 6');
    return ("Chalk Test 5","Chalk Test 6")

'''
  @db.sql注解：绑定一个sql方法
  -- SQL_TEMPLATE_TYPE = 6， 字典键值匹配
  -- 例如  :USERDESC1 匹配@sql注解方法返回值{"USERDESC1":value1,"USERDESC2":value2}中的value1
'''
@db.sql(USER,SQL_NAME='dml',SQL_TEMPLATE_TYPE=6)
def TempType6():
    # 返回值类型是dict，按照dict的key来绑定，自动填充引号
    # 组成的sql字符串：SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN ('Chalk Test 5','Chalk Test 6');
    return {"USERDESC1":"Chalk Test 5","USERDESC2":"Chalk Test 6"}

'''
  @db.sql注解：绑定一个sql方法
  -- QUOTATION参数改变自动填充的引号类型，默认单引号
'''
@db.sql(USER,SQL_NAME='dml',SQL_TEMPLATE_TYPE=5,QUOTATION="\"")
def quotationType():
    # 自动填充双引号
    # 组成的sql字符串：SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN ("Chalk Test 5","Chalk Test 6");
    return ("Chalk Test 5","Chalk Test 6")

'''
  @db.sql注解：绑定一个sql方法
  -- SQL_TEMPLATE_TYPE如果没有指定，默认值：SQL_TEMPLATE_TYPE=6
'''
@db.sql(USER,SQL_NAME='dml')
def defaultTempType():
    # 按照SQL_TEMPLATE_TYPE=6的方式解析
    # 组成的sql字符串：SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN ('Chalk Test 5','Chalk Test 6');
    return {"USERDESC1":"Chalk Test 5","USERDESC2":"Chalk Test 6"}

'''
  @db.conn注解：创建一个连接
  注意1：@db.sql注解的方法只能在@db.conn中被调用，但@db.sql可以调任何无注解方法
  注意2：@db.conn可以调用任何无注解方法，也可以被任何无注解方法调用，但不能调用@db.conn注解的方法
'''
# 通过注解创建一个链接
@db.conn()
def ExecSQL():
  tt1 = TempType1()
  print("TempType1 --> ",tt1)
  tt2 = TempType2()
  print("TempType2 --> ",tt2)
  tt3 = TempType3()
  print("TempType3 --> ",tt3)
  tt4 = TempType4()
  print("TempType4 --> ",tt4)
  tt5 = TempType5()
  print("TempType5 --> ",tt5)
  tt6 = TempType6()
  print("TempType6 --> ",tt6)
  qt = quotationType()
  print("quotationType --> ",qt)
  dt = defaultTempType()
  print("defaultTempType --> ",dt)

ExecSQL()