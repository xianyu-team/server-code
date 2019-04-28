from django.db import models

# Create your models here.

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