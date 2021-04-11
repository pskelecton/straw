#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    对象关系模型（ORM）工厂类
#    用于处理对象关系模型的Loader
# Created : 2020.10.14
# Author : Chalk Yu
# ========================================
from __future__ import absolute_import
from . import loader


class OrmFactory():
    def __init__(self):
        super().__init__()

    # 对象关系模型loader构造器
    def loaderCreater(self, loader):
        exec(f'from .loader import {loader}')
        __module__ = eval(loader)
        __loader__ = __module__.loader

        class OrmEngine(__loader__):
            def __init__(self, *args, **kwargs):
                super().__init__()
        return OrmEngine


orm = OrmFactory()
