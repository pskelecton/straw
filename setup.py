#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

long_description = '''
============
Straw 数据管
============

.. image:: https://img.shields.io/badge/Beta-0.9.x-yellow
.. image:: https://img.shields.io/badge/License-MIT-green
.. image:: https://img.shields.io/badge/Python-%3E%3D%203.7-blue
.. image:: https://img.shields.io/badge/SQL%40Support-postgres%20%7C%20mysql-lightgrey

**简单的函数调用来处理数据库**

*Straw可以方便的在多个不同的数据库之间传输数据，只需要调用一个方法把数据取出来，再调用一个方法把数据插到另一个数据库中
他可以像MyBatis一样，分离sql层和逻辑层，但又不同于MyBatis的是你可以在脚本中使用它，你还可以同时连接多个数据库
如果你只想写一个简单的脚本，把爬到的数据插到数据中，Straw会非常简单*

`[How to start] <https://github.com/pskelecton/straw>`_

**MIT License**

*Copyright (c) 2021 Chalk Yu (Straw)*

*Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.*

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*
'''

# import os
# dir = os.path.dirname(os.path.abspath(__file__))
# with open(os.path.join(dir,'readme.rst'),encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='pstraw',
    version='0.9.7',
    description=('简单的函数调用来处理数据库'),
    long_description=long_description,
    author='Chalk Yu',
    author_email='yuequn3721@qq.com',
    maintainer='Chalk Yu',
    maintainer_email='yuequn3721@qq.com',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    url='https://github.com/pskelecton/straw',
    install_requires=[
        "sqlalchemy==1.3.22",
        "sqlparse==0.4.1",
        "pychalk==2.0.1",
        "promise==2.3",
        "psycopg2==2.8.6",
        "pymysql==0.9.3"
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ],
)
