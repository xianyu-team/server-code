from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json

from user import models

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

# 增加装饰器，跳过csrf的保护，前端请求就不会被forbidden
# 或者在前端做csrf保护请求方式
@csrf_exempt
def user(request):
    if request.method == 'POST':
        try:
            parameters = request.POST
            # 先检查手机号是否唯一
            filter_user = models.User.objects.filter(user_phone=parameters['user_phone'])
            if filter_user.__len__() == 0:
                new_user = models.User(
                    user_phone=parameters['user_phone'],
                    user_password=parameters['user_password']
                )
                new_user.save()
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            else:
                __error__['message'] = '该手机号已经被注册'
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
        except Exception as exc:
            print(exc)
            return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_password_session(request):
    if request.session.get('login', none):
        if request.method == 'POST':
            filter_user = User.objects.get(user_phone=request.POST.user_phone)
            if filter_user.user_password == request.POST.user_password:
                request.session['user_id'] = filter_user.id 
                request.session['user_login'] = true
                __ok__['user_fillin'] = filter_user.user_fillln
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            else: 
                __error__['message'] = '用户名或密码错误'
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(notLogin), content_type='application/json', charset='utf-8')

@csrf_exempt
def user_password(request):
    if request.session.get('login', none):
        if request.method == 'POST':
            try:
                filter_user = User.objects.get(id = request.session.get('user_id'))
                filter_user.user_phone = request.POST.user_phone
                filter_user.user_password = request.POST.user_password
                filter_user.save()
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(notLogin), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_session(request):
    if request.session.get('login', none):
        if request.method == 'DELETE':
            try:
                del request.session['username_id']
                del request.session['login']
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(notLogin), content_type='application/json', charset='utf-8')



@csrf_exempt
def user_order(request):
    if request.session.get('login', none):
        if request.method == 'GET':
            if request.GET.type == 0:
                filter_publishOrder = PublishOrder.objects.get(id = request.session.get('user_id'))
                order = []
                for i in filter_publishOrder:
                    filter_order = Order.objects.get(id = request.session.get('i.order_id'))
                    order.append(filter_order)
                __ok__['order'] = order
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            elif request.GET.type == 1:
                filter_pickOrder = PickOrder.objects.get(id = request.session.get('user_id'))
                order = []
                for i in filter_pickOrder:
                    filter_order = Order.objects.get(id = request.session.get('i.order_id'))
                    order.append(filter_order)
                __ok__['order'] = order
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(notLogin), content_type='application/json', charset='utf-8')