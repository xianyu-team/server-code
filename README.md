# server-code
使用python后端框架Django搭建服务器



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

1. 在urls.py和setting.py中设置了URL尾部不加斜杠'/'
2. 在view.py中增加装饰器@csrf_exempt，跳过csrf的保护，前端请求就不会被forbidden

