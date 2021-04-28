from __future__ import absolute_import
import sys,os
# from ptest.test_db_create.main import *

def printHelp():
    print('''
 +-----------------------------------
 |
 | (1) 批量测试
 |
 |    >> python test.py --all
 |
 | (2) 初始化数据库
 |
 |    >> python test.py --init
 |
 | (3) 测试文件
 |
 |    >> python test.py test_db_create
 |    >> python test.py db_create
 |
 | (4) 还原数据库后测试
 |
 |    >> python test.py --clear test_db_create
 |    >> python test.py --clear db_create
 |
 +-----------------------------------
''')

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            if sys.argv[1] == '--all' or sys.argv[1] == '-a':
                dirOmit = [
                    '__pycache__',
                    '__init__.py'
                ]
                testCases = list(filter(lambda path:path not in dirOmit,os.listdir('./ptest')))
                for case in testCases:
                    if case != "test_db_create":
                        # 还原数据库
                        from ptest.test_db_create.main import *
                        # 运行脚本
                        job = f'from ptest.{case}.main import *'
                        print('Job-->',job)
                        exec(job)
            elif sys.argv[1] == '--help' or sys.argv[1] == '-h' or sys.argv[1] == '-?':
                printHelp()
            else:
                # 运行脚本
                job = f'from ptest.{sys.argv[1]}.main import *'
                print('Job-->',job)
                exec(job)
        elif len(sys.argv) == 3 and (sys.argv[1] == '--clear' or sys.argv[1] == '-c'):
            # 还原数据库
            from ptest.test_db_create.main import *
            # 运行脚本
            job = f'from ptest.{sys.argv[2]}.main import *'
            print('Job-->',job)
            exec(job)
        elif len(sys.argv) == 3 and (sys.argv[2] == '--clear' or sys.argv[2] == '-c'):
            # 还原数据库
            from ptest.test_db_create.main import *
            # 运行脚本
            job = f'from ptest.{sys.argv[1]}.main import *'
            print('Job-->',job)
            exec(job)
        else:
            printHelp()