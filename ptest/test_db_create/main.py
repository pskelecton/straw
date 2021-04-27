from pstraw import Straw
import os

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
