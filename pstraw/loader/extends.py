#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    ORM Loader 扩展模块
# Created : 2020.10.22
# Author : Chalk Yu
# ========================================
from __future__ import absolute_import
import sqlparse
import re
import math
from ..screws import Store
from ..tool import formatMsg


# ORM Loader接口
class OrmLoader():

    def __init__(self):
        super().__init__()

    def logging(self, type, message):
        print(type, message)

    '''
        数据库连接：
        参数：
            [allow_rollback] : default = False
            [auto_commit] : default = True
        传入方式：
            @[dbc].connection([allow_rollback],[auto_commit])
    '''

    def connect(self,dbConf=None):
        return None

    '''
        sql执行：
        参数：
            [allow_rollback] : default = False
            [auto_commit] : default = True
        传入方式：
            @[dbc].connection([allow_rollback],[auto_commit])
    '''

    # def execute(self, sql_path, args, parseType, modelFnName):
    #     pass

    def execute(self, sqls, sqlAction=None):
        return [None]

    def close(self):
        return None

    def commit(self):
        return None

    def rollback(self):
        return None

    def inject(self, curs, bean, resultCreater):
        return None


# SQL转换类
class SqlParser():
    def __init__(self):
        super().__init__()

    # logging检测
    #   @args：
    #      [logging] : logging
    #   @return：logging
    def logger(self, logging):
        if(logging is None):
            return print
        else:
            return logging

    # sql格式化
    #   @args：
    #      [sql] : str(sql)
    #      [loc] : index of sql, when there are multi-sqls in str(sql)
    #   @return：str(sql)
    def formatSql(self, sql, loc=0):
        format_sql = sqlparse.format(
            sql, reindent=True, keyword_case='upper', strip_comments=True, reindent_aligned=False)
        parsed = sqlparse.parse(format_sql)
        stmt = parsed[loc]
        sql = str(stmt)
        return sql

    # list替换
    #   @args：
    #      [sourceList] : sourceList
    #      [oldVal] : search value
    #      [newVal] : replace value
    #   @return：targetList
    def listReplace(self, sourceList, oldVal, newVal):
        targetList = []
        for item in sourceList:
            if item.strip() == oldVal.strip():
                targetList.append(newVal)
            else:
                targetList.append(item)
        return targetList

    # list拆分（不均匀拆分）
    def listSplit(self, sourceList, maxSize):
        targetList = []
        subList = []
        loc = 0
        for item in sourceList:
            # 子集长度累加
            loc = loc + len(item)
            # 累加后的子集长度如果小于最大长度则添加
            if loc < maxSize:
                subList.append(item)
            # 累加后的子集长度如果大于最大长度则执行下一轮
            else:
                targetList.append(subList)
                # 初始化子集
                subList = []
                # 当前元素添加到新子集中
                subList.append(item)
                # 重新计算新子集长度
                loc = len(item)
        # 总长度都没超过maxSize
        if len(targetList) == 0:
            targetList.append(subList)
        #
        return targetList

    # sql碎片化
    #   @args：
    #      [sql] : str(sql)
    #      [loc] : index of sql, when there are multi-sqls in str(sql)
    #   @return：list[sql]

    def sqlChipMaker(self, sql, loc=0):
        sqlFragments = []

        def deepenSqlChip(stmt):
            # root
            if hasattr(stmt, "tokens"):
                for tok in stmt.tokens:
                    deepenSqlChip(tok)
            else:
                # leaf
                seg = str(stmt)
                if seg.strip() != "":
                    sqlFragments.append(seg)
                return

        format_sql = sqlparse.format(
            sql, reindent=True, keyword_case='upper', strip_comments=True, reindent_aligned=False)
        parsed = sqlparse.parse(format_sql)
        sql_stmt = parsed[loc]
        deepenSqlChip(sql_stmt)
        return sqlFragments

    # 获取sql动作
    #   @args：
    #      [sql] : str(sql)
    #      [loc] : index of sql, when there are multi-sqls in str(sql)
    #   @return：INSERT|SELECT|UPDATE|DELETE
    def getSqlAction(self, sql, loc=0):
        sqlSegs = self.sqlChipMaker(sql, loc)
        return sqlSegs[0].upper()

    # 合并sql字符串
    def multiSqlParse(self, base_sql, args_list, logging, parseType, maxSize=1024*512, combType=None):
        sqlCache = []
        transSqls = ''
        transLen = 0
        #
        for args in args_list:
            transSql = self.sqlParse(
                base_sql, args, logging, parseType=parseType)
            # 通过正则去掉首尾的分号 ;
            pattern = re.compile(r'(^;*)|(;*$)', re.M)
            transSql = re.sub(pattern, '', transSql)
            # 为每个sql语句添加分号
            transSql = f'{transSql};'
            # 缓存sql
            sqlCache.append(transSql)
            # 合并sql
            if combType=='INSERT':
                '''
                    # 只适用 insert into ??? values ??? 语句
                '''
                # 分解sql
                sqlSegs = self.sqlChipMaker(transSql, 0)
                # values后面的部分
                sqlValuesStr = ''.join(sqlSegs[sqlSegs.index('VALUES')+1:])
                # 长度累加
                if transLen == 0:
                    transLen = len(transSql)
                else:
                    transLen += len(sqlValuesStr)
                if transLen < maxSize:
                    if transSqls == '':
                        transSqls = transSql
                    else:
                        # 截取VALUES后面的值，并且去分号，与前一个sql去分号合并添加逗号
                        transSqls = transSqls[:-1] + ',' + sqlValuesStr
            elif combType=='UPDATE':
                pass
            elif combType=='DELETE':
                pass
            elif combType=='SELECT':
                pass
            elif combType=='TRUNCATE':
                pass
            elif combType==None:
                '''
                    # 直接合并sql语句，泛用各类sql语句，包括嵌套、表关联、子查询等等
                '''
                transLen += len(transSql)
                if transLen < maxSize:
                    transSqls += transSql

        return Store({
            'sqls': sqlCache,
            'transSqls': transSqls,  # 字符串连接后的sql字符串
        })

    # sql模板参数转换
    #   @args：
    #      [sql] : str(sql)
    #      [tuple_args|dict_args] :
    #      [parseType] : 1 | 2 | 3 | 4 | 5 | 6
    #           parseType == 1: (default parse , no parse engine)
    #               sql : %s %s %s        ==>   model : (p1, p2, p3)
    #           parseType == 2: (StrParseEngine)
    #               sql : {0} {1} {0} {2} ==>   model : (p1, p2, p3)
    #                   {0} = p1 , {1} = p2 , {2} = p3
    #           parseType == 3: (DictParseEngine)
    #               sql :  col1=:c1, col2=:c2  ==>   model : {'c1':p1, 'c2':p2}
    #   @return：str(sql)
    # 注意： parseType = 4 | 5 | 6 转换方式同 1 | 2 | 3 , 只是对于非数值类型的值自动补充双引号

    def sqlParse(self, *args, parseType):
        if parseType == 1:
            return self.TempParseEngine(*args)
        elif parseType == 2:
            return self.StrParseEngine(*args)
        elif parseType == 3:
            return self.DictParseEngine(*args)
        elif parseType == 4:
            return self.TempParseEngineT(*args)
        elif parseType == 5:
            return self.StrParseEngineT(*args)
        elif parseType == 6:
            return self.DictParseEngineT(*args)
        else:
            return self.__DictParseEngine(*args)

    def TempParseEngine(self, sql, tuple_args, logging):
        sqlSegments = sql.split('\n')
        for segIdx in range(len(sqlSegments)):
            commentIdx = sqlSegments[segIdx].find('--')
            if commentIdx >= 0:
                sqlSegments[segIdx] = sqlSegments[segIdx].replace(
                    sqlSegments[segIdx][commentIdx:], "")
        sql = ' '.join(sqlSegments)
        logging("DEBUG",formatMsg('SQL',{sql}))
        sql = sql % tuple(map(lambda v: str(v), tuple_args))
        _sql_ = sql.strip()
        logging("DEBUG",formatMsg('SQL',{_sql_}))
        return _sql_

    def StrParseEngine(self, sql, tuple_args, logging):
        sqlSegments = sql.split('\n')
        for segIdx in range(len(sqlSegments)):
            commentIdx = sqlSegments[segIdx].find('--')
            if commentIdx >= 0:
                sqlSegments[segIdx] = sqlSegments[segIdx].replace(
                    sqlSegments[segIdx][commentIdx:], "")
        sql = ' '.join(sqlSegments)
        logging("DEBUG",formatMsg('SQL',{sql}))
        sql = sql.format(*tuple(map(lambda v: str(v), tuple_args)))
        _sql_ = sql.strip()
        logging("DEBUG",formatMsg('SQL',{_sql_}))
        return _sql_

    def DictParseEngine(self, sql, dict_args, logging):
        sql = self.formatSql(sql)
        logging("DEBUG",formatMsg('SQL',{sql}))
        sqlFragments = self.sqlChipMaker(sql)
        for key in dict_args:
            sqlFragments = self.listReplace(
                sqlFragments, f':{key}', str(dict_args[key]))
        sql = self.formatSql(' '.join(sqlFragments))
        _sql_ = sql.strip()
        logging("DEBUG",formatMsg('SQL',{_sql_}))
        return _sql_

    def TempParseEngineT(self, sql, tuple_args, logging):
        sqlSegments = sql.split('\n')
        for segIdx in range(len(sqlSegments)):
            commentIdx = sqlSegments[segIdx].find('--')
            if commentIdx >= 0:
                sqlSegments[segIdx] = sqlSegments[segIdx].replace(
                    sqlSegments[segIdx][commentIdx:], "")
        sql = ' '.join(sqlSegments)
        logging("DEBUG",formatMsg('SQL',{sql}))
        sql = sql % tuple(map(lambda v: str(v) if type(v)==int or type(v)==float else f'\'{str(v)}\'', tuple_args))
        _sql_ = sql.strip()
        logging("DEBUG",formatMsg('SQL',{_sql_}))
        return _sql_

    def StrParseEngineT(self, sql, tuple_args, logging):
        sqlSegments = sql.split('\n')
        for segIdx in range(len(sqlSegments)):
            commentIdx = sqlSegments[segIdx].find('--')
            if commentIdx >= 0:
                sqlSegments[segIdx] = sqlSegments[segIdx].replace(
                    sqlSegments[segIdx][commentIdx:], "")
        sql = ' '.join(sqlSegments)
        logging("DEBUG",formatMsg('SQL',{sql}))
        sql = sql.format(*tuple(map(lambda v: str(v) if type(v)==int or type(v)==float else f'\'{str(v)}\'', tuple_args)))
        _sql_ = sql.strip()
        logging("DEBUG",formatMsg('SQL',{_sql_}))
        return _sql_

    def DictParseEngineT(self, sql, dict_args, logging):
        sql = self.formatSql(sql)
        logging("DEBUG",formatMsg('SQL',{sql}))
        sqlFragments = self.sqlChipMaker(sql)
        for key in dict_args:
            sqlFragments = self.listReplace(
                sqlFragments, f':{key}', str(dict_args[key]) if type(dict_args[key])==int or type(dict_args[key])==float else f'\'{str(dict_args[key])}\'')
        sql = self.formatSql(' '.join(sqlFragments))
        _sql_ = sql.strip()
        logging("DEBUG",formatMsg('SQL',{_sql_}))
        return _sql_
