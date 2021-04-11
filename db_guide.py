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
            self._SqlPath_ = self.SQL_PATH
            self._ParseType_ = self.SQL_TEMPLATE_TYPE
            self._AllowRollback_ = self.ALLOW_ROLLBACK
            self._AutoCommit_ = self.AUTO_COMMIT
            self._UseBean_ = self.USE_BEAN
            # 绑定装饰器别名
            self.sql = self.__sql__
            self.conn = self.__connection__

        # sql装饰器
        def __sql__(self, *args, **kwargs):
            ''' 装饰器参数 '''
            # 应用模板类型
            _ParseType_ = self._ParseType_ if kwargs.get(
                'SQL_TEMPLATE_TYPE') == None else kwargs.get('SQL_TEMPLATE_TYPE')
            # 是否应用Bean来使用自动注入
            _UseBean_ = self._UseBean_ if kwargs.get(
                'USE_BEAN') == None else kwargs.get('USE_BEAN')
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
                self.resolvePath()
                # 初始化log
                self.initLogging()
                # 获取sql路径
                sql_path = None
                modelFnName = None
                if _SqlName_ == None:
                    sql_path = self.resolveSqlPath(
                        model_fn.__name__, self.getModelPath(model_fn))
                    modelFnName = None
                else:
                    sql_path = self.resolveSqlPathSn(_SqlName_)
                    modelFnName = model_fn.__name__

                def __model_fn(*args, **kwargs):
                    self.logging(
                        "DEBUG", "****** %s Start ******" % self.__module_name__)

                    # 生成sql语句
                    sqls,sqlAction = resf.sqlCompose(
                        sqlPath=sql_path,
                        args=model_fn(*args, **kwargs),
                        parseType=_ParseType_,
                        modelFnName=modelFnName,
                        sql=_SqlStr_,
                        logging=self.logging)

                    cur = self.execute(sqls,sqlAction)

                    # cur = self.execute(
                    #     sql_path, model_fn(*args, **kwargs), _ParseType_, model_fn.__name__)
                    
                    if(cur == None):
                        raise Exception("The 'cursor' is None", 1)
                    elif(type(cur) == list and len(cur) == 0):
                        raise Exception("The 'cursor' is None", 1)
                    else:
                        if _UseBean_:
                            return self.inject(cur, __bean__, bf.createResultClass)
                        return cur
                return __model_fn
            return _sql_

        # 链接装饰器
        def __connection__(self, *args, **kwargs):
            _AllowRollback_ = self._AllowRollback_ if kwargs.get(
                'allow_rollback') is None else kwargs.get('allow_rollback')
            _AutoCommit_ = self._AutoCommit_ if kwargs.get(
                'auto_commit') is None else kwargs.get('auto_commit')

            def _connection_(logic_fn):
                # 解析路径
                self.resolvePath()
                # 初始化log
                self.initLogging()

                def __logic_fn(*args, **kwargs):
                    self.connect(_AllowRollback_, _AutoCommit_)
                    self.logging('DEBUG', '\n'.join((f'''
                        DB_DATABASE:{self.DB_DATABASE}
                        DB_USER:{self.DB_USER}
                        DB_PASSWORD:{self.DB_PASSWORD}
                        DB_HOST:{self.DB_HOST}
                        DB_PORT:{self.DB_PORT}
                    ''').split()))
                    result = None
                    try:
                        result = logic_fn(*args, **kwargs)
                        if _AllowRollback_ and _AutoCommit_:
                            self.commit()
                    except Exception as exc:
                        if _AllowRollback_ and _AutoCommit_:
                            self.rollback()
                            self.logging("ERROR", exc)
                            self.logging("WARN", "****** SQL Rollback ******")
                            self.close()
                        raise exc
                    self.close()
                    self.logging("DEBUG", "****** %s End ******" %
                                 self.__module_name__)
                    return result
                return __logic_fn
            return _connection_

        # 主方法注解，可选注解，用于初始化
        def entry(self, main_fn):
            # 解析路径
            self.resolvePath(main_fn)
            # 主方法做为根目录解析路径
            # 初始化log
            self.initLogging()

            def __entry_fn(*args, **kwargs):
                return main_fn(*args, **kwargs)

    # 实例化数据库向导
    return Dbc(*args, **kwargs)
