from pstraw import Straw
import os

case_dir = os.path.dirname(os.path.abspath(__file__))
work_parh = os.getcwd()

db = Straw('test_db_create',
           CONF_PATH=os.path.join(case_dir, 'config.ini'),
           SQL_PATH=os.path.join(case_dir, '.'),
           LOG_PATH=os.path.join(case_dir, '.')
           )


@db.sql(SQL_NAME='mysql.ini.sql', SQL_TEMPLATE_TYPE=3)
def DropTable(tableName):
    return {"TBNAME": tableName}


@db.sql(SQL_NAME='mysql.ini.sql', SQL_TEMPLATE_TYPE=3)
def CreateUserTable():
    return {}


@db.sql(SQL_NAME='mysql.ini.sql', SQL_TEMPLATE_TYPE=3)
def CreateClientTable():
    return {}


@db.sql(SQL_NAME='mysql.ini.sql', SQL_TEMPLATE_TYPE=3)
def TruncateTable(tableName):
    return {"TBNAME": tableName}


@db.conn('mysql1', ALLOW_ROLLBACK=True)
def CreateTables():
    DropTable('USER')
    CreateUserTable()
    DropTable('CLIENT')
    CreateClientTable()


def run():
    CreateTables()
    # print(case_dir)


run()
