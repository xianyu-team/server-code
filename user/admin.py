from django.contrib import admin
from . import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_phone', 'user_balance', 'user_nearLogin')

admin.site.register(models.User, UserAdmin)