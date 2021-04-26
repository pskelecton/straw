from __future__ import absolute_import
import sys,os
# from ptest.test_db_create.main import *

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            dirOmit = [
                '__pycache__',
                '__init__.py'
            ]
            testCases = list(filter(lambda path:path not in dirOmit,os.listdir('./ptest')))
            for case in testCases:
                job = f'from ptest.{case}.main import *'
                print('Job-->',job)
                exec(job)
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h' or sys.argv[1] == '--h' or sys.argv[1] == '-?' or sys.argv[1] == '--?':
            print('''
                # 批量测试
                python test.py --all
                # 测试test_db_create
                python test.py test_db_create
            ''')
        else:
            job = f'from ptest.{sys.argv[1]}.main import *'
            print('Job-->',job)
            exec(job)