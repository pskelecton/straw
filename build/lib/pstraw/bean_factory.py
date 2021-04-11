#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    Bean工厂
#    默认Bean接口，Bean的加载器
# Created : 2020.10.14
# Author : Chalk Yu
# ========================================
from dataclasses import dataclass
import sqlparse


class Bean():
    def __init__(self):
        super().__init__()


class BeanFactory():
    def __init__(self):
        super().__init__()

    def createResultClass(self, *classType):
        class ResultBean(*classType):
            def __init__(self, *args, **kwargs):
                if len(classType) > 0:
                    super().__init__(*args)
                self.__cursor = kwargs.get('cursor') or None
                self.__count = kwargs.get('count') or None

            @property
            def cursor(self):
                return self.__cursor

            @cursor.setter
            def cursor(self, _cursor):
                # 有值后即被锁死
                if self.__cursor == None:
                    self.__cursor = _cursor

            @property
            def count(self):
                return self.__count

            @count.setter
            def count(self, _count):
                # 有值后即被锁死
                if self.__count == None:
                    self.__count = _count
        return ResultBean

    def _inject_(self, fn):
        def __inject__(*args, **kwargs):
            kwargs['__bean_factory__'] = self
            return fn(*args, **kwargs)
        return __inject__


bf = BeanFactory()
