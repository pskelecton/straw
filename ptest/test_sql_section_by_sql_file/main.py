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
    VALID:int
    CREATEBY: str
    CREATETIME:datetime
    UPDATEBY: str
    UPDATETIME:datetime

@dataclass
class CLIENT():
    ID:int
    USERID:str
    PHONE:str

'''
  @db.sql注解：绑定一个sql方法
  读取./dml.sql文件，并绑定@model`SearchUser`注解的sql语句
'''
@db.sql(USER,SQL_NAME='dml')
def SearchUser(name:str,minId:int):
    '''
      函数返回的参数是个字典，其中字典的key：'USER'对应SQL语句中的:USER
      如果user='Chalk Yu'，那么这个方法执行的就是：
      SELECT * FROM USER_TABLE WHERE USER = 'Chalk Yu'
    '''
    return {'NAME':name,'MINID':minId}

'''
    @db.sql注解：绑定一个sql方法
    读取./dml.sql文件，并绑定@model`AddClient`注解的sql语句
'''
@db.sql(SQL_NAME='dml')
def AddClient(userId:str,phone:str):
  return {
        "USERID": userId,
        "PHONE": phone,
        "CREATEBY": 'test_exec_by_sql',
        "CREATETIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "UPDATEBY":'test_exec_by_sql',
        "UPDATETIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
'''
    @db.sql注解：绑定一个sql方法
    读取./dml.sql文件，并绑定@model`SearchClient`注解的sql语句
'''
@db.sql(CLIENT,SQL_NAME='dml')
def SearchClient(minId:int):
  return {'MINID':minId}
'''
  @db.conn注解：创建一个连接
  注意1：@db.sql注解的方法只能在@db.conn中被调用，但@db.sql可以调任何无注解方法
  注意2：@db.conn可以调用任何无注解方法，也可以被任何无注解方法调用，但不能调用@db.conn注解的方法
'''
# 通过注解创建一个链接
@db.conn()
def ExecSQL():
    minId = 18
    clients = SearchClient(minId)
    print("Pre --> ",clients)
    # 调用函数来执行sql，函数调用的返回值res为sql查询的结果
    users:list(USER) = SearchUser('Chalk Yu',18)
    for userStore in users:
        print(f'ID={userStore.ID}',f'NAME={userStore.NAME}',f'USERDESC={userStore.USERDESC}',f'CREATETIME={userStore.CREATETIME}')
        AddClient(userStore.ID,13600000000+userStore.ID)
    clients = SearchClient(minId)
    print("Aft --> ",clients)

ExecSQL()