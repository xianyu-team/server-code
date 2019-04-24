from django.contrib import admin
from user.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_phone', 'user_balance')

admin.site.register(User, UserAdmin)