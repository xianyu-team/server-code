# server-code
使用python后端框架Django搭建服务器

## 安装方法
以下操作在ubuntu16.04系统的服务器下进行

- 安装python3.5以上的版本
- 用`pip3 install django`安装django2.2
- 安装mysql-8.0.15
- 用`pip3 install PyMySQL`安装PyMySQL操作数据库
- 安装mysqlclient操作数据库

## MySQL

* 用户名: root
* 密码: 123456
* 数据库名: xianyu_db



## admin超级用户
Django admin管理工具的超级用户为：
- 用户名：root
- 密码：123456





## 开发日志
- 2019-04-23

1. 在urls.py和setting.py中设置了URL尾部不加斜杠'/',即不能用/admin/访问，而是用/admin
2. 在view.py中增加装饰器@csrf_exempt，跳过csrf的保护，前端请求就不会被forbidden


