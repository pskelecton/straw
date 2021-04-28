from pstraw import Straw
from dataclasses import dataclass
import datetime
# 实例化straw对象
db = Straw(
    DB_DRIVER='mysql',
    DB_DATABASE='straw_test',
    DB_USER='root',
    DB_PASSWORD='root',
    DB_HOST='localhost',
    DB_PORT=8071
)
# 创建一个结构体，用于保存数据对象
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
# 绑定一条sql语句，函数的返回值为sql中的参数映射
@db.sql(USER,SQL='SELECT * FROM USER WHERE NAME = :NAME')
def SearchUser(name:str):
    return {'NAME':name}
# 通过注解创建一个链接
@db.conn()
def ExecSQL():
    # 调用函数来执行sql，函数调用的返回值res为sql查询的结果
    users:list(USER) = SearchUser('Chalk Yu')
    for userStore in users:
        print(f'ID={userStore.ID}',f'NAME={userStore.NAME}',f'USERDESC={userStore.USERDESC}',f'CREATETIME={userStore.CREATETIME}')

ExecSQL()