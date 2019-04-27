from django.db import models

#帐单
class Bill(models.Model):
    user_id = models.ForeignKey('user.User',on_delete=models.CASCADE)
    bill_type = models.SmallIntegerField(default=0)     #0代表收入, 1代表支出
    bill_number = models.IntegerField(default=0)
    bill_description = models.CharField(max_length=100)
    bill_time = models.DateTimeField()