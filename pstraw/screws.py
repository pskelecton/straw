#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    工具类
#    反射类、数据仓库类、路径加工、缓存
# Created : 2020.10.14
# Author : Chalk Yu
# ========================================
from promise import Promise
import os
import inspect
from dataclasses import dataclass

# 字典反射对象使用案例
# ConfStore = Store({})
# ConfStore.a = {'xxx': Store({'yyy': 123})}
# ConfStore.b = {'xxx': {'yyy': 123}}

# 配置对象，控制对象只读
class ConfStore():
    def __init__(self, **kwargs):
        self.__ConfStore__ = Store(kwargs)

    def __repr__(self):
        return str(self.__ConfStore__)

    def __str__(self):
        return str(self.__ConfStore__)

    def __getattr__(self, name):
        return self.__ConfStore__.get(name)

    def create(self, name, value):
        if self.__ConfStore__.get(name) == None:
            self.__ConfStore__[name] = value
            return True
        else:
            return False

    def modify(self, name, value):
        if self.__ConfStore__.get(name) != None:
            self.__ConfStore__[name] = value
            return True
        else:
            return False

    def remove(self, name):
        del self.__ConfStore__[name]


# 路径加工类
class PathPlant():
    def __init__(self, *args, **kwargs):
        super().__init__()
        # 接收一个model名的参数
        self.MODEL_FOLDER_NAME = kwargs.get('MODEL_FOLDER_NAME') if not hasattr(
            self, "MODEL_FOLDER_NAME") else getattr(self, "MODEL_FOLDER_NAME")

    # 转换绝对路径，纯静态方法，外部直接访问
    # 规则转换: @/xxx/ 则只取相对路径 , 没有@/则转换绝对路径
    @staticmethod
    def transAbspath(path):
        if type(path) == str:
            if path[:2] == '@/':
                # 相对路径转换
                # return os.path.normpath(path[2:])
                # 绝对路径转换
                return os.path.realpath(path[2:])
            else:
                # 绝对路径转换
                return os.path.abspath(path)
        else:
            return None

    # 获取模型绝对路径
    @classmethod
    def getModelPath(cls, model_func):
        # 获取模型绝对路径
        model_path = os.path.abspath(inspect.getfile(model_func))
        return model_path

    # 初始化文件夹，静态+对象方法，可直接访问，可继承访问
    @classmethod
    def splitFolder(cls, path, modelStr, includeModel=True):
        # 文件或目录检测,解决path最后带\\或/的情况
        tempath = os.path.split(path)
        if tempath[1] == '':
            path = tempath[0]
        #
        head = path
        tail = ""
        #
        skip = False
        while not skip:
            sp = os.path.split(head)
            # 匹配到或者都没有匹配到则跳出
            if sp[1] == modelStr or sp[0] == "":
                skip = True
            # 初始赋值
            if tail == "":
                tail = sp[1]
            else:
                if sp[1] == modelStr and includeModel == False:
                    # 不组装modelStr
                    pass
                else:
                    # 每次循环都合并一下路径
                    tail = os.path.join(sp[1], tail)
            head = sp[0]
        return [head, tail]

    @classmethod
    def initFolder(cls, path):
        # 判断路径是否存在，不存在则创建文件夹
        if not os.path.exists(path):
            # os.mkdir(path, mode=0o777)
            os.makedirs(path, mode=0o777, exist_ok=False)

    # 深度遍历文件，path一定要是绝对路径，静态+对象方法，可直接访问，可继承访问
    @classmethod
    def deepenFolder(cls, path):
        _file_list = list()
        _dep_file_dict = dict()

        # 结构化文件夹
        def traverseFile(dir_path):
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                file_list = os.listdir(dir_path)
                dep_file_dict = dict()
                for file_name in file_list:
                    file_path = os.path.join(dir_path, file_name)
                    if os.path.isdir(file_path):
                        dep_file_dict[file_name] = traverseFile(file_path)
                    else:
                        _file_list.append(file_path)
                        dep_file_dict[file_name] = file_path
                return dep_file_dict
            else:
                raise Exception

        # 生成文件结构化对象
        _dep_file_dict = traverseFile(os.path.abspath(path))

        return Store({'FILE_STRUCTURE': _dep_file_dict, 'PATH_LIST': _file_list})


# 字典反射成对象
class Store(dict):
    # 缓冲数据
    __cache_dict = None

    def __init__(self, iterable=None):
        iterable = iterable or {}
        self.__cache_dict = dict(iterable)
        super().__init__(iterable)
        self.__reflect__(iterable)

    # 构建时反射值
    def __reflect__(self, _dict):
        for key in _dict:
            if type(_dict[key]) == dict:
                self.__dict__[key] = Store(_dict[key])
            else:
                self.__dict__[key] = _dict[key]

    # 更新时同步反射
    def __updvalue__(self, key, value):
        # 判断旧值不等于新值的情况
        if str(self.__cache_dict.get(key)) != str(value):
            # 更新缓冲数据
            self.__cache_dict[key] = value
            # 引用赋值
            if type(value) == dict:
                self.__dict__[key] = Store(value)
            else:
                self.__dict__[key] = value
            # 赋值
            super().__setitem__(key, value)

    # 对象属性赋值拦截
    def __setattr__(self, key, value):
        if self.__cache_dict != None:
            self.__updvalue__(key, value)
        else:
            self.__dict__[key] = value

    # 字典属性赋值拦截
    def __setitem__(self, key, value):
        if self.__cache_dict != None:
            self.__updvalue__(key, value)

    # 字典取值拦截
    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except Exception as exc:
            return None

    # 解除属性引用
    def __delattr__(self, key):
        try:
            del self.__dict__[key]
            super().__delitem__(key)
        except Exception as exc:
            pass

    # 解除字典属性引用
    def __delitem__(self, key):
        try:
            del self.__dict__[key]
            super().__delitem__(key)
        except Exception as exc:
            pass
