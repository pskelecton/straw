#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    资源工厂
#    用于读取和解析sql文件资源
# Created : 2020.10.14
# Author : Chalk Yu
# ========================================
from promise import Promise
from .screws import Store
from .loader import SqlParser
from types import MethodType, FunctionType
from .tool import FormatMsg

# 根据外部传入的转换器，解析sql字符串，如果未传转换器，则直接读取sql字符串
class sqlLoad():
    def __init__(self, sqlPath, transFunc = None):
        self.sqlPath = sqlPath
        self.__sqlChips__ = None
        # sql转换方法
        self.transFunc = transFunc

    def __enter__(self):
        with open(self.sqlPath, "r", encoding='utf-8') as fs_sql:
            sql = fs_sql.read()
            if type(self.transFunc) == FunctionType:
                self.__sqlChips__ = self.transFunc(sql)
            else:
                self.__sqlChips__ = sql
        return self
    
    def read(self):
        return  self.__sqlChips__

    def __exit__(self, exc_type, exc_value, traceback):
        return self


class ResourceFactory():
    def __init__(self):
        self.sqlParser = SqlParser()
    
    def sqlCompose(self, args=None, parseType=None, modelFnName=None, sql=None, logging=None):
        if logging == None:
            logging = self.sqlParser.logging
        # 读取sql字符串
        sqlStr = None
        sqlChips = self.sqlTrans(sql)
        if modelFnName == None:
            sqlStr = sqlChips._default_
        else:
            if sqlChips[modelFnName] == None:
                sqlStr = sqlChips._default_
            else:
                sqlStr = sqlChips[modelFnName]
        # 解析sql动作
        sqlAction = self.sqlParser.getSqlAction(sqlStr)
        # 插入的时候，可以一次插入多条数据
        if type(args) == list:
            if sqlAction == 'INSERT' or sqlAction == 'UPDATE' or sqlAction == 'DELETE':
                sqlStore = self.sqlParser.multiSqlParse(sqlStr, args,logging, parseType=parseType)
                return sqlStore.transSqls , sqlAction
            else:
                errMsg = FormatMsg("When the '@sql' annotation function returns the list type, the sql statement must be a simple 'insert' or 'update' or 'delete'")
                self.sqlParser.logging('ERROR',errMsg)
                raise Exception(errMsg)
        else:
            singleSql = self.sqlParser.sqlParse(sqlStr, args,logging or self.sqlParser.logging, parseType=parseType)
            return singleSql , sqlAction

    def sqlLoad(self, sqlPath):
        sqlStr = None
        with sqlLoad(sqlPath) as res:
            sqlStr = res.read()
        return sqlStr
    
    # sql模板转换方法
    @classmethod
    def sqlTrans(cls,sqlStr):
        sqlChips = Store()
        sqlChips._default_ = sqlStr
        tmpModuleFnName = None
        sqlLines = sqlStr.split('\n')
        for sqlLine in sqlLines:
            if sqlLine.strip()[:2]=='@@':
                tmpModuleFnName = sqlLine.strip()[2:]
                sqlChips[tmpModuleFnName] = ""
            else:
                if tmpModuleFnName != None:
                    sqlChips[tmpModuleFnName] = sqlChips[tmpModuleFnName] + '\n' + sqlLine
        return sqlChips

resf = ResourceFactory()