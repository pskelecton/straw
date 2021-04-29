-- 通过@model标记sql段落，``符号中的内容对应被@sql绑定该文件的同名函数
@model`AddClient`
-- 新增CLIENT
INSERT INTO CLIENT(USERID,PHONE) VALUES (:USERID,:PHONE);

@model`SearchClient`
-- 查询CLIENT数据
SELECT ID,USERID,PHONE FROM CLIENT WHERE USERID > :MINID;

@model`SearchUser`
-- 查询USER数据
SELECT * FROM USER WHERE NAME = :NAME AND ID > :MINID;