# Straw 数据管 :zap:
[![beta:0.9.x](https://img.shields.io/badge/Beta-0.9.x-yellow)](https://pypi.org/project/pstraw/) [![license:MIT](https://img.shields.io/badge/License-MIT-green)](https://github.com/pskelecton/straw/blob/master/pstraw/LICENSE) [![python:>=3.7](https://img.shields.io/badge/Python-%3E%3D%203.7-blue)](https://www.python.org/downloads/) [![SQL@Support:postgres|mysql](https://img.shields.io/badge/SQL%40Support-postgres%20%7C%20mysql-lightgrey)](https://github.com/pskelecton/straw) 

简单的函数调用来处理数据库

## 快速开始

- 运行环境

[![python:>=3.7](https://img.shields.io/badge/Python-%3E%3D%203.7-blue)](https://www.python.org/downloads/)

- 安装
```shell
# 安装straw库
pip install pstraw
```

- 快速使用
```python
from pstraw import Straw
# 实例化straw对象
db = Straw(
    DB_DRIVER='mysql',
    DB_DATABASE='demo_db',
    DB_USER='root',
    DB_PASSWORD='root',
    DB_HOST='localhost',
    DB_PORT=3306
)
# 创建一个结构体，用于保存数据对象
@dataclass
class USER_TABLE():
    ID: int
    USER: str
    PASSWORD: str
    CREATE_TIME:datetime
    CREATE_BY: str
    UPDATE_TIME:datetime
    UPDATE_BY: str
# 绑定一条sql语句，函数的返回值为sql中的参数映射
@db.sql(USER_TABLE,SQL='SELECT * FROM USER_TABLE WHERE USER = :USER')
def SearchUser(user:str):
    return {'USER':user}
# 通过注解创建一个链接
@db.conn()
def ExecSQL():
    # 调用函数来执行sql，函数调用的返回值res为sql查询的结果
    res:list(USER_TABLE) = SearchUser('Chalk Yu')
    for userStore in res:
        print(f'ID={userStore.ID}',f'USER={userStore.USER}',f'PASSWORD={userStore.PASSWORD}')

if __name__ == '__main__':
    ExecSQL()

```

- 参数API
  - Straw参数
    | 参数 | 类型 | 默认值 | 必输项 | 取值范围 | 说明 |
    | ------------ | :------------: | :------------: | :------------: | ------------ | ------------ |
    | DB_DRIVER | str | None | :o: | "mysql" \| "postgres" | 驱动类型
    | DB_DATABASE | str | None | :o: | | 数据库名
    | DB_USER | str | None | :o: | | 用户名
    | DB_PASSWORD | str | None | :o: | | 密码
    | DB_HOST | str | None | :o: | | 数据库连接地址
    | DB_PORT | int | 3306 \| 2345 | | | 端口号，默认mysql或者postgres的端口
    | CONF_PATH | str | None |  |  | 配置文件路径
    | ENV_DIR | str | . |  |  | 环境参数目录
    | SQL_PATH | str | . |  |  | sql文件目录
    | LOG_PATH | str | . |  |  | log文件目录
    | LOG_ON | bool | False |  |  | 是否写入log文件
    | ENV_ON | bool | False |  |  | 是否使用环境参数目录
    | DEBUG | bool | False |  |  | 是否开启debug模式
    | LOG_MAX_SIZE | int | 10 |  |  | log文件最大mb
    | LOG_BACKUP_CNT | int | 1 |  |  | log文件最大备份数
    | TRACK_SQL_FILE | bool | False |  |  | 根据model目录来映射sql路径
    | MODEL_FOLDER_NAME | str | "straw" |  |  | model目录名称
    | USE_BEAN | bool | True |  |  | 默认是否使用bean
    | ALLOW_ROLLBACK | bool | True |  |  | 异常是否自动回滚
    | AUTO_COMMIT | bool | True |  |  | 是否自动提交
    | SQL_TEMPLATE_TYPE | int | 6 |  | 1\|2\|3\|4\|5\|6 | 模板类型
    | ORM_LOADER | type(OrmLoader) | None |  |  | 驱动插件扩展(oracle/sqlserver等)

  - @Straw.sql参数
    | 参数 | 类型 | 默认值 | 必输项 | 取值范围 | 说明 |
    | ------------ | :------------: | :------------: | :------------: | ------------ | ------------ |
    | [Bean] | type(Bean) |  |  |  | 结构体
    | SQL_TEMPLATE_TYPE | int | 6 |  | 1\|2\|3\|4\|5\|6 | 模板类型
    | USE_BEAN | bool | True |  |  | 默认是否使用bean
    | SQL_NAME | str | None |  |  | 直接绑定sql文件
    | SQL | str | None |  |  | 直接绑定sql语句

  - @Straw.conn参数
    | 参数 | 类型 | 默认值 | 必输项 | 取值范围 | 说明 |
    | ------------ | :------------: | :------------: | :------------: | ------------ | ------------ |
    | ALLOW_ROLLBACK | bool | True |  |  | 异常是否自动回滚
    | AUTO_COMMIT | bool | True |  |  | 是否自动提交

  - @Straw.enter参数
    | 参数 | 类型 | 默认值 | 必输项 | 取值范围 | 说明 |
    | ------------ | :------------: | :------------: | :------------: | ------------ | ------------ |
    | 待扩展 |  |  |  |  |
