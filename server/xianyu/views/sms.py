"""
API文档的手机短信sms部分
"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json

from xianyu import models

__ok__ = {
    'code': 200,
    'message': 'OK'
}
__error__ = {
    'code': 400,
    'message': '服务器发生错误'
}

__notExistUser__ = {
    'code': 400,
    'message': '用户名不存在'
}

__hasExistUser__ = {
    'code': 400,
    'message': '该手机号已经被注册'
}

__wrongPassword__ = {
    'code': 400,
    'message': '密码错误'
}

__notLogin__ = {
    'code': 401,
    'message': '未登录'
}

# 增加装饰器，跳过csrf的保护，前端请求就不会被forbidden
# 或者在前端做csrf保护请求方式
@csrf_exempt
def sms_verification_code(request):
    """获取手机验证码"""
    pass


@csrf_exempt
def sms_verification(request):
    """验证手机验证码"""
    pass
