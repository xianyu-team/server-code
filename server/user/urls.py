from django.urls import path, include

from .views import user
from .views import profile

urlpatterns = [
    path('', user.user),
    path('/profile', profile.profile),
    path('/session', user.user_session),
    path('/password', user.user_password),
    path('/password/session', user.user_password_session),
    path('/order', user.user_order)
]
