from django.db import models

# Create your models here.

#用户
class User(models.Model):
    #用户ID是mysql自动生成的
    user_phone = models.CharField(max_length=11)
    user_password = models.CharField(max_length=20)
    user_icon = models.BinaryField(default=None, null=True)
    user_balance = models.FloatField(default=0.0)
    user_fillln = models.SmallIntegerField(default=0)
    