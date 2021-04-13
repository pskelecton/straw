# Straw 数据管
[![beta:0.9.x](https://img.shields.io/badge/Beta-0.9.x-yellow)](https://pypi.org/project/pstraw/) [![license:MIT](https://img.shields.io/badge/License-MIT-green)](https://github.com/pskelecton/straw/blob/master/pstraw/LICENSE) [![python:>=3.7](https://img.shields.io/badge/Python-%3E%3D%203.7-blue)](https://www.python.org/downloads/) [![SQL@Support:postgres|mysql](https://img.shields.io/badge/SQL%40Support-postgres%20%7C%20mysql-lightgrey)](https://github.com/pskelecton/straw) 

简单的函数调用来处理数据库

## 快速开始

- 运行环境

[![python:>=3.7](https://img.shields.io/badge/Python-%3E%3D%203.7-blue)](https://www.python.org/downloads/)

- 安装
```shell
# 安装straw库
pip install pstraw
# 安装数据库驱动(二选一)
pip install pymysql # mysql
pip install psycopg2 # postgres
```

- 快速使用
```python
from pstraw import Straw

db = Straw(DB_DRIVER='mysql',DB_DATABASE='demo_db',DB_USER='root',DB_PASSWORD='root',DB_HOST='localhost',DB_PORT=3306)

@dataclass
class USER_TABLE():
    ID: int
    USER: str
    PASSWORD: str
    CREATE_TIME:datetime
    CREATE_BY: str
    UPDATE_TIME:datetime
    UPDATE_BY: str

@db.sql(USER_TABLE,SQL='SELECT * FROM USER_TABLE WHERE USER = :USER',SQL_TEMPLATE_TYPE=6)
def SearchUser(user:str):
    return {'USER':user}

@db.conn()
def ExecSQL():
    res:list(USER_TABLE) = SearchUser('Chalk Yu')
    for userStore in res:
        print(f'ID={userStore.ID}',f'USER={userStore.USER}',f'PASSWORD={userStore.PASSWORD}')

if __name__ == '__main__':
    ExecSQL()

```

