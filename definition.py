#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    全局定义
# Created : 2020.10.14
# Author : Chalk Yu
# ========================================
from .screws import ConfStore, Store
# 默认参数常量
__cache__ = ConfStore(
    # 路径缓存定义
    root_dir=None,  # 项目根目录
    model_dir=None,  # 模型文件目录
    env_dir=None,  # 配置目录
    conf_file=None,  # 配置文件路径
    sql_dir=None,  # sql文件目录
    log_dir=None,  # log文件目录
    # 默认模块文件夹名称
    model_folder='model',
    # 默认模块名
    model_name='pskel'
)

# DB类型反射python类型
__type_reflect__ = Store(
    {
        "postgres":{
            "varchar":str,
            "int":int,
            "datetime":str
        },
        "db2":{
            "varchar":str,
            "int":int,
            "datetime":str
        },
        "mysql":{
            "varchar":str,
            "int":int,
            "datetime":str
        },
        "sqlite":{
            "varchar":str,
            "int":int,
            "datetime":str
        },
        "oracle":{
            "varchar":str,
            "int":int,
            "datetime":str
        }
    }
)
