# server-code
使用python后端框架Django搭建服务器

## 安装方法
以下操作在ubuntu16.04系统的服务器下进行

- 安装python3.5以上的版本
- 用`pip3 install django`安装django2.2
- 安装mysql-8.0.15
- 用`pip3 install PyMySQL`安装PyMySQL操作数据库
- 安装mysqlclient操作数据库
- 前往 redis 官网下载 redis-server 并安装
- 用`pip3 install django_redis`安装 django 操作 redis 的库


## 运行方法

- 开启 mysql 数据库服务并新建一个名为 xianyu 的 database
- 启动 redis-server 服务
- 进入 server 文件夹执行`python manage.py runserver 0.0.0.0:8000`


## MySQL

* 用户名: root
* 密码: 123456
* 数据库名: xianyu_db



## admin超级用户
Django admin管理工具的超级用户为：
- 用户名：root
- 密码：123456
