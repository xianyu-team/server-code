"""
API文档的用户user部分
"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from time import strftime, localtime
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

def _verify_phone_code_(user_phone, verification_code):
    """
    此函数为私有函数，作用是验证手机验证码，传入参数为手机号和验证码，返回值为bool值，true为成功验证
    状态码：
        200: 操作成功
        301: 被封禁
        315: IP限制
        403: 非法操作或没有权限
        404: 对象不存在
        413: 验证失败(短信服务)
        414: 参数错误
        500: 服务器内部错误
    这里只验证几个重要的状态码
    """
    sms_url = 'https://api.netease.im/sms/verifycode.action'
    post_data = {
        'mobile': user_phone,
        'code': verification_code
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
        return True
    else:
        return False


@csrf_exempt
def user(request):
    """用户注册"""
    try:
        if request.method == 'POST':
            parameters = request.POST

            # 先检查手机号是否唯一
            # 获取多个对象用filter
            filter_user = models.User.objects.filter(user_phone=parameters['user_phone'])
            if filter_user.__len__() == 0:
                is_verified = _verify_phone_code_(parameters['user_phone'], parameters['verification_code'])

                if is_verified:
                    new_user = models.User(
                        user_phone=parameters['user_phone'],
                        user_password=parameters['user_password']
                    )
                    new_user.save()

                    # session保存用户登录状态
                    request.session['user_id'] = new_user.user_id
                    request.session['user_login'] = True

                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
                else:
                    return HttpResponse(json.dumps(__wrongVerification__), content_type='application/json', charset='utf-8')    
            else:
                return HttpResponse(json.dumps(__hasExistUser__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_profile(request):
    """PUT为完善或修改当前用户信息，GET为获取当前用户信息"""
    try:
        if request.session.get('login', None):
            if request.method == 'PUT':
                parameters = request.PUT

                # 获取单个对象用get
                get_user = models.User.objects.get(user_id=request.session['user_id'])
                get_user.user_icon = parameters['user_icon']
                get_user.save()

                # 学生信息不存在则创建
                get_student = models.Student.objects.get(user_id=request.session['user_id'])
                if get_student is None:
                    new_student = models.Student(
                        user_id=request.session['user_id'],
                        student_number=parameters['student_number'],
                        student_name=parameters['student_name'],
                        student_university=parameters['student_university'],
                        student_academy=parameters['student_academy'],
                        student_gender=parameters['student_gender']
                    )
                    new_student.save()
                else:
                    get_student.user_id = request.session['user_id']
                    get_student.student_number = parameters['student_number']
                    get_student.student_name = parameters['student_name']
                    get_student.student_university = parameters['student_university']
                    get_student.student_academy = parameters['student_academy']
                    get_student.student_gender = parameters['student_gender']
                    get_student.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            elif request.method == 'GET':
                get_user = models.User.objects.get(user_id=request.session['user_id'])
                get_student = models.Student.objects.get(user_id=request.session['user_id'])

                __ok__['user'] = {
                    'user_id': get_user.user_id,
                    'user_phone': get_user.user_phone,
                    'user_icon': get_user.user_icon,
                    'user_balance': get_user.user_balance,
                    'user_fillln': get_user.user_fillln
                }

                __ok__['student'] = {
                    'student_id': get_student.student_id,
                    'user_id': get_student.user_id,
                    'student_number': get_student.student_number,
                    'student_name': get_student.student_name,
                    'student_university': get_student.student_university,
                    'student_academy': get_student.student_academy,
                    'student_gender': get_student.student_gender
                }

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_password_session(request):
    """密码登录"""
    try:
        if request.method == 'POST':
            parameters = request.POST

            get_user = models.User.objects.get(user_phone=parameters['user_phone'])
            if get_user is None:
                return HttpResponse(json.dumps(__notExistUser__), content_type='application/json', charset='utf-8')
            elif parameters['user_password'] != get_user.user_password:
                return HttpResponse(json.dumps(__wrongPassword__), content_type='application/json', charset='utf-8')
            else:
                request.session['user_id'] = get_user.user_id
                request.session['user_login'] = True

                __ok__['user_fillln'] = get_user.user_fillln
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_password(request):
    """找回密码-重置密码"""
    try:
        if request.method == 'PUT':
            parameters = request.PUT

            is_verified = _verify_phone_code_(parameters['user_phone'], parameters['verification_code'])

            if is_verified:
                get_user = models.User.objects.get(user_phone=parameters['user_phone'])
                get_user.user_password = parameters['user_password']
                get_user.save()
            else:
                return HttpResponse(json.dumps(__wrongVerification__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_sms_session(request):
    """用户短信登录"""
    try:
        if request.method == 'POST':
            parameters = request.POST

            is_verified = _verify_phone_code_(parameters['user_phone'], parameters['verification_code'])

            if is_verified:
                get_user = models.User.objects.get(user_phone=parameters['user_phone'])
                
                request.session['user_id'] = get_user.user_id
                request.session['user_login'] = True

                __ok__['user_fillln'] = get_user.user_fillln
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            else:
                return HttpResponse(json.dumps(__wrongVerification__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_session(request):
    """退出登录"""
    try:
        if request.session.get('login', None):
            if request.method == 'DELETE':
                del request.session['user_id']
                del request.session['user_login']

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_balance(request):
    """获取当前用户的余额"""
    try:
        if request.session.get('user_login', None):
            get_user = models.User.objects.get(user_id=request.session['user_id'])
            __ok__['user_balance'] = get_user.user_balance

            return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_tasks(request):
    """获得当前用户发布/领取的所有任务id和共同属性"""
    try:
        if request.session.get('user_login', None):
            if request.method == 'GET':
                parameters = request.GET

                # 0为用户发布的，1为用户领取的
                if parameters['type'] == 0:
                    filter_tasks = models.PublishTask.objects.filter(user_id=request.session['user_id'])
                elif parameters['type'] == 1:
                    filter_tasks = models.PickTask.objects.filter(user_id=request.session['user_id'])

                tasks = []
                for filter_task in filter_tasks:
                    get_task = models.Task.objects.get(task_id=filter_task.task_id)
                    tasks.append({
                        'task_id': get_task.task_id,
                        'user_id': get_task.user_id,
                        'task_type': get_task.task_type,
                        'task_sketch': get_task.task_sketch,
                        'task_bonus': get_task.task_bonus,
                        'task_publishDate': strftime('%Y-%m-%d %H:%M:%S', get_task.task_publishDate)
                    })
                __ok__['tasks'] = tasks

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_information(request):
    """根据用户/关注的人/粉丝id获取用户信息(user_id/following_id/fan_id都适用)"""
    try:
        if request.session.get('user_login', None):
            if request.method == 'GET':
                parameters = request.GET

                users = []
                for user_id_object in parameters['user_ids']:
                    get_user = models.User.objects.get(user_id=user_id_object['user_id'])
                    get_student = models.Student.objects.get(user_id=user_id_object['user_id'])

                    users.append({
                        'user': {
                            'user_id': get_user.user_id,
                            'user_phone': get_user.user_phone,
                            'user_icon': get_user.user_icon,
                            'user_balance': get_user.user_balance,
                            'user_fillln': get_user.user_fillln
                        },
                        'student': {
                            'student_id': get_student.student_id,
                            'user_id': get_student.user_id,
                            'student_number': get_student.student_number,
                            'student_name': get_student.student_name,
                            'student_university': get_student.student_university,
                            'student_academy': get_student.student_academy,
                            'student_gender': get_student.student_gender
                        }
                    })
                __ok__['users'] = users

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_following(request):
    """POST为当前用户关注其它用户，DELETE为当前用户取关其它用户"""
    try:
        if request.session.get('user_login', None):
            if request.method == 'POST':
                parameters = request.POST
                filter_dict = {
                    'user_id': request.session['user_id'],
                    'following_id': parameters['user_id']
                }
                filter_followings = models.Following.objects.filter(**filter_dict)

                # 若未关注则关注
                if filter_followings.__len__ == 0:
                    new_following = models.Following(
                        user_id=request.session['user_id'],
                        following_id=parameters['user_id']
                    )
                    new_following.save()

                    # 并且要添加到粉丝列表
                    new_fan = models.Fan(
                        user_id=parameters['user_id'],
                        fan_id=request.session['user_id']
                    )
                    new_fan.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            elif request.method == 'DELETE':
                parameters = request.DELETE

                # 删除following表条目
                filter_following_dict = {
                    'user_id': request.session['user_id'],
                    'following_id': parameters['user_id']
                }
                models.Following.objects.filter(**filter_following_dict).delete()

                # 删除fan表条目
                filter_fan_fict = {
                    'user_id': parameters['user_id'],
                    'fan_id': request.session['user_id']
                }
                models.Fan.objects.filter(**filter_fan_fict).delete()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_followings(request):
    """获取当前用户关注的所有用户的id"""
    try:
        if request.session.get('user_login', None):
            if request.method == 'GET':
                followings = []
                filter_followings = models.Following.objects.filter(user_id=request.session['user_id'])
                for filter_following in filter_followings:
                    followings.append({
                        'following_id': filter_following.following_id
                    })
                __ok__['followings'] = followings

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_fans(request):
    """获取当前用户的所有粉丝的id"""
    try:
        if request.session.get('user_login', None):
            if request.method == 'GET':
                fans = []
                filter_fans = models.Fan.objects.filter(user_id=request.session['user_id'])
                for filter_fan in filter_fans:
                    fans.append({
                        'fan_id': filter_fan.fan_id
                    })
                __ok__['fans'] = fans

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')