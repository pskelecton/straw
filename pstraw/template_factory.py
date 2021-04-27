#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# ========================================
# Description :
#    模板工厂
#    解析模板指令
# Created : 2021.04.22
# Author : Chalk Yu
# ========================================
from functools import reduce
import re
from .screws import Store
'''
@model``
@receive``
@execute``
@repeat``
'''


class TemplateFactory():
    def __init__(self):
        self.keywords = [
            'model',
            'receive',
            'execute',
            'repeat'
        ]

    def composition(self, strContent, keywordIndex):
        expIdxArr = []
        # 表达式不存在
        if not self.keywords[keywordIndex]:
            return ([strContent], [])
        partern = re.compile(f'\@{self.keywords[keywordIndex]}\s*\`[^\`]*\`')
        expArr = partern.findall(strContent)  # 表达式数组
        expSpl = partern.split(strContent)  # 被表达式分割的字符串数组
        # 匹配不到表达式
        if len(expArr) == 0:
            return ([strContent], [])
        return (expArr, expSpl)

    # 碎片化

    def fragmentization(self, strContent, keywordIndex=0):
        expArr, expSpl = self.composition(strContent, keywordIndex)
        if len(expSpl) == 0:
            return expArr
        self.expCur = 0  # 表达式数组当前指针

        def callback(target, current):
            resArr = []
            if(type(target) == str):
                resArr = self.fragmentization(
                    target, keywordIndex+1) + [expArr[self.expCur]] + self.fragmentization(current, keywordIndex+1)
            else:
                resArr = target + [expArr[self.expCur]] + \
                    self.fragmentization(current, keywordIndex+1)
            self.expCur = self.expCur + 1
            return resArr
        return reduce(callback, expSpl)

    # 从指令函数中，拆解指令参数，如： @model`User` => User
    def getArg(self, strExp, directName):
        if f'@{directName}' in strExp and strExp.strip().index(f'@{directName}') == 0:
            arg = strExp.replace(f'@{directName}', '').strip()
            return arg[1:-1]

    # 判断是否是某个指令
    def checkIsDirective(self, strExp, directName):
        if f'@{directName}' in strExp and strExp.strip().index(f'@{directName}') == 0:
            arg = strExp.replace(f'@{directName}', '').strip()
            if arg[0] == '`' and arg[-1] == '`':
                return True
            else:
                return False
        else:
            return False

    '''
        @model指令，用于给长sql语句分段，如：
        
        -- 这条sql的模块名是user
        @model`user`
        select * from user;
        -- 这条sql的模块名是address
        @model`address`
        select * from address;
    '''

    def Model(self, fullSql):
        sqlChips = Store()
        sectionName = None
        sqlLines = fullSql.split('\n')
        for sqlLine in sqlLines:
            # 数据如： ['   ', '@model`user`', '   ']
            # fraArr = self.fragmentization(sqlLine)
            # if len(fraArr) == 3 and fraArr[0].strip() == "" and self.checkIsDirective(fraArr[1], 'model') and fraArr[2].strip() == "":
            # directive = fraArr[1]
            fraArr, splitStr = self.composition(sqlLine, 0)
            if len(splitStr) > 0 and ''.join(splitStr).strip() == "":
                directive = fraArr[0]
                sectionName = self.getArg(directive, 'model').strip()
                sqlChips[sectionName] = ""
            else:
                if sectionName != None:
                    sqlChips[sectionName] = sqlChips[sectionName] + \
                        '\n' + sqlLine
                    sqlChips[sectionName] = sqlChips[sectionName].strip()
        return sqlChips


templatePaser = TemplateFactory()
