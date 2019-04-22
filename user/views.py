from django.shortcuts import render

from . import models

# Create your views here.

def user(request):
    user = models.User.objects.get(pk=1)
    return render(request, 'user/test.html', {'user': user})