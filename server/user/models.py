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


#学生
class Student(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    student_number = models.IntegerField()
    student_name = models.CharField(max_length=20)
    student_university = models.CharField(max_length=50) 
    student_academy = models.CharField(max_length=50)
    student_gender = models.SmallIntegerField(default=0)


#用户发布订单
class PublishOrder(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    order_id = models.ForeignKey('order.Order',on_delete=models.CASCADE)


#用户接取订单
class PickOrder(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    order_id = models.ForeignKey('order.Order',on_delete=models.CASCADE)


#用户关注对象
class Followings(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    folloings_id = models.IntegerField()


#关注用户对象
class Fans(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    fans_id = models.IntegerField()