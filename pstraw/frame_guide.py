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
import sys
import os
import inspect
import traceback
import configparser
import logging
import logging.handlers
from dataclasses import dataclass
from .screws import PathPlant
from .tool import Str2Bool, Str2Int, VarGet
from .definition import __cache__
from .logger_factory import LoggerFactory


# conf文件获取初始化参数
class ConfArgs():
    def __init__(self, *args, **kwargs):
        # 初始化配置
        self.__configparser__ = configparser.ConfigParser()
        # 配置文件路径
        self.__CONF_PATH = PathPlant.transAbspath(
            kwargs.get('CONF_PATH') or None)
        # 配置文件夹
        self.__CONF_DIR = PathPlant.transAbspath(None if self.__CONF_PATH == None else os.path.dirname(
            self.__CONF_PATH))
        # print("ConfArgs", kwargs)
        # 读取配置
        self.loadConf()

    def loadConf(self):
        # print(self.__CONF_PATH)
        if self.__CONF_PATH != None:
            self.__configparser__.read(self.__CONF_PATH, encoding="utf-8")
        return self.__configparser__

    def getArg(self, arg, namespace=__cache__.model_name):
        if self.__configparser__.has_section(namespace):
            sec = self.__configparser__._sections
            conf = sec.get(namespace)
            return conf.get(arg.lower())
        else:
            return None

    # 配置文件夹
    @property
    def CONF_DIR(self):
        return self.__CONF_DIR

    @CONF_DIR.setter
    def CONF_DIR(self, value):
        self.__CONF_DIR = PathPlant.transAbspath(value)
        pass  # 读写属性

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
        # 是否不输出日志文件
        self.__Args__['LOG_ON'] = VarGet(kwargs.get(
            'LOG_ON'), self.getArg('LOG_ON'), __cache__.log_on)
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
            "DB_HOST"), self.getArg('DB_HOST'), None)
        self.__Args__['DB_PORT'] = VarGet(kwargs.get(
            "DB_PORT"), self.getArg('DB_PORT'), None)
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

    # 是否不输出日志文件
    @property
    def LOG_ON(self):
        return self.__Args__['LOG_ON']

    @LOG_ON.setter
    def LOG_ON(self, value):
        self.__Args__['LOG_ON'] = value
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

    # 数据库驱动
    @property
    def DB_DRIVER(self):
        return self.__Args__['DB_DRIVER']

    @DB_DRIVER.setter
    def DB_DRIVER(self, value):
        # self.__Args__['DB_DRIVER'] = value
        pass  # 只读属性

    # 数据库认证
    @property
    def DB_DATABASE(self):
        return self.__Args__['DB_DATABASE']

    @DB_DATABASE.setter
    def DB_DATABASE(self, value):
        # self.__Args__['DB_DATABASE'] = value
        pass  # 只读属性

    @property
    def DB_USER(self):
        return self.__Args__['DB_USER']

    @DB_USER.setter
    def DB_USER(self, value):
        # self.__Args__['DB_USER'] = value
        pass  # 只读属性

    @property
    def DB_PASSWORD(self):
        return self.__Args__['DB_PASSWORD']

    @DB_PASSWORD.setter
    def DB_PASSWORD(self, value):
        # self.__Args__['DB_PASSWORD'] = value
        pass  # 只读属性

    @property
    def DB_HOST(self):
        return self.__Args__['DB_HOST']

    @DB_HOST.setter
    def DB_HOST(self, value):
        # self.__Args__['DB_HOST'] = value
        pass  # 只读属性

    @property
    def DB_PORT(self):
        return self.__Args__['DB_PORT']

    @DB_PORT.setter
    def DB_PORT(self, value):
        # self.__Args__['DB_PORT'] = value
        pass  # 只读属性


class InitGuide(GuideArgs, PathPlant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 模块名字
        self.module_name = __cache__.model_name if len(args) == 0 else args[0]

    # 初始化文件夹
    def resolvePath(self):
        # 解决sql文件夹
        if self.SQL_PATH == None:
            self.SQL_PATH = os.path.realpath('sql')
        self.initFolder(self.SQL_PATH)
        # 路径写入缓存
        __cache__.modify('sql_dir', self.SQL_PATH)
        # 解决log文件夹
        if self.LOG_PATH == None:
            self.LOG_PATH = os.path.realpath('log')
        self.initFolder(self.LOG_PATH)
        # 路径写入缓存
        __cache__.modify('log_dir', self.LOG_PATH)
        # 解决env文件夹
        if self.CONF_DIR == None:
            self.CONF_DIR = os.path.realpath('env')
        self.initFolder(self.CONF_DIR)
        # 路径写入缓存
        __cache__.modify('env_dir', self.CONF_DIR)

    # 根据sql文件名查找sql路径
    def getSqlPath(self, sqlname):
        # 解析后缀名
        _sqlname = sqlname if sqlname[-4] == '.sql' else sqlname + '.sql'
        # 获取sql文件列表
        folder_structure = self.deepenFolder(self.SQL_PATH)
        for sqlpath in folder_structure.PATH_LIST:
            if os.path.basename(sqlpath) == _sqlname:
                return sqlpath
        return None

    # 解析sql文件路径
    def resolveSqlPath(self, func_name, model_path):
        if self.TRACK_SQL_FILE and self.MODEL_FOLDER_NAME != None:
            # 模块路径截取，model_path是包含文件名的
            model_split_paths = self.splitFolder(
                model_path, self.MODEL_FOLDER_NAME, includeModel=False)
            # sql文件全路径,[:-3]是去掉后缀名.py
            sql_fullpath = os.path.join(
                self.SQL_PATH, model_split_paths[1][:-3], func_name + '.sql')
            return sql_fullpath
        else:
            sql_fullpath = self.getSqlPath(func_name)
            return sql_fullpath
    # 通过sql_name解析sql文件路径

    def resolveSqlPathSn(self, sql_name):
        sql_fullpath = self.getSqlPath(sql_name)
        return sql_fullpath

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
        self.__print(level, message, *msgs)
        if self.LOG_ON:
            self.__logging(level, message, *msgs)

    # 初始化logging
    def initLogging(self):
        self.__logger = LoggerFactory(
            path=os.path.join(self.LOG_PATH, self.module_name + ".log"),
            console=False,
            debug=self.DEBUG,
            maxMb=self.LOG_MAX_SIZE,
            backupCount=self.LOG_BACKUP_CNT,
            logOn=self.LOG_ON)
