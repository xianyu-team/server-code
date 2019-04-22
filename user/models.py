from django.db import models

# Create your models here.

class User(models.Model):
    user_phone = models.CharField(max_length=11)
    user_password = models.CharField(max_length=20)