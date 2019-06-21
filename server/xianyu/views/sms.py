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
import string
import random

from xianyu import models

# 注意data字段，因为__ok__是全局变量，所以每次返回时都要对data进行赋值，以覆盖原来的data值
__ok__ = {
    'code': 200,
    'message': 'OK',
    'data': {}
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
@csrf_exempt
def sms_verification_code(request, user_phone):
    """没有用第三方短信服务，后端模拟向手机发送验证码"""
    try:
        if request.method == 'GET':
            # 产生 4 位随机数
            seeds = string.digits
            random_str = []
            for i in range(4):
                random_str.append(random.choice(seeds))
            verification_code = "".join(random_str)

            request.session[user_phone + '_verification_code'] = verification_code
            request.session[user_phone + '_get_verification_code_time'] = time.time()

            __ok__['data'] = {
                'verification_code': verification_code
            }
            return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def sms_verification(request):
    """没有用第三方短信服务，后端模拟验证手机验证码"""
    try:
        if request.method == 'POST':
            parameters = json.loads(request.body.decode('utf-8'))

            user_phone = parameters['user_phone']
            verification_code = parameters['verification_code']

            current_time = time.time()
            get_verification_code_time = request.session.get(user_phone + '_get_verification_code_time', 0)

            if current_time - get_verification_code_time < 600:
                if verification_code == request.session.get(user_phone + '_verification_code', '-1'):
                    data = {}
                    __ok__['data'] = data

                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
                else:
                    return HttpResponse(json.dumps(__wrongVerification__), content_type='application/json', charset='utf-8')
            else:
                return HttpResponse(json.dumps(__wrongVerification__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


'''
@csrf_exempt
def sms_verification_code(request, user_phone):
    """向手机发送验证码"""
    try:
        if request.method == 'GET':
            sms_url = 'https://api.netease.im/sms/sendcode.action'
            post_data = {
                'mobile': user_phone,
                'templateid': 9734879
            }

            # 以下是网易云官网要求的headers
            cur_time = str(time.time())
            app_secret = '940441f4e010'
            nonce = str(uuid.uuid4())

            # 参数拼接
            post_param = app_secret + nonce + cur_time
            # 哈希加密
            check_sum = hashlib.new('sha1', post_param.encode('utf-8')).hexdigest()

            headers = {
                'AppKey': '7a2d8351ad47c6310468f01ca4d18c5e',
                'Nonce': nonce,
                'CurTime': cur_time,
                'CheckSum': check_sum
            }

            response = requests.post(sms_url, data=post_data, headers=headers)
            response_data = response.json()

            if response_data['code'] == 200:
                data = {}
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            else:
                return HttpResponse(json.dumps(__failedSendVerification__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
'''


'''
@csrf_exempt
def sms_verification(request):
    """验证手机验证码"""
    try:
        if request.method == 'POST':
            parameters = json.loads(request.body.decode('utf-8'))

            sms_url = 'https://api.netease.im/sms/verifycode.action'
            post_data = {
                'mobile': parameters['user_phone'],
                'code': parameters['verification_code']
            }

            # 以下是网易云官网要求的headers
            cur_time = str(time.time())
            app_secret = '940441f4e010'
            nonce = str(uuid.uuid4())

            # 参数拼接
            post_param = app_secret + nonce + cur_time
            # 哈希加密
            check_sum = hashlib.new('sha1', post_param.encode('utf-8')).hexdigest()

            headers = {
                'AppKey': '7a2d8351ad47c6310468f01ca4d18c5e',
                'Nonce': nonce,
                'CurTime': cur_time,
                'CheckSum': check_sum
            }

            response = requests.post(sms_url, data=post_data, headers=headers)
            response_data = response.json()

            if response_data['code'] == 200:
                data = {}
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            else:
                return HttpResponse(json.dumps(__wrongVerification__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
'''
