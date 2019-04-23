from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json

from . import models

# Create your views here.

__ok__ = {
    'code': 200,
    'message': 'OK'
}
__error__ = {
    'code': 400,
    'message': 'ERROR'
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
    elif request.method == 'GET':
        new_user = models.User.objects.get(id=1)
        return render(request, 'user/test.html', {'user': new_user})
    