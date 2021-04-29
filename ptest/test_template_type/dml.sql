-- 通过@model标记sql段落，``符号中的内容对应被@sql绑定该文件的同名函数
@model`TempType1`
-- SQL_TEMPLATE_TYPE = 1， 通过python字符串的%s占位符替换
SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN %s;

@model`TempType2`
  -- SQL_TEMPLATE_TYPE = 2， 通过参数{0} ~ {n}的形式接收内容
SELECT ID,NAME,{1} FROM USER WHERE {1} IN {0};

@model`TempType3`
-- SQL_TEMPLATE_TYPE = 3， 字典键值匹配
-- 例如  :USERDESC1 匹配@sql注解方法返回值{"USERDESC1":value1,"USERDESC2":value2}中的value1
SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN (:USERDESC1,:USERDESC2);

@model`TempType4`
-- SQL_TEMPLATE_TYPE = 4， 通过python字符串的%s占位符替换
-- 字符串类型，自动填充引号，默认单引号
SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN (%s,%s);

@model`TempType5,quotationType`
  -- SQL_TEMPLATE_TYPE = 5， 通过参数{0} ~ {n}的形式接收内容
-- 字符串类型，自动填充引号，默认单引号
SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN ({0},{1});

@model`TempType6,defaultTempType`
-- SQL_TEMPLATE_TYPE = 6， 字典键值匹配
-- 例如  :USERDESC1 匹配@sql注解方法返回值{"USERDESC1":value1,"USERDESC2":value2}中的value1
-- 字符串类型，自动填充引号，默认单引号
SELECT ID,NAME,USERDESC FROM USER WHERE USERDESC IN (:USERDESC1,:USERDESC2);