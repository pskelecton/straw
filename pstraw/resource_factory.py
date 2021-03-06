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
from .template_factory import templatePaser  # 模板转换器

# 根据外部传入的转换器，解析sql字符串，如果未传转换器，则直接读取sql字符串


class sqlLoad():
    def __init__(self, sqlPath, transFunc=None):
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
        return self.__sqlChips__

    def __exit__(self, exc_type, exc_value, traceback):
        return self


class ResourceFactory():
    def __init__(self):
        # sql转换器
        self.sqlParser = SqlParser()

    def sqlCompose(self, args=None, parseType=None, modelFnName=None, sql=None, logging=None, parserOptions={}):
        if logging == None:
            logging = self.sqlParser.logging
        # 读取sql字符串
        sqlStr = None
        sqlChips = templatePaser.Model(sql)
        if modelFnName == None:
            sqlStr = sql
        else:
            if sqlChips[modelFnName] == None:
                sqlStr = sql
            else:
                sqlStr = sqlChips[modelFnName]
        # 解析sql动作
        sqlAction = self.sqlParser.getSqlAction(sqlStr)
        # 插入的时候，可以一次插入多条数据
        if type(args) == list:
            if sqlAction == 'INSERT' or sqlAction == 'UPDATE' or sqlAction == 'DELETE':
                sqlStore = self.sqlParser.multiSqlParse(
                    sqlStr, args, logging, parseType=parseType, options=parserOptions)
                return sqlStore.transSqls, sqlAction
            else:
                errMsg = FormatMsg(
                    "When the '@sql' annotation function returns the list type, the sql statement must be a simple 'insert' or 'update' or 'delete'")
                logging('ERROR', errMsg)
                raise Exception(errMsg)
        else:
            singleSql = self.sqlParser.sqlParse(
                sqlStr, args, logging, parseType=parseType,quotation=parserOptions.get('quotation'))
            return singleSql, sqlAction

    def sqlLoad(self, sqlPath):
        sqlStr = None
        with sqlLoad(sqlPath) as res:
            sqlStr = res.read()
        return sqlStr


resf = ResourceFactory()
