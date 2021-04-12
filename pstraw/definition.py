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
    # 是否不输出日志文件
    log_on=False,
    # 是否是debug模式
    debug=True,
    # 单个日志文件最大容量(mb)
    log_max_size=10,
    # 日志最大备份数
    log_backup_cnt=1,
    # 是否追踪子文件夹下的SQL文件
    track_sql_file=False,
    # 默认模块文件夹名称
    model_folder_name='model',
    # 默认模块名
    model_name='straw',
    # 自动Bean注入
    use_bean=True,
    # 是否自动回滚
    allow_rollback=True,
    # 是否自动提交
    auto_commit=True,
    # sql模板类型
    sql_template_type=3,
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

GlobalConfig = __cache__
SQLTypeMap = __type_reflect__