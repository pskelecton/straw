#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    数据库引导层
#    SQL挂载注解、DB连接注解
# Created : 2020.10.14
# Author : Chalk Yu
# ========================================
from __future__ import absolute_import
from .frame_guide import InitGuide
from .bean_factory import bf
from .orm_factory import orm
from .resource_factory import resf
from .tool import FormatMsg
from .screws import Store

def createDbc(*args, **kwargs):
    # 采用的数据库关系映射的库
    ORM_LOADER = kwargs.get('ORM_LOADER') or 'sqlalchemy'
    # 读取关系映射的loader
    OrmLoader: type = ORM_LOADER if type(
        ORM_LOADER) == type else orm.loaderCreater(ORM_LOADER)

    class Dbc(InitGuide, OrmLoader):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__module_name__ = self.module_name
            # 绑定装饰器别名
            self.sql = self.__sql__
            self.conn = self.__connection__
            self.entry = self.__entry__
            # 初始化connection数据库连接对象
            self.connection = None

        # sql装饰器
        def __sql__(self, *args, **kwargs):
            ''' 装饰器参数 '''
            # 直接读取sql文件，不从缓存中拿去
            _HardLoadSql_ = self.HARD_LOAD_SQL if kwargs.get(
                'HARD_LOAD_SQL') == None else kwargs.get('HARD_LOAD_SQL')
            # 应用模板类型
            _ParseType_ = self.SQL_TEMPLATE_TYPE if kwargs.get(
                'SQL_TEMPLATE_TYPE') == None else kwargs.get('SQL_TEMPLATE_TYPE')
            # 是否应用Bean来使用自动注入
            _UseBean_ = self.USE_BEAN
            # 注入的Bean类，USE_BEAN=True才生效
            __bean__ = None if len(args) == 0 else args[0]
            # 直接指定sql文件
            _SqlName_ = None if kwargs.get(
                'SQL_NAME') == None else kwargs.get('SQL_NAME')
            # 直接设置sql语句
            _SqlStr_ = None if kwargs.get(
                'SQL') == None else kwargs.get('SQL')
            def _sql_(model_fn):
                # 解析路径
                # self.resolvePath(sql_on=_SqlName_==None and _SqlStr_==None)
                # 初始化log
                self.initLogging()
                # 获取sql路径
                sql_path = None
                # 设置sql段落名，优先级： SQL参数 > SQL_NAME参数 > 自动查找
                modelFnName = None
                if _SqlStr_ == None:
                    if _SqlName_ == None:
                        sql_path = self.resolveSqlPath(
                            model_fn.__name__, self.getModelPath(model_fn))
                        modelFnName = None
                    else:
                        sql_path = self.resolveSqlPathSn(_SqlName_)
                        modelFnName = model_fn.__name__
                else:
                    modelFnName = model_fn.__name__

                def __model_fn(*args, **kwargs):
                    self.logging("DEBUG", FormatMsg("%s Start" % self.__module_name__))
                    # 如果参数传SQL，直接用参数的sql语句
                    if _SqlStr_ == None:
                        if _SqlName_ == None:
                            # 每次都重新读取sql文件
                            if _HardLoadSql_:
                                _SqlStr_ = resf.sqlLoad(sql_path)
                            else:
                                # 获取缓存中的sql字符串
                                if self.cache.all_sqls_cached:
                                    _SqlStr_ = self.cache.sql_str_dict.get(sql_path)
                                else:
                                    # 重新读取文件，并写入缓存
                                    _SqlStr_ = resf.sqlLoad(sql_path)
                                    self.cache.sql_str_dict[sql_path] = _SqlStr_
                        else:
                            _SqlStr_ = resf.sqlLoad(sql_path)
                            
                    # 生成sql语句
                    sqlStr,sqlAction = resf.sqlCompose(
                        args=model_fn(*args, **kwargs),
                        parseType=_ParseType_,
                        modelFnName=modelFnName,
                        sql=_SqlStr_,
                        logging=self.logging)
                    
                    cursor = None
                    if self.RW_EXECUTE:
                        cursor = self.RW_EXECUTE(self.connection,sqlStr,sqlAction)
                    else:
                        cursor = self.execute(self.connection,sqlStr,sqlAction)
                    
                    if _UseBean_:
                        if __bean__ == None:
                            return cursor
                        else:
                            if self.RW_INJECT:
                                return self.RW_INJECT(self.connection,sqlAction,cursor, __bean__, bf.createResultClass)
                            else:
                                return self.inject(self.connection,sqlAction,cursor, __bean__, bf.createResultClass)
                    else:
                        return cursor
                return __model_fn
            return _sql_

        # 链接装饰器
        def __connection__(self, *args, **kwargs):
            # 接受缓存数据库的model_name
            _db_model_name_ = None if len(args) == 0 else args[0]
            #
            _AllowRollback_ = self.ALLOW_ROLLBACK if kwargs.get(
                'ALLOW_ROLLBACK') is None else kwargs.get('ALLOW_ROLLBACK')
            _AutoCommit_ = self.AUTO_COMMIT if kwargs.get(
                'AUTO_COMMIT') is None else kwargs.get('AUTO_COMMIT')
            def _connection_(logic_fn):
                # 解析路径
                # self.resolvePath()
                # 初始化log
                self.initLogging()
                #
                def __logic_fn(*args, **kwargs):
                    # 校验缓存的数据库连接
                    if self.CACHE_CONNECT and self.conn_cache.get(_db_model_name_) == None:
                            raise Exception(FormatMsg("%s >> %s >> End" % (_db_model_name_,'@conn can`t get db connection.')))
                    #
                    if self.CACHE_CONNECT:
                        _AllowRollback_ = self.getAccessInfo(_db_model_name_).get('ALLOW_ROLLBACK') or self.ALLOW_ROLLBACK
                        _AutoCommit_ = self.getAccessInfo(_db_model_name_).get('AUTO_COMMIT') or self.AUTO_COMMIT
                        # 获取连接
                        self.connection = self.conn_cache.get(_db_model_name_)
                    else:
                        dbConf = Store({
                            'DB_DRIVER':self.DB_DRIVER,
                            'DB_USER':self.DB_USER,
                            'DB_PASSWORD':self.DB_PASSWORD,
                            'DB_HOST':self.DB_HOST,
                            'DB_PORT':self.DB_PORT,
                            'DB_DATABASE':self.DB_DATABASE,
                            'ENCODING':self.ENCODING,
                            'ALLOW_ROLLBACK':_AllowRollback_,
                            'AUTO_COMMIT':_AutoCommit_,
                            'SQLALCHEMY_ARGS':self.SQLALCHEMY_ARGS
                        })
                        if self.RW_CONNECT:
                            self.connection = self.RW_CONNECT(dbConf=dbConf)
                        else:
                            self.connection = self.connect(dbConf=dbConf)

                    self.logging('DEBUG',FormatMsg('DB Connection','\n'.join((f'''
                        DB_DATABASE:{self.DB_DATABASE}
                        DB_USER:{self.DB_USER}
                        DB_PASSWORD:{self.DB_PASSWORD}
                        DB_HOST:{self.DB_HOST}
                        DB_PORT:{self.DB_PORT}
                    ''').split())))
                    result = None
                    try:
                        result = logic_fn(*args, **kwargs)
                        if _AllowRollback_ and _AutoCommit_:
                            if self.RW_COMMIT:
                                self.RW_COMMIT(self.connection)
                            else:
                                self.commit(self.connection)
                    except Exception as exc:
                        if _AllowRollback_ and _AutoCommit_:
                            if self.RW_ROLLBACK:
                                self.RW_ROLLBACK(self.connection)
                            else:
                                self.rollback(self.connection)
                            self.logging("ERROR", exc)
                            self.logging("WARN", FormatMsg("SQL Rollback"))
                            # 如果保持连接状态，数据库不关闭
                            if self.CACHE_CONNECT:
                                pass
                            else:
                                if self.RW_CLOSE:
                                    self.RW_CLOSE(self.connection)
                                else:
                                    self.close(self.connection)
                        raise exc
                    # 如果保持连接状态，数据库不关闭
                    if self.CACHE_CONNECT:
                        pass
                    else:
                        if self.RW_CLOSE:
                            self.RW_CLOSE(self.connection)
                        else:
                            self.close(self.connection)
                    self.logging("DEBUG", FormatMsg("%s End" % self.__module_name__))
                    return result
                return __logic_fn
            return _connection_

        # 主方法注解，可选注解，用于初始化
        def __entry__(self, *args, **kwargs):
            # @entry注解计数器
            self.cache.modify('entry_cnt', self.cache.entry_cnt + 1)
            if self.cache.entry_cnt > 1:
                raise Exception(FormatMsg("%s >> %s >> End" % (self.__module_name__,'@entry annotation must be unique.')))
            # 解析sql,log,env文件夹路径
            # self.resolvePath()
            # 向导生成文件夹以及文件结构
            _StartGuide_ = kwargs.get('START_GUIDE')
            if _StartGuide_:
                self.runGuide()
            
            # 全局 HARD_LOAD_SQL 生效
            if not self.HARD_LOAD_SQL:
                # 是否缓存所有sqls数据
                _CacheSqls_ = kwargs.get('CACHE_SQLS')
                if _CacheSqls_ == True:
                    self.cacheSqlFiles()
                
            # 初始化log
            self.initLogging()

            # 缓存数据库连接
            if self.CACHE_CONNECT:
                self.cacheDbConn()

            def _entry_(logic_fn):
                # 解析路径
                # self.resolvePath()
                # 主方法做为根目录解析路径
                # 初始化log
                self.initLogging()

                def __entry_fn(*args, **kwargs):
                    return logic_fn(*args, **kwargs)
                return __entry_fn
            return _entry_

    # 实例化数据库向导
    return Dbc(*args, **kwargs)
