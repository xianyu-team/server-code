from django.urls import path, include

from .views import balance

urlpatterns = [
    path('', balance.balance),
    path('/bill', balance.balance_bill),
]
