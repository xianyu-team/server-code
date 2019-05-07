"""
API文档的手机短信sms部分
"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
import time
import hashlib
import uuid
import requests

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

__failedSendVerification__ = {
    'code': 400,
    'message': '验证码发送失败'
}

__wrongVerification__ = {
    'code': 400,
    'message': '验证码验证失败'
}

__notLogin__ = {
    'code': 401,
    'message': '未登录'
}


# 增加装饰器，跳过csrf的保护，前端请求就不会被forbidden
# 或者在前端做csrf保护请求方式

xianyu_app_secret = '940441f4e010'
xianyu_AppKey: '7a2d8351ad47c6310468f01ca4d18c5e'

@csrf_exempt
def sms_verification_code(request):
    """向手机发送验证码"""
    try:
        if request.method == 'GET':
            parameters = request.GET

            sms_url = 'https://api.netease.im/sms/sendcode.action'
            post_data = {
                'mobile': parameters['user_phone'],
                'templateid': 9734879
            }

            # 以下是网易云官网要求的headers
            cur_time = str(time.time())
            app_secret = xianyu_app_secret
            nonce = str(uuid.uuid4())

            # 参数拼接
            post_param = app_secret + nonce + cur_time
            # 哈希加密
            check_sum = hashlib.new('sha1', post_param.encode('utf-8')).hexdigest()

            headers = {
                'AppKey': xianyu_AppKey,
                'Nonce': nonce,
                'CurTime': cur_time,
                'CheckSum': check_sum
            }

            response = requests.post(sms_url, data=post_data, headers=headers)

            if response['code'] == 200:
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            else:
                return HttpResponse(json.dumps(__failedSendVerification__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def sms_verification(request):
    """验证手机验证码"""
    try:
        if request.method == 'POST':
            parameters = request.POST

            sms_url = 'https://api.netease.im/sms/verifycode.action'
            post_data = {
                'mobile': parameters['user_phone'],
                'code': parameters['verification_code']
            }

            # 以下是网易云官网要求的headers
            cur_time = str(time.time())
            app_secret = xianyu_app_secret
            nonce = str(uuid.uuid4())

            # 参数拼接
            post_param = app_secret + nonce + cur_time
            # 哈希加密
            check_sum = hashlib.new('sha1', post_param.encode('utf-8')).hexdigest()

            headers = {
                'AppKey': xianyu_AppKey,
                'Nonce': nonce,
                'CurTime': cur_time,
                'CheckSum': check_sum
            }

            response = requests.post(sms_url, data=post_data, headers=headers)

            if response['code'] == 200:
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            else:
                return HttpResponse(json.dumps(__wrongVerification__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')