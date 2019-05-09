from django.contrib import admin
from . import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_phone', 'user_password', 'user_icon', 'user_balance', 'user_fillln')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user_id', 'student_number', 'student_name', 'student_university', 'student_academy', 'student_gender')

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Student, StudentAdmin)