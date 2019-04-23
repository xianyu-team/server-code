from django.db import models

# Create your models here.

#用户
class User(models.Model):
    #用户ID是mysql自动生成的
    user_phone = models.CharField(max_length=11)
    user_password = models.CharField(max_length=20)
    user_icon = models.BinaryField(default=None, null=True)
    user_balance = models.FloatField(default=0.0)
    user_nearLogin = models.SmallIntegerField(default=0)    #0代表最近7天没登陆，1为最近7天有登录
    