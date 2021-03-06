#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    框架引导层
#    全局参数定义、配置参数定义、默认参数生成、路径参数生成
# Created : 2020.10.14
# Author : Chalk Yu
# ========================================
from __future__ import absolute_import
from types import MethodType, FunctionType
import sys
import os
import inspect
import traceback
import configparser
import logging
import logging.handlers
from dataclasses import dataclass
from .screws import PathPlant, Store, ConfStore
from .tool import Str2Bool, Str2Int, VarGet, FormatMsg
from .definition import __cache__
from .logger_factory import LoggerFactory


# conf文件获取初始化参数
class ConfArgs():
    def __init__(self, *args, **kwargs):
        # 初始化配置
        self.__configparser__ = configparser.ConfigParser()

        # 使用多环境切换
        self.__ENV_ON = kwargs.get("ENV_ON") or __cache__.env_on
        # 环境类型，用于多个环境切换
        self.__ENV_TYPE = kwargs.get("ENV_TYPE") or __cache__.env_type
        # 配置文件夹
        self.__ENV_DIR = PathPlant.transAbspath(
            kwargs.get('ENV_DIR') or __cache__.env_dir)
        if self.__ENV_ON:
            self.__CONF_PATH = os.path.join(
                self.__ENV_DIR, f'{self.__ENV_TYPE}.ini')
        else:
            # 配置文件路径
            self.__CONF_PATH = PathPlant.transAbspath(
                kwargs.get('CONF_PATH') or None)
        # 读取配置
        self.loadConf()

    def loadConf(self):
        if self.__CONF_PATH != None:
            self.__configparser__.read(self.__CONF_PATH, encoding="utf-8")
        return self.__configparser__

    def getArg(self, arg, namespace=__cache__.model_name):
        sec = self.__configparser__._sections
        if self.__configparser__.has_section(namespace):
            conf = sec.get(namespace)
            return conf.get(arg.lower())
        else:
            return None

    def getArgs(self, namespace=__cache__.model_name):
        sec = self.__configparser__._sections
        if self.__configparser__.has_section(namespace):
            args = sec.get(namespace)
            if args:
                return dict(args)
            else:
                return {}
        else:
            return {}

    def getArgsBySuffix(self, suffix, arg):
        namespace = f'{__cache__.conf_section_prefix}_{suffix}'
        return self.getArg(arg, namespace=namespace)

    def getSections(self, prefix=None):
        sec = self.__configparser__._sections
        secList = list(sec.keys())
        if prefix == None:
            return secList
        else:
            return list(filter(lambda x: (f'{prefix}_' in x) and x.index(f'{prefix}_') == 0, secList))

    # 配置文件夹
    @property
    def ENV_DIR(self):
        return self.__ENV_DIR

    @ENV_DIR.setter
    def ENV_DIR(self, value):
        self.__ENV_DIR = PathPlant.transAbspath(value)
        # pass  # 读写属性

    # 环境类型，用于多个环境切换
    @property
    def ENV_TYPE(self):
        return self.__ENV_TYPE

    @ENV_TYPE.setter
    def ENV_TYPE(self, value):
        self.__ENV_TYPE = value
        # pass  # 只读属性

    # 使用多环境切换
    @property
    def ENV_ON(self):
        return self.__ENV_ON

    @ENV_ON.setter
    def ENV_ON(self, value):
        self.__ENV_ON = value
        # pass  # 只读属性

# 初始化参数


class GuideArgs(ConfArgs):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print("GuideArgs", kwargs)
        # 创建参数字典
        self.__Args__ = dict()
        # SQL文件存放目录
        self.__Args__['SQL_PATH'] = PathPlant.transAbspath(kwargs.get(
            'SQL_PATH') or self.getArg('SQL_PATH') or None)
        # LOG文件存放目录
        self.__Args__['LOG_PATH'] = PathPlant.transAbspath(kwargs.get(
            'LOG_PATH') or self.getArg('LOG_PATH') or None)
        # 是否输出日志文件
        self.__Args__['LOG_ON'] = VarGet(kwargs.get(
            'LOG_ON'), self.getArg('LOG_ON'), __cache__.log_on)
        # 是否开启控制台
        self.__Args__['CONSOLE_ON'] = VarGet(kwargs.get(
            'CONSOLE_ON'), self.getArg('CONSOLE_ON'), __cache__.console_on)
        # 是否是debug模式
        self.__Args__['DEBUG'] = VarGet(kwargs.get(
            'DEBUG'), self.getArg('DEBUG'), __cache__.debug)
        self.__Args__['DEBUG'] = Str2Bool(self.__Args__['DEBUG'])
        # 单个日志文件最大容量(mb)
        self.__Args__['LOG_MAX_SIZE'] = VarGet(kwargs.get(
            'LOG_MAX_SIZE'), self.getArg('LOG_MAX_SIZE'), __cache__.log_max_size)
        self.__Args__['LOG_MAX_SIZE'] = Str2Int(self.__Args__['LOG_MAX_SIZE'])
        # 日志最大备份数
        self.__Args__['LOG_BACKUP_CNT'] = VarGet(kwargs.get(
            'LOG_BACKUP_CNT'), self.getArg('LOG_BACKUP_CNT'), __cache__.log_backup_cnt)
        self.__Args__['LOG_BACKUP_CNT'] = Str2Int(
            self.__Args__['LOG_BACKUP_CNT'])
        # 是否追踪子文件夹下的SQL文件
        self.__Args__['TRACK_SQL_FILE'] = VarGet(kwargs.get(
            'TRACK_SQL_FILE'), self.getArg('TRACK_SQL_FILE'), __cache__.track_sql_file)
        self.__Args__['TRACK_SQL_FILE'] = Str2Bool(
            self.__Args__['TRACK_SQL_FILE'])
        # 指定model文件夹名称，默认是model
        self.__Args__['MODEL_FOLDER_NAME'] = VarGet(kwargs.get(
            'MODEL_FOLDER_NAME'), self.getArg('MODEL_FOLDER_NAME'), __cache__.model_folder_name)

        # 是否使用Bean来获取数据
        self.__Args__['USE_BEAN'] = VarGet(kwargs.get(
            'USE_BEAN'), self.getArg('USE_BEAN'), __cache__.use_bean)
        # 是否在异常时自动回滚
        self.__Args__['ALLOW_ROLLBACK'] = VarGet(kwargs.get(
            "ALLOW_ROLLBACK"), self.getArg('ALLOW_ROLLBACK'), __cache__.allow_rollback)
        # 是否自动提交
        self.__Args__['AUTO_COMMIT'] = VarGet(kwargs.get(
            "AUTO_COMMIT"), self.getArg('AUTO_COMMIT'), __cache__.auto_commit)
        # SQL模板类型
        self.__Args__['SQL_TEMPLATE_TYPE'] = VarGet(kwargs.get(
            "SQL_TEMPLATE_TYPE"), self.getArg('SQL_TEMPLATE_TYPE'), __cache__.sql_template_type)
        # 可识别最大sql长度
        self.__Args__['MAX_SQL_SIZE'] = VarGet(kwargs.get(
            "MAX_SQL_SIZE"), self.getArg('MAX_SQL_SIZE'), __cache__.max_sql_size)
        # 默认引号类型
        self.__Args__['QUOTATION'] = VarGet(kwargs.get(
            "QUOTATION"), self.getArg('QUOTATION'), __cache__.quotation)

        # 数据库驱动
        self.__Args__['DB_DRIVER'] = VarGet(kwargs.get(
            "DB_DRIVER"), self.getArg('DB_DRIVER'), None)
        # 数据库认证
        self.__Args__['DB_DATABASE'] = VarGet(kwargs.get(
            "DB_DATABASE"), self.getArg('DB_DATABASE'), None)
        self.__Args__['DB_USER'] = VarGet(kwargs.get(
            "DB_USER"), self.getArg('DB_USER'), None)
        self.__Args__['DB_PASSWORD'] = VarGet(kwargs.get(
            "DB_PASSWORD"), self.getArg('DB_PASSWORD'), None)
        self.__Args__['DB_HOST'] = VarGet(kwargs.get(
            "DB_HOST"), self.getArg('DB_HOST'), __cache__.db_host)
        # 默认端口号设置
        __default_port = None
        if self.__Args__['DB_DRIVER'] == "postgres":
            __default_port = 5432
        elif self.__Args__['DB_DRIVER'] == "mysql":
            __default_port = 3306
        # 设置端口号
        self.__Args__['DB_PORT'] = VarGet(kwargs.get(
            "DB_PORT"), self.getArg('DB_PORT'), __default_port, None)
        # sqlite db文件路径
        self.__Args__['SQLITE_PATH'] = VarGet(kwargs.get(
            "SQLITE_PATH"), self.getArg('SQLITE_PATH'), None)

        # 数据库编码
        self.__Args__['ENCODING'] = VarGet(kwargs.get(
            "ENCODING"), self.getArg('ENCODING'), __cache__.encoding)

        # sqlalchemy扩展参数
        self.__Args__['SQLALCHEMY_ARGS'] = Store(VarGet(kwargs.get("SQLALCHEMY_ARGS") if type(
            kwargs.get("SQLALCHEMY_ARGS")) == dict else None, __cache__.sqlalchemy_args))

        # loader外部重载方法
        # connect()
        self.__Args__['RW_CONNECT'] = kwargs.get("RW_CONNECT") if type(
            kwargs.get("RW_CONNECT")) == FunctionType else None
        # execute()
        self.__Args__['RW_EXECUTE'] = kwargs.get("RW_EXECUTE") if type(
            kwargs.get("RW_EXECUTE")) == FunctionType else None
        # close()
        self.__Args__['RW_CLOSE'] = kwargs.get("RW_CLOSE") if type(
            kwargs.get("RW_CLOSE")) == FunctionType else None
        # commit()
        self.__Args__['RW_COMMIT'] = kwargs.get("RW_COMMIT") if type(
            kwargs.get("RW_COMMIT")) == FunctionType else None
        # rollback()
        self.__Args__['RW_ROLLBACK'] = kwargs.get("RW_ROLLBACK") if type(
            kwargs.get("RW_ROLLBACK")) == FunctionType else None
        # inject()
        self.__Args__['RW_INJECT'] = kwargs.get("RW_INJECT") if type(
            kwargs.get("RW_INJECT")) == FunctionType else None

        # 每次都重新读取sql文件，不进缓存
        self.__Args__['HARD_LOAD_SQL'] = VarGet(kwargs.get(
            "HARD_LOAD_SQL"), self.getArg('HARD_LOAD_SQL'), __cache__.hard_load_sql)

        # 缓存数据库连接，保持数据库连接对象，数据库关闭失效
        self.__Args__['CACHE_CONNECT'] = VarGet(kwargs.get(
            "CACHE_CONNECT"), self.getArg('CACHE_CONNECT'), __cache__.cache_connect)

        # 缓存DB预设
        self.__Args__['DB_CONF'] = VarGet(kwargs.get(
            "DB_CONF"), self.getArg('DB_CONF'), None)

    # 获取参数字典

    @property
    def _Args_(self):
        return self.__Args__

    # SQL文件存放目录
    @property
    def SQL_PATH(self):
        return self.__Args__['SQL_PATH']

    @SQL_PATH.setter
    def SQL_PATH(self, value):
        self.__Args__['SQL_PATH'] = PathPlant.transAbspath(value)
        # pass  # 可读写属性

    # LOG文件存放目录
    @property
    def LOG_PATH(self):
        return self.__Args__['LOG_PATH']

    @LOG_PATH.setter
    def LOG_PATH(self, value):
        self.__Args__['LOG_PATH'] = PathPlant.transAbspath(value)
        # pass  # 可读写属性

    # 是否输出日志文件
    @property
    def LOG_ON(self):
        return self.__Args__['LOG_ON']

    @LOG_ON.setter
    def LOG_ON(self, value):
        self.__Args__['LOG_ON'] = value
        # pass  # 可读写属性

    # 是否开启控制台
    @property
    def CONSOLE_ON(self):
        return self.__Args__['CONSOLE_ON']

    @CONSOLE_ON.setter
    def CONSOLE_ON(self, value):
        self.__Args__['CONSOLE_ON'] = value
        # pass  # 可读写属性

    # 是否是debug模式
    @property
    def DEBUG(self):
        return self.__Args__['DEBUG']

    @DEBUG.setter
    def DEBUG(self, value):
        self.__Args__['DEBUG'] = value
        # pass  # 可读写属性

    # 单个日志文件最大容量(mb)
    @property
    def LOG_MAX_SIZE(self):
        return self.__Args__['LOG_MAX_SIZE']

    @LOG_MAX_SIZE.setter
    def LOG_MAX_SIZE(self, value):
        self.__Args__['LOG_MAX_SIZE'] = value
        # pass  # 可读写属性

    # 日志最大备份数
    @property
    def LOG_BACKUP_CNT(self):
        # print(self.__Args__)
        return self.__Args__['LOG_BACKUP_CNT']

    @LOG_BACKUP_CNT.setter
    def LOG_BACKUP_CNT(self, value):
        self.__Args__['LOG_BACKUP_CNT'] = value
        # pass  # 可读写属性

    # 是否追踪子文件夹下的SQL文件
    @property
    def TRACK_SQL_FILE(self):
        return self.__Args__['TRACK_SQL_FILE']

    @TRACK_SQL_FILE.setter
    def TRACK_SQL_FILE(self, value):
        # self.__Args__['TRACK_SQL_FILE'] = value
        pass  # 只读属性

    # 指定model文件夹名称，默认是model
    @property
    def MODEL_FOLDER_NAME(self):
        return self.__Args__['MODEL_FOLDER_NAME']

    @MODEL_FOLDER_NAME.setter
    def MODEL_FOLDER_NAME(self, value):
        # self.__Args__['MODEL_FOLDER_NAME'] = value
        pass  # 只读属性

    # 是否使用Bean来获取数据
    @property
    def USE_BEAN(self):
        return self.__Args__['USE_BEAN']

    @USE_BEAN.setter
    def USE_BEAN(self, value):
        # self.__Args__['USE_BEAN'] = value
        pass  # 只读属性

    # 是否在异常时自动回滚
    @property
    def ALLOW_ROLLBACK(self):
        return self.__Args__['ALLOW_ROLLBACK']

    @ALLOW_ROLLBACK.setter
    def ALLOW_ROLLBACK(self, value):
        # self.__Args__['ALLOW_ROLLBACK'] = value
        pass  # 只读属性

    # 是否自动提交
    @property
    def AUTO_COMMIT(self):
        return self.__Args__['AUTO_COMMIT']

    @AUTO_COMMIT.setter
    def AUTO_COMMIT(self, value):
        # self.__Args__['AUTO_COMMIT'] = value
        pass  # 只读属性

    # SQL模板类型
    @property
    def SQL_TEMPLATE_TYPE(self):
        return self.__Args__['SQL_TEMPLATE_TYPE']

    @SQL_TEMPLATE_TYPE.setter
    def SQL_TEMPLATE_TYPE(self, value):
        # self.__Args__['SQL_TEMPLATE_TYPE'] = value
        pass  # 只读属性

    # 可识别最大sql长度
    @property
    def MAX_SQL_SIZE(self):
        return self.__Args__['MAX_SQL_SIZE']

    @MAX_SQL_SIZE.setter
    def MAX_SQL_SIZE(self, value):
        # self.__Args__['MAX_SQL_SIZE'] = value
        pass  # 只读属性

    # 默认引号类型
    @property
    def QUOTATION(self):
        return self.__Args__['QUOTATION']

    @QUOTATION.setter
    def QUOTATION(self, value):
        # self.__Args__['QUOTATION'] = value
        pass  # 只读属性

    # 数据库驱动
    @property
    def DB_DRIVER(self):
        return self.__Args__['DB_DRIVER']

    @DB_DRIVER.setter
    def DB_DRIVER(self, value):
        self.__Args__['DB_DRIVER'] = value
        # pass  # 只读属性

    # 数据库认证
    @property
    def DB_DATABASE(self):
        return self.__Args__['DB_DATABASE']

    @DB_DATABASE.setter
    def DB_DATABASE(self, value):
        self.__Args__['DB_DATABASE'] = value
        # pass  # 只读属性

    @property
    def DB_USER(self):
        return self.__Args__['DB_USER']

    @DB_USER.setter
    def DB_USER(self, value):
        self.__Args__['DB_USER'] = value
        # pass  # 只读属性

    @property
    def DB_PASSWORD(self):
        return self.__Args__['DB_PASSWORD']

    @DB_PASSWORD.setter
    def DB_PASSWORD(self, value):
        self.__Args__['DB_PASSWORD'] = value
        # pass  # 只读属性

    @property
    def DB_HOST(self):
        return self.__Args__['DB_HOST']

    @DB_HOST.setter
    def DB_HOST(self, value):
        self.__Args__['DB_HOST'] = value
        # pass  # 只读属性

    @property
    def DB_PORT(self):
        return self.__Args__['DB_PORT']

    @DB_PORT.setter
    def DB_PORT(self, value):
        self.__Args__['DB_PORT'] = value
        # pass  # 只读属性

    # sqlite db文件路径
    @property
    def SQLITE_PATH(self):
        return self.__Args__['SQLITE_PATH']

    @SQLITE_PATH.setter
    def SQLITE_PATH(self, value):
        self.__Args__['SQLITE_PATH'] = value
        # pass  # 只读属性

    # 数据库编码
    @property
    def ENCODING(self):
        return self.__Args__['ENCODING']

    @ENCODING.setter
    def ENCODING(self, value):
        self.__Args__['ENCODING'] = value
        # pass  # 只读属性

    # sqlalchemy扩展参数
    @property
    def SQLALCHEMY_ARGS(self):
        return self.__Args__['SQLALCHEMY_ARGS']

    @SQLALCHEMY_ARGS.setter
    def SQLALCHEMY_ARGS(self, value):
        self.__Args__['SQLALCHEMY_ARGS'] = value
        # pass  # 只读属性

    # loader外部重载方法
    @property
    def RW_CONNECT(self):
        return self.__Args__['RW_CONNECT']

    @RW_CONNECT.setter
    def RW_CONNECT(self, value):
        # self.__Args__['RW_CONNECT'] = value
        pass  # 只读属性

    @property
    def RW_EXECUTE(self):
        return self.__Args__['RW_EXECUTE']

    @RW_EXECUTE.setter
    def RW_EXECUTE(self, value):
        # self.__Args__['RW_EXECUTE'] = value
        pass  # 只读属性

    @property
    def RW_CLOSE(self):
        return self.__Args__['RW_CLOSE']

    @RW_CLOSE.setter
    def RW_CLOSE(self, value):
        # self.__Args__['RW_CLOSE'] = value
        pass  # 只读属性

    @property
    def RW_COMMIT(self):
        return self.__Args__['RW_COMMIT']

    @RW_COMMIT.setter
    def RW_COMMIT(self, value):
        # self.__Args__['RW_COMMIT'] = value
        pass  # 只读属性

    @property
    def RW_ROLLBACK(self):
        return self.__Args__['RW_ROLLBACK']

    @RW_ROLLBACK.setter
    def RW_ROLLBACK(self, value):
        # self.__Args__['RW_ROLLBACK'] = value
        pass  # 只读属性

    @property
    def RW_INJECT(self):
        return self.__Args__['RW_INJECT']

    @RW_INJECT.setter
    def RW_INJECT(self, value):
        # self.__Args__['RW_INJECT'] = value
        pass  # 只读属性

    # 每次都重新读取sql文件，不进缓存
    @property
    def HARD_LOAD_SQL(self):
        return self.__Args__['HARD_LOAD_SQL']

    @HARD_LOAD_SQL.setter
    def HARD_LOAD_SQL(self, value):
        # self.__Args__['HARD_LOAD_SQL'] = value
        pass  # 只读属性

    # 缓存数据库连接，保持数据库连接对象，数据库关闭失效
    @property
    def CACHE_CONNECT(self):
        return self.__Args__['CACHE_CONNECT']

    @CACHE_CONNECT.setter
    def CACHE_CONNECT(self, value):
        # self.__Args__['CACHE_CONNECT'] = value
        pass  # 只读属性

    # 多DB预设
    @property
    def DB_CONF(self):
        return self.__Args__['DB_CONF']

    @DB_CONF.setter
    def DB_CONF(self, value):
        # self.__Args__['DB_CONF'] = value
        pass  # 只读属性


class InitGuide(GuideArgs, PathPlant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 模块名字
        self.module_name = __cache__.model_name if len(args) == 0 else args[0]
        # 生成缓存对象，一个实例生成一个缓存对象
        self.cache = ConfStore(
            # 已缓存全部sql数据
            all_sqls_cached=False,
            # @entry注解调用计数，目前只允许一个
            entry_cnt=0,
            # # 一次性读取的sql文件路径
            # folder_structure=list(),
            # # 一次性缓存的sql数据
            # sql_str_dict=dict(),
            # 缓存DB连接头
            # conn_headstr = list()
        )
        # 缓存DB连接的字典
        self.conn_cache = dict()
        # 解析sql,log,env文件夹路径
        self.resolvePath()

    # 从配置中获取DB信息
    def getDBInfoFromConf(self, dbModelName):
        return {
            'DB_DRIVER': None if dbModelName == None else self.getArgsBySuffix(dbModelName, 'DB_DRIVER'),
            'DB_DATABASE': None if dbModelName == None else self.getArgsBySuffix(dbModelName, 'DB_DATABASE'),
            'DB_USER': None if dbModelName == None else self.getArgsBySuffix(dbModelName, 'DB_USER'),
            'DB_PASSWORD': None if dbModelName == None else self.getArgsBySuffix(dbModelName, 'DB_PASSWORD'),
            'DB_HOST': None if dbModelName == None else self.getArgsBySuffix(dbModelName, 'DB_HOST'),
            'DB_PORT': None if dbModelName == None else self.getArgsBySuffix(dbModelName, 'DB_PORT'),
            'ALLOW_ROLLBACK': None if dbModelName == None else self.getArgsBySuffix(dbModelName, 'ALLOW_ROLLBACK'),
            'AUTO_COMMIT': None if dbModelName == None else self.getArgsBySuffix(dbModelName, 'AUTO_COMMIT'),
            'ENCODING': None if dbModelName == None else self.getArgsBySuffix(dbModelName, 'ENCODING'),
        }

    # 获取数据库连接信息
    def getAccessInfo(self, dbModelName):
        if self.DB_CONF == None:
            DB_CONF = self.getDBInfoFromConf(dbModelName)
        else:
            if self.DB_CONF.get(dbModelName) == None:
                DB_CONF = self.getDBInfoFromConf(dbModelName)
            else:
                DB_CONF = self.DB_CONF.get(dbModelName)
        return DB_CONF

    # 获取数据库连接头列表
    def getAccessHeadStr(self):
        # 从参数中获取
        conn_headstr = []
        for model_name in self.DB_CONF:
            conn_headstr.append(model_name)
        # 从配置文件中获取
        for model_name in self.getSections(__cache__.conf_section_prefix):
            conn_headstr.append(model_name)
        # 去重
        conn_headstr = list(set(conn_headstr))
        self.cache.create('conn_headstr', conn_headstr)
        return conn_headstr

    # 解析文件夹路径
    def resolvePath(self, sql_on=False):
        if sql_on:
            # 解决sql文件夹
            if self.SQL_PATH == None:
                self.SQL_PATH = os.path.realpath('sql')
            # self.initFolder(self.SQL_PATH)
            # 路径写入缓存
            __cache__.modify('sql_dir', self.SQL_PATH)
        # 解决log文件夹
        if self.LOG_ON:
            if self.LOG_PATH == None:
                self.LOG_PATH = os.path.realpath('log')
            # self.initFolder(self.LOG_PATH)
            # 路径写入缓存
            __cache__.modify('log_dir', self.LOG_PATH)
        # 解决env文件夹
        if self.ENV_ON:
            if self.ENV_DIR == None:
                self.ENV_DIR = os.path.realpath('env')
            # self.initFolder(self.ENV_DIR)
            # 路径写入缓存
            __cache__.modify('env_dir', self.ENV_DIR)

    # 解决sql后缀名
    def resolveSqlExtension(self, sqlname):
        return sqlname if sqlname[-4:] == '.sql' else sqlname + '.sql'

    # 根据sql文件名查找sql路径
    def getSqlPath(self, sqlname):
        # 解析后缀名
        _sqlname = self.resolveSqlExtension(sqlname)
        # 缓存sql文件列表
        if self.cache.folder_structure == None:
            self.cacheSqlPaths()
        #
        for sqlpath in self.cache.folder_structure.PATH_LIST:
            if os.path.basename(sqlpath) == _sqlname:
                return sqlpath
        return None

    # 缓存sql文件路径
    def cacheSqlPaths(self):
        if not self.cache.folder_structure:
            folder_structure = self.deepenFolder(self.SQL_PATH)
            self.cache.create('folder_structure', folder_structure)

    # 缓存sql字符串
    def cacheSqlString(self, sql_path_list):
        sql_str_dict = {}
        for sqlPath in sql_path_list:
            with open(sqlPath, "r", encoding='utf-8') as fs_sql:
                sqlStr = fs_sql.read()
                sql_str_dict[sqlPath] = sqlStr
        self.cache.create('sql_str_dict', sql_str_dict)

    # 解析sql文件路径
    def resolveSqlPath(self, func_name, model_path):
        if self.TRACK_SQL_FILE and self.MODEL_FOLDER_NAME != None:
            # 模块路径截取，model_path是包含文件名的
            preModelPath, relModelPath = self.splitFolder(
                model_path, self.MODEL_FOLDER_NAME, includeModel=False)
            # sql文件全路径,[:-3]是去掉后缀名.py
            sql_fullpath = os.path.join(
                self.SQL_PATH, relModelPath[:-3], func_name + '.sql')
            return sql_fullpath
        else:
            sql_fullpath = self.getSqlPath(func_name)
            return sql_fullpath

    # 通过sql_name解析sql文件路径
    def resolveSqlPathSn(self, sql_name):
        sql_fullpath = os.path.join(
            self.SQL_PATH, self.resolveSqlExtension(sql_name))
        return sql_fullpath

    # 主动缓存sql文件
    def cacheSqlFiles(self):
        # 读取全部sql文件
        self.cacheSqlPaths()
        # 读取全部的sql字符串
        self.cacheSqlString(self.cache.folder_structure.PATH_LIST)
        # 把已缓存sql标记为True
        self.cache.modify('all_sqls_cached', True)

    # 主动缓存db连接
    def cacheDbConn(self):
        for model_name in self.getAccessHeadStr():
            dbConf = self.getAccessInfo(model_name)
            if self.RW_CONNECT:
                self.conn_cache[model_name] = self.RW_CONNECT(dbConf=dbConf)
            else:
                self.conn_cache[model_name] = self.connect(dbConf=dbConf)

    # 主动调用路径模板向导
    def runGuide(self):
        self.initFolder(self.SQL_PATH)
        self.initFolder(self.LOG_PATH)
        self.initFolder(self.ENV_DIR)

    # 控制台输出
    def __print(self, level, message, *msgs):
        # 获取当前帧对象 ， 代表执行到当前的logging函数
        cur_frame = inspect.currentframe()
        # 获取上一帧对象 ， 代表谁调用的
        # bac_frame = cur_frame.f_back
        bac_frame = cur_frame
        # 字符串转换
        __msgs = tuple(map(lambda m: str(m), msgs))
        # 添加换行符
        msgStr = '\n'.join(__msgs)
        # 字符串message
        if type(message) == str:
            # 合并
            message = message + '\n' + msgStr
            self.__logger.print(level, message, cur_frame=bac_frame)
        else:
            # Exception message
            self.__logger.print(level, msgStr, cur_frame=bac_frame)
            self.__logger.print(level, message, cur_frame=bac_frame)
        # self.__logger.print(level, message, cur_frame=bac_frame)

    # 日志输出
    def __logging(self, level, message, *msgs):
        # 获取当前帧对象 ， 代表执行到当前的logging函数
        cur_frame = inspect.currentframe()
        # 获取上一帧对象 ， 代表谁调用的
        # bac_frame = cur_frame.f_back
        bac_frame = cur_frame
        # 字符串转换
        __msgs = tuple(map(lambda m: str(m), msgs))
        # 添加换行符
        msgStr = '\n'.join(__msgs)
        # 字符串message
        if type(message) == str:
            # 合并
            message = message + '\n' + msgStr
            self.__logger.logging(level, message, cur_frame=bac_frame)
        else:
            # Exception message
            self.__logger.logging(level, msgStr, cur_frame=bac_frame)
            self.__logger.logging(level, message, cur_frame=bac_frame)

    # 打印输出函数
    def logging(self, level, message, *msgs):
        if self.CONSOLE_ON:
            self.__print(level, message, *msgs)
        if self.LOG_ON:
            self.__logging(level, message, *msgs)

    # 初始化logging
    def initLogging(self):
        logPath = None
        if self.LOG_PATH:
            logPath = os.path.join(self.LOG_PATH, self.module_name + ".log")
        #
        self.__logger = LoggerFactory(
            path=logPath,
            console=False,
            debug=self.DEBUG,
            maxMb=self.LOG_MAX_SIZE,
            backupCount=self.LOG_BACKUP_CNT,
            logOn=self.LOG_ON)
