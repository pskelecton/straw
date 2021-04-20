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
from ..screws import Store


class loader(OrmLoader, SqlParser):
    def __init__(self):
        super().__init__()

    def connect(self, dbConf=None):
        dbAccess = Store({
            'DB_DRIVER':self.DB_DRIVER,
            'DB_USER':self.DB_USER,
            'DB_PASSWORD':self.DB_PASSWORD,
            'DB_HOST':self.DB_HOST,
            'DB_PORT':self.DB_PORT,
            'DB_DATABASE':self.DB_DATABASE,
            'ENCODING':self.ENCODING,
            'ALLOW_ROLLBACK':self.ALLOW_ROLLBACK,
            'AUTO_COMMIT':self.AUTO_COMMIT,
            'SQLALCHEMY_ARGS':self.SQLALCHEMY_ARGS
        })
        if dbConf != None:
            dbAccess = dbConf

        conn_str = ''
        if dbAccess.DB_DRIVER == "postgres":
            conn_str = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (
                dbAccess.DB_USER, dbAccess.DB_PASSWORD, dbAccess.DB_HOST, dbAccess.DB_PORT, dbAccess.DB_DATABASE)
        elif dbAccess.DB_DRIVER == "mysql":
            conn_str = 'mysql+pymysql://%s:%s@%s:%s/%s' %(
                dbAccess.DB_USER,dbAccess.DB_PASSWORD,dbAccess.DB_HOST,dbAccess.DB_PORT,dbAccess.DB_DATABASE)
        elif dbAccess.DB_DRIVER == "oracle":
            conn_str = 'oracle+cx_oracle://%s:%s@%s:%s/%s' %(
                dbAccess.DB_USER,dbAccess.DB_PASSWORD,dbAccess.DB_HOST,dbAccess.DB_PORT,dbAccess.DB_DATABASE)
        elif dbAccess.DB_DRIVER == "mssql":
            conn_str = 'mssql+pymssql://%s:%s@%s:%s/%s' %(
                dbAccess.DB_USER,dbAccess.DB_PASSWORD,dbAccess.DB_HOST,dbAccess.DB_PORT,dbAccess.DB_DATABASE)
        elif dbAccess.DB_DRIVER == "sqlite":
            conn_str = 'sqlite:///%s' %dbAccess.SQLITE_PATH
        else:
            raise Exception(formatMsg("DB Driver must be one of postgres/mysql."))
        # 连接数据库
        if conn_str != '':
            # sqlalchemy扩展参数
            engine = None
            if dbAccess.SQLALCHEMY_ARGS and type(dbAccess.SQLALCHEMY_ARGS.create_engine) == dict:
                if dbAccess.SQLALCHEMY_ARGS.create_engine['poolclass'] == None:
                    dbAccess.SQLALCHEMY_ARGS.create_engine['poolclass'] = NullPool
                if dbAccess.SQLALCHEMY_ARGS.create_engine['encoding'] == None:
                    dbAccess.SQLALCHEMY_ARGS.create_engine['encoding'] = dbAccess.ENCODING
                engine = create_engine(conn_str, **dbAccess.SQLALCHEMY_ARGS.create_engine)
            else:
                engine = create_engine(conn_str, poolclass=NullPool,encoding=dbAccess.ENCODING)
            #
            sessionFacory = None
            if dbAccess.SQLALCHEMY_ARGS and  type(dbAccess.SQLALCHEMY_ARGS.sessionFacory) == dict:
                if dbAccess.SQLALCHEMY_ARGS.sessionFacory['autoflush'] == None:
                    dbAccess.SQLALCHEMY_ARGS.sessionFacory['autoflush'] = True
                sessionFacory = sessionmaker(bind=engine, **dbAccess.SQLALCHEMY_ARGS.sessionFacory)
            else:
                sessionFacory = sessionmaker(bind=engine, autoflush=True)
            #
            __connection__ = None
            if dbAccess.SQLALCHEMY_ARGS and  type(dbAccess.SQLALCHEMY_ARGS.scoped_session) == dict:
                __connection__ = scoped_session(sessionFacory, **dbAccess.SQLALCHEMY_ARGS.scoped_session)
            else:
                __connection__ = scoped_session(sessionFacory)
            #
            return __connection__

    def execute(self,conn, sqls, sqlAction):
        # self._SqlAction_ = sqlAction
        try:
            # cursor数组
            curs = []
            for sql in sqls:
                cur = conn.execute(sql)
                curs.append(cur)
                self.logging("DEBUG", formatMsg("SQL execute success."))
            return curs
        except Exception as exc:
            self.logging("ERROR", formatMsg("SQL execute error."))
            raise Exception("%s: %s" %(exc.__class__.__name__, exc))

    def close(self,conn):
        conn.close()

    def commit(self,conn):
        conn.commit()

    def rollback(self,conn):
        conn.rollback()

    def inject(self,conn,sqlAction, curs, bean, resultCreater):
        if sqlAction == 'SELECT':
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
        elif sqlAction == 'INSERT':
            res = resultCreater()(cursor=curs, count=None)
            rowcount = 0
            for cur in curs:
                rowcount += cur.rowcount
            res.count = rowcount
            return res
        elif sqlAction == 'UPDATE':
            res = resultCreater()(cursor=curs, count=None)
            rowcount = 0
            for cur in curs:
                rowcount += cur.rowcount
            res.count = rowcount
            return res
        elif sqlAction == 'DELETE':
            res = resultCreater()(cursor=curs, count=None)
            rowcount = 0
            for cur in curs:
                rowcount += cur.rowcount
            res.count = rowcount
            return res
        elif sqlAction == 'TRUNCATE':
            res = resultCreater()(cursor=curs, count=None)
            return res
        else:
            raise Exception(formatMsg(f'SQL action \[{sqlAction}\] is not in \[SELECT,INSERT,UPDATE,DELETE,TRUNCATE\]'))
