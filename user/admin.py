from django.contrib import admin
from . import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_phone',)

admin.site.register(models.User, UserAdmin)