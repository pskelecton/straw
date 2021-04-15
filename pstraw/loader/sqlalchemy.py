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
from ..tool import formatMsg


class loader(OrmLoader, SqlParser):
    def __init__(self):
        super().__init__()

    def connect(self, allowRollback=None, autoCommit=None):
        conn_str = ''
        if self.DB_DRIVER == "postgres":
            conn_str = 'postgresql://%s:%s@%s:%s/%s' % (
                self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_DATABASE)
        elif self.DB_DRIVER == "mysql":
            conn_str = 'mysql+pymysql://%s:%s@%s:%s/%s' %(
                self.DB_USER,self.DB_PASSWORD,self.DB_HOST,self.DB_PORT,self.DB_DATABASE)
        # elif self.DB_DRIVER == "sqlite":
        #     pass
        # elif self.DB_DRIVER == "oracle":
        #     pass
        else:
            raise Exception(formatMsg("DB Driver must be one of postgres/mysql."))
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
                self.logging("DEBUG", formatMsg("SQL execute success."))
            return curs
        except Exception as exc:
            self.logging("ERROR", formatMsg("SQL execute error."))
            # self.logging("ERROR", "%s: %s" %(exc.__class__.__name__, exc))
            # raise
            raise Exception("%s: %s" %(exc.__class__.__name__, exc))

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
            raise Exception(formatMsg(f'SQL action \[{self._SqlAction_}\] is not in \[SELECT,INSERT,UPDATE,DELETE,TRUNCATE\]'))
