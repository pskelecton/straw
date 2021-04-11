#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    兼容多数据库 Loader
# Created : 2020.10.22
# Author : Chalk Yu
# ========================================
from __future__ import absolute_import
from .extends import SqlParser, OrmLoader
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool


class loader(OrmLoader, SqlParser):
    def __init__(self):
        super().__init__()

    def connect(self, allowRollback=None, autoCommit=None):
        conn_str = ''
        if self.DB_DRIVER == "postgres":
            conn_str = 'postgresql://%s:%s@%s:%s/%s' % (
                self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_DATABASE)
        elif self.DB_DRIVER == "db2":
            pass
        elif self.DB_DRIVER == "mysql":
            conn_str = 'mysql+pymysql://%s:%s@%s:%s/%s' %(
                self.DB_USER,self.DB_PASSWORD,self.DB_HOST,self.DB_PORT,self.DB_DATABASE)
        elif self.DB_DRIVER == "sqlite":
            pass
        elif self.DB_DRIVER == "oracle":
            pass
        else:
            raise Exception(
                f'******* DB Driver \[{self.DB_DRIVER}\] is not in \[postgres,db2,mysql,sqlite,oracle\] *******')
        # 连接数据库
        if conn_str != '':
            engine = create_engine(conn_str, poolclass=NullPool)
            sessionFacory = sessionmaker(bind=engine, autoflush=True)
            self.conn = scoped_session(sessionFacory)

    def execute(self, sqls, sqlAction):
        self._SqlAction_ = sqlAction
        try:
            # cursor组
            curs = []
            for sql in sqls:
                cur = self.conn.execute(sql)
                curs.append(cur)
                self.logging("DEBUG", f'****** SQL loading success ******')
            return curs
        except Exception as exc:
            self.logging("ERROR", "****** SQL loading error ******")
            self.logging("ERROR", "%s: %s" %
                         (exc.__class__.__name__, exc))
            raise

    # def execute(self, sql_path, args, parseType, modelFnName):
    #     try:
    #         cur = None
    #         with open(sql_path, "r", encoding='utf-8') as fs_sql:
    #             sql = fs_sql.read()
    #             self._SqlAction_ = self.getSqlAction(sql)
    #             # cursor组
    #             curs = []
    #             # 插入的时候，可以一次插入多条数据
    #             if type(args) == list and self._SqlAction_ == 'INSERT':
    #                 transSql = self.multiSqlParse(
    #                     sql, args, self.logging, parseType=parseType, comb=True)
    #                 for sql in transSql.mutiSqls:
    #                     cur = self.conn.execute(sql)
    #                     curs.append(cur)
    #             else:
    #                 sql = self.sqlParse(
    #                     sql, args, self.logging, parseType=parseType)
    #                 cur = self.conn.execute(sql)
    #                 curs.append(cur)
    #             self.logging("DEBUG", f'****** SQL loading success ******')
    #         return curs
    #     except Exception as exc:
    #         self.logging("ERROR", "****** SQL loading error ******")
    #         self.logging("ERROR", "%s: %s" %
    #                      (exc.__class__.__name__, exc))
    #         raise

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def inject(self, curs, bean, resultCreater):
        if resultCreater == None:
            return curs
        if self._SqlAction_ == 'SELECT':
            if type(bean) == type:
                res = resultCreater(list)(cursor=curs, count=None)
                rowcount = 0
                for cur in curs:
                    for record in cur:
                        res.append(bean(*record))
                    rowcount += cur.rowcount
                res.count = rowcount
            else:
                return curs
            return res
        elif self._SqlAction_ == 'INSERT':
            res = resultCreater()(cursor=curs, count=None)
            rowcount = 0
            for cur in curs:
                rowcount += cur.rowcount
            res.count = rowcount
            return res
        elif self._SqlAction_ == 'UPDATE':
            res = resultCreater()(cursor=curs, count=None)
            rowcount = 0
            for cur in curs:
                rowcount += cur.rowcount
            res.count = rowcount
            return res
        elif self._SqlAction_ == 'DELETE':
            res = resultCreater()(cursor=curs, count=None)
            rowcount = 0
            for cur in curs:
                rowcount += cur.rowcount
            res.count = rowcount
            return res
        elif self._SqlAction_ == 'TRUNCATE':
            res = resultCreater()(cursor=curs, count=None)
            return res
        else:
            raise Exception(
                f'******* SQL action \[{_sms[0]}\] is not in \[SELECT,INSERT,UPDATE,DELETE\] *******')
