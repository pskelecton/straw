# Straw 数据管 :zap:
[![beta:0.9.x](https://img.shields.io/badge/Beta-0.9.7-yellow)](https://pypi.org/project/pstraw/) [![license:MIT](https://img.shields.io/badge/License-MIT-green)](https://github.com/pskelecton/straw/blob/master/pstraw/LICENSE) [![python:>=3.7](https://img.shields.io/badge/Python-%3E%3D%203.7-blue)](https://www.python.org/downloads/) [![SQL@Support:postgres|mysql](https://img.shields.io/badge/SQL%40Support-postgres%20%7C%20mysql-lightgrey)](https://github.com/pskelecton/straw) 

**简单的函数调用来处理数据库**

> Straw可以方便的在多个不同的数据库之间传输数据，只需要调用一个方法把数据取出来，再调用一个方法把数据插到另一个数据库中
> 他可以像<i><b>MyBatis</b></i>一样，分离sql层和逻辑层，但又不同于<i><b>MyBatis</b></i>的是你可以在脚本中使用它，你还可以同时连接多个数据库
> 如果你只想写一个简单的脚本，把爬到的数据插到数据中，<font color="red"><b>Straw</b></font>会非常简单
------------

## 快速开始

- 运行环境

[![python:>=3.7](https://img.shields.io/badge/Python-%3E%3D%203.7-blue)](https://www.python.org/downloads/)

- 安装
```shell
# 安装straw库
pip install pstraw
```

- 快速使用

[![源文件](https://img.shields.io/badge/Link-%E6%BA%90%E7%A0%81-orange)](https://github.com/pskelecton/straw/blob/master/ptest/test_quick_to_use/main.py)

```python
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
```

## 基本调用

### 通过SQL的方式调用

[![源文件](https://img.shields.io/badge/Link-%E6%BA%90%E7%A0%81-orange)](https://github.com/pskelecton/straw/blob/master/ptest/test_exec_by_sql/main.py)

```python
from pstraw import Straw
from dataclasses import dataclass
from datetime import datetime
# 实例化straw对象
db = Straw(
    DB_DRIVER='mysql', # 必须输入
    DB_DATABASE='straw_test', # 必须输入
    DB_USER='root', # 必须输入3306, # mysql默认值：3306 ， postgres默认值：5432
    DB_PASSWORD='root', # 必须输入
    DB_HOST='127.0.0.1', # 默认值：localhost
    DB_PORT='8071', # mysql默认值：3306 ， postgres默认值：5432
    USE_BEAN=True # 是否使用结构体用于查询后的数据注入
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
  通过SQL参数绑定一个sql查询语句，@db.sql注解的第一个参数是上面定义的结构体
  注意：这只有查询的时候才会用到
'''
@db.sql(USER,SQL='SELECT * FROM USER WHERE NAME = :NAME AND ID > :MINID')
def SearchUser(name:str,minId:int):
    '''
      函数返回的参数是个字典，其中字典的key：'USER'对应SQL语句中的:USER
      如果user='Chalk Yu'，那么这个方法执行的就是：
      SELECT * FROM USER_TABLE WHERE USER = 'Chalk Yu'
    '''
    return {'NAME':name,'MINID':minId}

'''
    @db.sql注解：绑定一个sql方法
    插入数据
'''
@db.sql(SQL='INSERT INTO CLIENT(USERID,PHONE) VALUES (:USERID,:PHONE)')
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
    验证插入成功
'''
@db.sql(CLIENT,SQL='SELECT ID,USERID,PHONE FROM CLIENT WHERE USERID > :MINID')
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
```

### 通过SQL_NAME指定一个sql文件

[![源文件](https://img.shields.io/badge/Link-%E6%BA%90%E7%A0%81-orange)](https://github.com/pskelecton/straw/blob/master/ptest/test_exec_by_sql_file/main.py)

#### 目录结构如下
```
|-- [项目文件夹]
    | -- test_exec_by_sql_file.py
    | -- InsertClient.sql
    | -- SelectClient.sql
    | -- SelectUser.sql
```
#### 代码如下
 - InsertClient.sql
```sql
-- 新增CLIENT
INSERT INTO CLIENT(USERID,PHONE) VALUES (:USERID,:PHONE);
```
 - SelectClient.sql
```sql
-- 查询CLIENT数据
SELECT ID,USERID,PHONE FROM CLIENT WHERE USERID > :MINID;
```
 - SelectUser.sql
```sql
-- 查询USER数据
SELECT * FROM USER WHERE NAME = :NAME AND ID > :MINID;
```
 - test_exec_by_sql_file.py
```python
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
  SQL_NAME为要读入sql的文件名
  这里相当于读取./select_user.sql文件
'''
@db.sql(USER,SQL_NAME='SelectUser')
def SearchUser(name:str,minId:int):
    '''
      函数返回的参数是个字典，其中字典的key：'USER'对应SQL语句中的:USER
      如果user='Chalk Yu'，那么这个方法执行的就是：
      SELECT * FROM USER_TABLE WHERE USER = 'Chalk Yu'
    '''
    return {'NAME':name,'MINID':minId}

'''
    @db.sql注解：绑定一个sql方法
    插入数据
'''
@db.sql(SQL_NAME='InsertClient')
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
    验证插入成功
'''
@db.sql(CLIENT,SQL_NAME='SelectClient')
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
```

### 通过@model(func_name)在一个sql文件中绑定多个方法

> 绑定一个sql文件的一段sql语句

### SQL_TEMPLATE_TYPE选择模板方式

> 1 ~ 6 六种模板 

### ALLOW_ROLLBACK自动回滚和AUTO_COMMIT自动提交

> 在自动提交状态下可以设置数据库异常时是否回滚
> 手动提交状态下，需要手动调用commit和rollback

## 框架使用

### SQL方法自动绑定

> 通过模块文件路径自动绑定sql文件的路径

### 日志模块化

> 调试模式
> 外部调用日志打印
> 外部调用控制台打印
> DEBUG模式开关

## 服务端引入

### sql文件缓存

> 可以一次性把sql全部加载到内存中，但前期初始化时间较长，建议在服务端使用

## 多数据库传输

### 数据库缓存

> 数据传递很频繁的时候，需要预先配置好多个数据库连接信息，通过@entry注解做连接缓存，但缓存中的数据库不会自动关闭，需要手动关闭

## sqlalchemy参数自定义

> 本项目采用的orm是sqlalchemy库，所以可以直接通过sqlalchemy来指定各种连接功能

### ssl连接

> 通过sqlalchemy的自定义参数实现ssl连接

## 配置加载

### CONF_PATH配置文件读取

> 指定一个配置文件

### ENV_DIR环境切换

> 通过环境类型来指定一个配置文件

## 外部orm扩展

> 利用loader扩展外部orm
### 外载ORM_LOADER

### 重写loader方法
> RW_CONNECT / RW_EXECUTE / RW_COMMIT / RW_ROLLBACK / RW_CLOSE / RW_INJECT

### 通过重写loader实现sql脚本生成器

## API接口

### 参数API
- Straw参数

| 参数 | 类型 | 默认值 | 说明 |
| ------------ | :------------: | ------------ | ------------ |
| DB_DRIVER | str | None | 驱动类型 "mysql" \| "postgres"
| DB_DATABASE | str | "localhost" | 数据库名
| DB_USER | str | None | 用户名
| DB_PASSWORD | str | None  |  密码
| DB_HOST | str | None |  数据库连接地址
| DB_PORT | int | 3306 \| 5432 |  端口号，默认mysql或者postgres的端口
| SQLITE_PATH | str | None |  sqlite db文件路径
| ENCODING | str | 'utf-8' |  数据库编码
| SQLALCHEMY_ARGS | dict | {'create_engine':None,<br/>'sessionmaker':None,<br/>'scoped_session':None} | sqlalchemy扩展参数
| CONF_PATH | str | None |  配置文件路径
| ENV_DIR | str | "." |  环境参数目录
| SQL_PATH | str | "." |  sql文件目录
| LOG_PATH | str | "." |  log文件目录
| LOG_ON | bool | False |  是否写入log文件
| ENV_ON | bool | False |  是否使用环境参数
| ENV_TYPE | str | "dev" |  指定名dev.ini的环境配置文件
| ENV_DIR | str | "./env" |  环境配置文件指定的目录
| DEBUG | bool | False |  是否开启debug模式
| LOG_MAX_SIZE | int | 10 |   log文件最大mb
| LOG_BACKUP_CNT | int | 1 |  log文件最大备份数
| TRACK_SQL_FILE | bool | False |  根据model目录来映射sql路径
| MODEL_FOLDER_NAME | str | "straw" |   model目录名称
| USE_BEAN | bool | True |  默认是否使用bean
| ALLOW_ROLLBACK | bool | True |  异常是否自动回滚
| AUTO_COMMIT | bool | True |  是否自动提交
| SQL_TEMPLATE_TYPE | int | 6 | 模板类型 1\|2\|3\|4\|5\|6
| MAX_SQL_SIZE | int | 1024*512 | 可识别最大sql长度
| QUOTATION | str | '\'' | sql字符串所用的引号类型  \'\|\"\|\`
| ORM_LOADER | type(OrmLoader) | None |  驱动插件扩展(oracle/sqlserver等)
| RW_CONNECT | type(FunctionType) | None |  重写loader的connect方法
| RW_EXECUTE | type(FunctionType) | None |  重写loader的execute方法
| RW_CLOSE | type(FunctionType) | None |  重写loader的close方法
| RW_COMMIT | type(FunctionType) | None |  重写loader的commit方法
| RW_ROLLBACK | type(FunctionType) | None |  重写loader的rollback方法
| RW_INJECT | type(FunctionType) | None |  重写loader的inject方法
| HARD_LOAD_SQL | bool | False |  是否每次都重新读取sql文件
| CACHE_CONNECT | bool | False |  缓存数据库连接，并保持不关闭
| DB_CONF | dict | None | 缓存数据库连接时，需要配置的数据库信息<br>{[DbModelName]:{'DB_DRIVER':?,'DB_DATABASE':?,...}}

- @Straw.sql参数

| 参数 | 类型 | 默认值   | 说明 |
| ------------ | :------------: | ------------ | ------------ |
| [Bean] | type(Bean) |   | 结构体
| SQL_TEMPLATE_TYPE | int | 6 | 模板类型 1\|2\|3\|4\|5\|6
| SQL_NAME | str | None |  直接绑定sql文件
| SQL | str | None |  直接绑定sql语句
| HARD_LOAD_SQL | bool | False |  是否每次都重新读取sql文件

- @Straw.conn参数

| 参数 | 类型 | 默认值  | 说明 |
| ------------ | :------------: | ------------ | ------------ |
| [DbModelName]] | type(Bean) |   | 缓存数据库连接的情况下根据这个名称拿到连接对象
| ALLOW_ROLLBACK | bool | True | 异常是否自动回滚
| AUTO_COMMIT | bool | True | 是否自动提交

- @Straw.entry参数

| 参数 | 类型 | 默认值  | 说明 |
| ------------ | :------------: | ------------ | ------------ |
| START_GUIDE | bool | False | 启动向导，自动生成文件夹以及模板
| CACHE_SQLS | bool | False | 是否缓存所有sqls数据（HARD_LOAD_SQL=True不做任何缓存）

### 可调用方法、类
  - Straw [主类]
  - Store [数据对象生成类]
  - ConfStore [配置生成类]
  - GlobalConfig [全局参数引用对象]
  - Transition [加载注入SQL工具]
  - OrmLoader [loader接口类]
  - Bean [bean接口类]

### Straw对象的方法
> 初始化调用Straw()返回一个Straw对象，可调用方法如下所示
 
 - 装饰器函数

   - @sql() [sql绑定]
   - @conn() [数据库连接]
   - @entry() [入口]
 
 - 数据库操作函数
  
   - connect(DB_CONF=DB_CONF) [连接数据库]
   - execute(connection,sql,sqlAction=None) [执行sql]
   - commit(connection) [提交]
   - rollback(connection) [回滚]
   - close(connection) [关闭数据库]
   - inject() [实现注入]
 
 - 缓存处理函数
  
   - getAccessHeadStr() [获取数据库配置列表]
   - cacheSqlFiles() [缓存所有的sql文件]
   - cacheDbConn() [根据数据库配置列表连接所有的数据库，并缓存]
 
 - 向导函数
  
   - runGuide() [自动生成框架文件夹与模板]
 
 - 调试、日志、输出
  
   - logging(level,msg,*msgs) [输出在日志文件]
   - print(level,msg,*msgs) [输出在控制台]

