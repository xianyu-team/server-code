from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json

from user import models
from balance import models

# Create your views here.

__ok__ = {
    'code': 200,
    'message': 'OK'
}
__error__ = {
    'code': 400,
    'message': '服务器发生错误'
}

_notLogin_ = {
    'code': 401,
    'message': '未登录'
}

@csrf_exempt
def balance(request):
    if request.session.get('login', none):
        if request.method == 'GET':
            try:
                filter_user = models.User.objects.filter(id = request.session.get('user_id'))
                __ok__['user_balance'] = filter_user.filter_user
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(notLogin), content_type='application/json', charset='utf-8')


@csrf_exempt
def balance_bill(request):
    if request.session.get('login', none):
        if request.method == 'GET':
            try:
                filter_bills = models.Bill.objects.filter(user_id = request.session.get('user_id'))
                __ok__['bills'] = filter_bills.bills
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(notLogin), content_type='application/json', charset='utf-8')