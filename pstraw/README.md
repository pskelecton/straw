# 文档说明

### 目录结构
```
|-- _straw
|    |-- __init__.py
|    |-- loader
|    |    |-- __init__.py
|    |    |-- extends.py
|    |    |-- ibm_db_dbi.py
|    |    |-- psycopg.py
|    |    |-- pymysql.py
|    |    |-- sqlalchemy.py
|    |-- bean_factory.py
|    |-- db_guide.py (入口)
|    |-- frame_guide.py
|    |-- definition.py
|    |-- orm_factory.py
|    |-- output_console.py
|    |-- screws.py
|    |-- tool.py
```

### 模块说明
> #### db_guide.py
> 入口模块, 包含主类的定义, 装饰器的定义

> #### frame_guide.py
> 框架模块, 全局接口定义, 文件查询和调度

> #### definition.py
> 定义模块, 初始化缓存, 指定缺省值

> #### logger_factory.py
> 日志输出和异常打印模块

> #### screws.py
> 零部件模块, 路径解析类, 字典转换类, 缓存生成类

> #### tool.py
> 工具模块, 字符串转布尔, 字符串转数值

> #### orm_factory.py
> orm工厂, orm动态加载器, 动态构造器, orm类型引用

> #### bean_factory.py
> bean工厂, bean动态加载器, 动态构造器, bean类型引用

> #### loader/???.py
> orm插件加载单元, 包含各类orm的加载类, 动态直接加载

> #### loader/extends.py
> orm插件加载器接口, sql模板转换类

> #### resource_factory.py
> 资源工厂, 对资源读取与缓存的统一处理

### 待完成项目
> 1. 异常处理, 包括路径不存在, 文件不存在, 需要抛出正确错误信息
> 2. 一次缓存重复调用, 需要全局找可复用缓存
> 3. sqlalchemy的loader
> 4. bean工具扩展
> 5. 连接池, db可重复连接
> 6. 多db连携,多配置文件
> 7. 初始执行生成模板案例
> 8. 多db类型支持, loader扩展化
> 9. sql文件通过标记映射方法，通过sql注解参数来指定sql文件名
> 10. DB类型反射python语言类型，比如说datetime类型对应python的str方式解析
> 11. 垃圾回收以及效率优化
> 12. ssl功能追加
> 13. entry注解通过闭包保存状态，并缓存下次直接获取
> 14. sql生成器

### 大功能
> 1. 动态sql与模板引擎（外部插件）
> 2. 核心与插件化分离
> 3. 非关系型数据库对接
> 4. 外部执行语言对接（java、js、shell、cmd、c）

### 测试问题一览（待解决）
> 1. @sql注解函数中的返回值，如果为list，则做多个sql的合并后再执行（增加效率），只作用于增、改、删
> 2. 识别字符串、数值、日期、布尔、字节等类型，自动拼接单引号''
> 3. TRACK_SQL_FILE = True的情况下，可以允许手动通过路径匹配sql文件
> 4. sql类型新增Truncate等
> 5. bean继承的数组支持数组运算
> 6. 异常文件追踪，从发生问题的文件上一个文件开始，应该是从发生问题的文件开始
> 7. @sql注解和全局参数，新增allow_mutisql参数
> 8. 文件读取逻辑移动到外层db_guide中，而接口的loader中可以直接拿到字符串
> 9. psycopg和pymysq需要修正
> 10. 文件夹层级比较深，但内容都没什么用的情况不需要深度遍历，或者选择性遍历
> 11. 初始化控制，LOG_ON=False的时候，不需要自动生成文件夹
> 12. 重构logger_factory模块，分离logger和错误追踪处理


### 说明：
> 1. connection注解不能嵌套使用，非connection注解函数可以调用connection注解函数，反之也可
> 2. allow_mutisql = True的时候，返回的cursor是list类型，False时返回的cursor是单个对象
> 3. sql文件以及数据库缓存，在入口注解中添加，如果没有入口注解，则不作缓存
> 4. 关于factory类，是不嵌入到主类中的，都是单独开辟一块引用处理逻辑（不被主类继承）

### 记事：
> 1. 参考标准库 https://docs.python.org/zh-cn/3.7/library/index.html，调查扩展与优化

### 发布：
```linux
# 安装上传工具
pip install twine
# 打包
python setup.py sdist build
# 上传
# python setup.py sdist upload
twine upload dist/*
```

 - pip查看版本
```
pip show pstraw
```

 - pip安装
```
pip install pstraw
```

 - git打标签
```
git tag v0.9.3
git push origin v0.9.3
```

### 工作日程
- API文档整理
- Pypi说明文档，readme.rst
- MIT License
- Example文档整理
- readme介绍主页
- Gitpage主页搭建

### 多编程语言支持
- js/ts
- go
- julia
- rust