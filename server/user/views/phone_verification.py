from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json

# Create your views here.

__ok__ = {
    'code': 200,
    'message': 'OK'
}
__error__ = {
    'code': 400,
    'message': '服务器发生错误'
}

# 增加装饰器，跳过csrf的保护，前端请求就不会被forbidden
# 或者在前端做csrf保护请求方式
@csrf_exempt
def user_phone_verification(request):
    return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
