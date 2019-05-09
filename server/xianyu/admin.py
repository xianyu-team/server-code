from django.contrib import admin
from . import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_phone', 'user_password', 'user_icon', 'user_balance', 'user_fillln')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user_id', 'student_number', 'student_name', 'student_university', 'student_academy', 'student_gender')

class FollowingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'following_id')

class FanAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'fan_id')

class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'user_id', 'bill_type', 'bill_number', 'bill_description', 'bill_time')

class PublishTaskAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'task_id')

class PickTaskAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'task_id')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'user_id', 'task_type', 'task_sketch', 'task_bonus', 'task_publishDate')

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_id', 'task_id', 'delivery_detail', 'delivery_picked', 'delivery_complished', 'delivery_complishDate')

class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('questionnaire_id', 'task_id', 'questionnaire_closed', 'questionnaire_deadline', 'questionnaire_number')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'questionnaire_id', 'question_description', 'question_type', 'question_a', 'question_b', 'question_c', 'question_d')

class AnswerSheetAdmin(admin.ModelAdmin):
    list_display = ('answerSheet_id', 'questionnaire_id', 'user_id')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_id', 'answerSheet_id', 'question_id', 'answer_content')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Following, FollowingAdmin)
admin.site.register(models.Fan, FanAdmin)
admin.site.register(models.Bill, BillAdmin)
admin.site.register(models.PublishTask, PublishTaskAdmin)
admin.site.register(models.PickTask, PickTaskAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Delivery, DeliveryAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.AnswerSheet, AnswerSheetAdmin)
admin.site.register(models.Answer, AnswerAdmin)