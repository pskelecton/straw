from pstraw import Straw
import os

case_dir = os.path.dirname(os.path.abspath(__file__))
work_parh = os.getcwd()

db = Straw('test_db_create',CONF_PATH=os.path.join(case_dir,'config.ini'))

@db.sql(SQL_NAME='mysql.ini.sql')
def DropTable(tableName):
    return {"TBNAME":tableName}

@db.sql(SQL_NAME='mysql.ini.sql')
def CreateUserTable():
    return {}

@db.sql(SQL_NAME='mysql.ini.sql')
def CreateClientTable():
    return {}

@db.sql(SQL_NAME='mysql.ini.sql')
def TruncateTable(tableName):
    return {"TBNAME":tableName}

@db.conn('mysql',ALLOW_ROLLBACK=True)
def CreateTables():
    DropTable('USER')
    CreateUserTable()
    DropTable('CLIENT')
    CreateClientTable()

def run():
    CreateTables()
    # print(case_dir)

run()