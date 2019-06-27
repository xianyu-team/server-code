# server-code
使用python后端框架Django搭建服务器

## 服务器系统环境
- 阿里云 Ubuntu 16.04 LTS Server

## 安装方法
以下操作在ubuntu16.04系统的服务器下进行

- 前往[python官网](https://www.python.org/downloads/)安装python3.5以上的版本
- 用`pip3 install django`安装django2.2
- 前往[mysql官网](https://www.mysql.com/downloads/)安装mysql-8.0.15
- 用`pip3 install PyMySQL`安装 PyMySQL 操作数据库
- 用`pip3 install mysqlclient`安装mysqlclient操作数据库
- 用`sudo apt-get install redis-server`安装 redis-server
- 用`pip3 install django_redis`安装 django 操作 redis 的库


## 运行方法

- 用`service mysql start`开启 mysql 数据库服务，然后用命令`mysql –u root –p`登录mysql终端，用户名和密码为安装msyql时创建的，并新建一个名为 `xianyu` 的 database
- 启动 redis-server 服务，window 下进入 redis 安装目录，执行命令为`redis-server.exe redis.windows.conf`，ubuntu 安装 redis 后，可直接执行命令`redis-server`
- 进入 server 文件夹执行`python manage.py runserver 0.0.0.0:8000`


## MySQL

* 用户名: root
* 密码: 123456
* 数据库名: xianyu_db



## admin超级用户
Django admin管理工具的超级用户为：
- 用户名：root
- 密码：123456
