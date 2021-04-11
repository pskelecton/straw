from promise import Promise
from .screws import Store
from .loader import SqlParser

class sqlLoad():
    def __init__(self, sqlPath):
        self.sqlPath = sqlPath
        self.__sqlChips__ = None

    def __enter__(self):
        sqlChips = Store()
        if type(self.sqlPath) == str:
            with open(self.sqlPath, "r", encoding='utf-8') as fs_sql:
                sql = fs_sql.read()
                sqlChips._default_ = sql
                tmpModuleFnName = None
                sqlLines = sql.split('\n')
                for sqlLine in sqlLines:
                    if sqlLine.strip()[:2]=='@@':
                        tmpModuleFnName = sqlLine.strip()[2:]
                        sqlChips[tmpModuleFnName] = ""
                    else:
                        if tmpModuleFnName != None:
                            sqlChips[tmpModuleFnName] = sqlChips[tmpModuleFnName] + '\n' + sqlLine
        self.__sqlChips__ = sqlChips
        return self
    
    def read(self):
        return Store() if self.__sqlChips__ == None else self.__sqlChips__

    def __exit__(self, exc_type, exc_value, traceback):
        return self


class ResourceFactory():
    def __init__(self):
        self.sqlParser = SqlParser()
    
    def sqlCompose(self, sqlPath=None, args=None, parseType=None, modelFnName=None, sql=None, logging=None):
        # 读取sql字符串
        sqlStr = None
        if sql==None:
            sqlChips = self.sqlLoad(sqlPath)
            if modelFnName == None:
                sqlStr = sqlChips['_default_']
            else:
                if sqlChips[modelFnName] == None:
                    sqlStr = sqlChips['_default_']
                else:
                    sqlStr = sqlChips[modelFnName]
        else:
            sqlStr = sql
        # 解析sql动作
        sqlAction = self.sqlParser.getSqlAction(sqlStr)
        # 插入的时候，可以一次插入多条数据
        if type(args) == list and (sqlAction == 'INSERT' or sqlAction == 'UPDATE'):
            transSql = self.sqlParser.multiSqlParse(sqlStr, args,logging or self.sqlParser.logging, parseType=parseType, comb=True)
            return transSql.mutiSqls , sqlAction
        else:
            singleSql = self.sqlParser.sqlParse(sqlStr, args,logging or self.sqlParser.logging, parseType=parseType)
            return [singleSql] , sqlAction



    def sqlLoad(self, sqlPath):
        sqlChips = None
        with sqlLoad(sqlPath) as res:
            sqlChips = res.read()
        return sqlChips

resf = ResourceFactory()