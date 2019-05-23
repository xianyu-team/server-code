from django.db import models
from django.utils import timezone


#用户
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_phone = models.CharField(max_length=11)
    user_password = models.CharField(max_length=20)
    user_icon = models.BinaryField(default=None, null=True)
    user_balance = models.IntegerField(default=100)
    user_fillln = models.SmallIntegerField(default=0)


#学生
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    student_number = models.CharField(max_length=20)
    student_name = models.CharField(max_length=20)
    student_university = models.CharField(max_length=50)
    student_academy = models.CharField(max_length=50)
    student_gender = models.SmallIntegerField(default=0)


#用户关注的对象
class Following(models.Model):
    user_id = models.IntegerField()
    following_id = models.IntegerField()


#关注用户的对象
class Fan(models.Model):
    user_id = models.IntegerField()
    fan_id = models.IntegerField()


#开支帐单
class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    bill_type = models.SmallIntegerField(default=0)     #0代表收入, 1代表支出
    bill_number = models.IntegerField(default=0)
    bill_description = models.CharField(max_length=100)
    bill_time = models.DateTimeField(auto_now_add=True) #格式为YYYY-MM-DD HH:MM:SS


#用户发布的任务
class PublishTask(models.Model):
    user_id = models.IntegerField()
    task_id = models.IntegerField()


#用户接取的任务
class PickTask(models.Model):
    user_id = models.IntegerField()
    task_id = models.IntegerField()


#任务
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()                    # 任务发布者的ID
    task_type = models.SmallIntegerField(default=0)    #0代表递送, 1代表问卷
    task_sketch = models.CharField(max_length=100)
    task_bonus = models.IntegerField()
    task_publishDate = models.DateTimeField(auto_now_add=True)   #格式为YYYY-MM-DD HH:MM:SS


#递送
class Delivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    task_id = models.IntegerField()
    delivery_detail = models.CharField(max_length=100)
    delivery_picked = models.SmallIntegerField(default=0)    #0代表未接取, 1代表接取
    delivery_complished = models.SmallIntegerField(default=0)    #0代表未完成, 1代表完成
    delivery_complishDate = models.DateTimeField(default=timezone.now)


#问卷
class Questionnaire(models.Model):
    questionnaire_id = models.AutoField(primary_key=True)
    task_id = models.IntegerField()
    questionnaire_closed = models.SmallIntegerField(default=0)      #0代表未截止, 1代表截止
    questionnaire_deadline = models.DateTimeField(default=timezone.now)                 #格式为YYYY-MM-DD HH:MM:SS
    questionnaire_number = models.IntegerField(default=0)


#题目
class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    questionnaire_id = models.IntegerField()
    question_description = models.CharField(max_length=100)
    question_type = models.SmallIntegerField(default=0)     #0代表单选, 1代表多选, 2代表填空
    question_a = models.CharField(max_length=100)
    question_b = models.CharField(max_length=100)
    question_c = models.CharField(max_length=100)
    question_d = models.CharField(max_length=100)


#答卷
class AnswerSheet(models.Model):
    answerSheet_id = models.AutoField(primary_key=True)
    questionnaire_id = models.IntegerField()
    user_id = models.IntegerField()


#答案
class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    answerSheet_id = models.IntegerField()
    question_id = models.IntegerField()
    answer_content = models.CharField(max_length=100)
