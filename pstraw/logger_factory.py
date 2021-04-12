#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    输出控制台模块
#    用于日志打印和控制台输出、错误追踪
# Created : 2020.10.14
# Author : Chalk Yu
# ========================================
from __future__ import print_function
import logging
import logging.handlers
import chalk
from chalk import Chalk
import os
import math
import inspect
import traceback
import sys
import os
# 函数重载
from functools import singledispatch

# cmd中需要关闭echo
os.system('@echo off')
#

class LoggerFactory():
    def __init__(self, path='./default.log', console=False, debug=True, maxMb=1, backupCount=5, logOn=True):
        self.path = path
        self.console = console
        self.maxMb = maxMb
        self.backupCount = backupCount
        self.debug = debug
        self.logOn = logOn
        self.__create()

    # 初始化logging
    def __create(self, debug=None):
        # 无日志设置
        if self.logOn == False:
            self.__logger = None
            return
        # 路径截取的文件名做为模块名
        module_name = os.path.basename(self.path)
        # 获取logging对象
        self.__logger = logging.getLogger(module_name)
        #
        __debug = self.debug if debug == None else debug
        # 设置阈值 ，低于阈值以下的则不输出(DEBUG < INFO < WARNING < ERROR)
        if __debug == True:
            self.__logger.setLevel(logging.DEBUG)
        else:
            self.__logger.setLevel(logging.INFO)
        # 设置日志格式化 (时间 - 消息)
        __formatter = logging.Formatter('%(asctime)s - %(message)s', style='%')
        # log文件不存在的情况，初始化log
        if not self.__logger.handlers:
            if self.console:
                # 控制台输出的 handler
                __stream_handler = logging.StreamHandler()
                __stream_handler.setFormatter(__formatter)
                self.__logger.addHandler(__stream_handler)
            # 文件输出的 handler
            __file_handler = logging.handlers.RotatingFileHandler(
                filename=os.path.abspath(self.path),
                maxBytes=math.pow(2, 20)*self.maxMb,
                backupCount=self.backupCount,
                encoding='utf-8',
                delay=False)
            __file_handler.setFormatter(__formatter)
            self.__logger.addHandler(__file_handler)

    # 获取logger
    def logger(self, debug=True):
        self.__create(debug)
        return self.__logger

    # log输出
    def logging(self, level, message, cur_frame=None):
        # 无日志设置
        if self.logOn == False:
            self.__logger = None
            return
        # 获取当前帧对象 ， 代表执行到当前的logging函数
        cur_frame = cur_frame or inspect.currentframe()
        # 获取上一帧对象 ， 代表谁调用的logging
        bac_frame = cur_frame.f_back
        # 从帧对象中获取信息
        bac_frame_info = inspect.getframeinfo(bac_frame)
        # 截取文件名
        fileName = bac_frame_info.filename
        # 异常处理
        isError = isinstance(message, Exception)
        if isError:
            level = 'ERROR'
            message = traceback.format_exc()

        # 控制台打印异常信息
        if not self.console:
            self.print(level, message, cur_frame=bac_frame)

        message = "{0}[{1}] >>> {2:<6} >>> {3}".format(fileName,
                                                       str(bac_frame_info.lineno), level, message)

        if (level == "INFO"):
            self.__logger.info(message)
        elif (level == "ERROR"):
            self.__logger.error(message)
        elif (level == "DEBUG"):
            self.__logger.debug(message)
        elif (level == "WARN"):
            self.__logger.warning(message)

    def print(self, level, message, cur_frame=None):
        # 异常检测
        isError = isinstance(message, Exception)
        if isError:
            if level != 'ERROR' and level != 'WARN':
                level = 'ERROR'
            message = traceback.format_exc()
        # 获取当前帧对象 ， 代表执行到当前的logging函数
        # cur_frame = cur_frame or inspect.currentframe().f_back
        cur_frame = cur_frame or inspect.currentframe()
        # 获取上一帧对象 ， 代表谁调用的logging
        bac_frame = cur_frame.f_back
        # 从帧对象中获取信息
        bac_frame_info = inspect.getframeinfo(bac_frame)
        # 截取文件名
        fileName = bac_frame_info.filename
        if level == 'ERROR':
            # 控制台打印异常信息
            print(chalk.white('ERROR'.capitalize(), background='red'))
            print(chalk.red(message))
            self.print_traceback(color='red', cur_frame=bac_frame)
        elif level == 'WARN':
            # 控制台打印异常信息
            print(chalk.black('WARNING'.capitalize(), background='yellow'))
            print(chalk.yellow(message))
            if isError:
                self.print_traceback(
                    color='yellow', font_color='black', cur_frame=bac_frame)
        elif level == 'DEBUG':
            print(chalk.white(level.capitalize(), background='cyan'))
            print(chalk.cyan(message))
        else:
            print(message)

    # 追踪执行的文件、行号以及函数名
    def traceback(self, cur_frame=None):
        # 项目入口的根目录
        entry_dir = os.path.realpath('.')
        # 追踪记录
        trace_stack = []
        #
        cur_frame = cur_frame or inspect.currentframe().f_back
        # 上一帧
        pre_frame = None
        #
        isSkip = False
        while not isSkip:
            # 获取帧信息
            frame_info = inspect.getframeinfo(cur_frame)
            # 获取当前帧的目录
            if frame_info.function == '<module>':
                curr_dir = frame_info.filename
            else:
                curr_dir = os.path.dirname(frame_info.filename)
            # 记录文件名和行号
            trace_stack.append(
                [frame_info.filename, frame_info.lineno, frame_info.function])
            # 跳出
            if entry_dir == curr_dir or frame_info.function == '<module>':
                isSkip = True
            else:
                # 记录当前帧
                pre_frame = cur_frame
                # 向前追溯
                cur_frame = cur_frame.f_back
        return trace_stack

    # 打印追踪信息
    def print_traceback(self, color='red', font_color='white', cur_frame=None):
        # 获取当前帧对象
        cur_frame = cur_frame or inspect.currentframe().f_back
        # 获取追踪记录
        trace_stack = self.traceback(cur_frame)
        # 前一条记录
        pre_record = [None, None, None]
        # 层级列表
        tiers = []
        # 竖线
        verticalLine = chalk.white("", background='red')
        title = Chalk(font_color)("Exception", background=color)
        print(f'{verticalLine}{title}')
        for index in range(len(trace_stack)):
            record = trace_stack[index]
            if index == 0:
                content = Chalk(color)(
                    f" - {record[0]}({record[1]}) -> {record[2]}")
                print(f'{verticalLine}{content}')
            else:
                # 不在同一个文件中
                if pre_record[0] != record[0]:
                    if index > 1:
                        # 缩进
                        tiers.append('')
                    content = Chalk(color)(
                        f'{"".join(tiers)} - {record[0]}({record[1]}) -> {record[2]}')
                    print(f'{verticalLine}{content}')
                else:
                    content = Chalk(color)(
                        f'{"".join(tiers)}   {record[0]}({record[1]}) -> {record[2]}')
                    print(f'{verticalLine}{content}')
            # 记录上一个
            pre_record = record
