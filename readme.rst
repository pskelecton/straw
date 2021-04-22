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

快速开始
---------
- 运行环境

 .. image:: https://img.shields.io/badge/Python-%3E%3D%203.7-blue

- 安装

  .. code-block:: shell
    :linenos:

    # 安装straw库
    pip install pstraw

- 快速使用

  .. code-block:: python
    :linenos:

      from pstraw import Straw
      # 实例化straw对象
      db = Straw(
          DB_DRIVER='mysql',
          DB_DATABASE='demo_db',
          DB_USER='root',
          DB_PASSWORD='root'
      )
      # 创建一个结构体，用于保存数据对象
      @dataclass
      class USER_TABLE():
          ID: int
          USER: str
          PASSWORD: str
          CREATE_TIME:datetime
          CREATE_BY: str
          UPDATE_TIME:datetime
          UPDATE_BY: str
      # 绑定一条sql语句，函数的返回值为sql中的参数映射
      @db.sql(USER_TABLE,SQL='SELECT * FROM USER_TABLE WHERE USER = :USER')
      def SearchUser(user:str):
          return {'USER':user}
      # 通过注解创建一个链接
      @db.conn()
      def ExecSQL():
          # 调用函数来执行sql，函数调用的返回值res为sql查询的结果
          res:list(USER_TABLE) = SearchUser('Chalk Yu')
          for userStore in res:
              print(f'ID={userStore.ID}',f'USER={userStore.USER}',f'PASSWORD={userStore.PASSWORD}')

      if __name__ == '__main__':
          ExecSQL()
