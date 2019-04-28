from django.urls import path, include

from .views import order

urlpatterns = [
    path('', order.order),
    path('/pick', order.order_pick),
    path('/complish', order.order_complish),
]
