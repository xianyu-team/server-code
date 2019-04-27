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
    student_sex = models.SmallIntegerField(default=0)


#订单
class Order(models.Model):
    order_type = models.SmallIntegerField(default=0)    #0代表跑腿, 1代表作业辅导
    order_description = models.CharField(max_length=100)
    order_detail = models.CharField(max_length=100)
    order_bonus = models.IntegerField()
    order_publishDate = models.DateTimeField()
    order_picked = models.SmallIntegerField(default=0)    #0代表未接取, 1代表接取
    order_complished = models.SmallIntegerField(default=0)    #0代表未完成, 1代表完成
    order_complishDate = models.DateTimeField()


#用户发布订单
class PublishOrder(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    order_id = models.ForeignKey('Order',on_delete=models.CASCADE)


#用户接取订单
class PickOrder(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    order_id = models.ForeignKey('Order',on_delete=models.CASCADE)
