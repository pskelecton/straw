from pstraw import Straw, Store
import os
from datetime import datetime

case_dir = os.path.dirname(os.path.abspath(__file__))
# work_parh = os.getcwd()

# 指定
db = Straw('test_db_create',
           CONF_PATH=os.path.join(case_dir, 'config.ini'),
           SQL_PATH=os.path.join(case_dir, '.'),
           LOG_PATH=os.path.join(case_dir, '.')
           )

'''
    初始化mysql
'''
@db.sql(SQL_NAME='mysql.ini', SQL_TEMPLATE_TYPE=3)
def DropTable(tableName):
    return {"TBNAME": tableName}


@db.sql(SQL_NAME='mysql.ini', SQL_TEMPLATE_TYPE=3)
def CreateUserTable():
    return {}


@db.sql(SQL_NAME='mysql.ini', SQL_TEMPLATE_TYPE=3)
def CreateClientTable():
    return {}


@db.sql(SQL_NAME='mysql.ini', SQL_TEMPLATE_TYPE=3)
def TruncateTable(tableName):
    return {"TBNAME": tableName}


@db.conn('mysql', ALLOW_ROLLBACK=True)
def CreateMysqlTables():
    DropTable('USER')
    CreateUserTable()
    DropTable('CLIENT')
    CreateClientTable()

CreateMysqlTables()


'''
    初始化postgres
'''
@db.sql(SQL_NAME='postgres.ini', SQL_TEMPLATE_TYPE=6, QUOTATION='\"')
def DropTable(tableName):
    return {"TBNAME": tableName}


@db.sql(SQL_NAME='postgres.ini', SQL_TEMPLATE_TYPE=3)
def CreateUserTable():
    return {}


@db.sql(SQL_NAME='postgres.ini', SQL_TEMPLATE_TYPE=3)
def CreateClientTable():
    return {}


@db.sql(SQL_NAME='postgres.ini', SQL_TEMPLATE_TYPE=6, QUOTATION='\"')
def TruncateTable(tableName):
    return {"TBNAME": tableName}


@db.conn('postgres', ALLOW_ROLLBACK=True)
def CreatePostgresTables():
    DropTable('USER')
    CreateUserTable()
    DropTable('CLIENT')
    CreateClientTable()


CreatePostgresTables()

'''
    插入数据
'''
@db.sql(SQL_NAME='mysql.ini', SQL_TEMPLATE_TYPE=6)
def InsertUser(store):
    return {
        "NAME": store.NAME,
        "USERDESC": store.USERDESC,
        "CREATEBY": 'Chalk Yu',
        "CREATETIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "UPDATEBY":'Chalk Yu',
        "UPDATETIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@db.sql(SQL_NAME='mysql.ini', SQL_TEMPLATE_TYPE=6)
def InsertClient(store):
    return {
        "USERID": store.USERID,
        "PHONE": store.PHONE,
        "CREATEBY": 'Chalk Yu',
        "CREATETIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "UPDATEBY":'Chalk Yu',
        "UPDATETIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@db.sql(SQL_NAME='mysql.ini', SQL_TEMPLATE_TYPE=3)
def TruncateTable(table):
    return {"TBNAME":table}

@db.conn('mysql', ALLOW_ROLLBACK=True)
def Insert2Mysql():
    TruncateTable("USER")
    TruncateTable("CLIENT")
    for id in range(20):
        store = Store({
            "NAME":"Chalk Yu",
            "USERDESC":f"Chalk Test {str(id+1)}",
            "USERID":id+1,
            "PHONE":f'+86-{str(1300000001+id)}'
        })
        InsertUser(store)
        InsertClient(store)

Insert2Mysql()