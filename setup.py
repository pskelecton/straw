#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='pstraw',
    version='0.9.1',
    description=('函数调用的方式操作数据库'),
    long_description=open('README.md').read(),
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
        "promise==2.3"
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
)
