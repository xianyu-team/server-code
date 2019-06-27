"""
API文档的用户user部分
"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from time import strftime, localtime
from django.http import QueryDict
import json
import time
import hashlib
import uuid
import requests
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

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

__followMyselfError__ = {
    'code': 400,
    'message': '无法关注自己'
}

__notLogin__ = {
    'code': 401,
    'message': '未登录'
}


'''
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
        return True
    else:
        return False
'''


def _verify_phone_code_(request, user_phone, verification_code):
    """
    此函数为私有函数，没有用第三方短信服务，后端模拟验证手机验证码，传入参数为手机号和验证码，返回值为bool值，true为成功验证
    """
    current_time = time.time()
    get_verification_code_time = request.session.get(user_phone + '_get_verification_code_time', 0)

    if current_time - get_verification_code_time < 600:
        if verification_code == request.session.get(user_phone + '_verification_code', '-1'):
            return True
        else:
            return False
    else:
        return False


@csrf_exempt
def user(request):
    """用户注册"""
    try:
        if request.method == 'POST':
            parameters = json.loads(request.body.decode('utf-8'))

            # 先检查手机号是否唯一
            # 获取多个对象用filter
            filter_user = models.User.objects.filter(user_phone=parameters['user_phone'])
            if filter_user.__len__() == 0:
                is_verified = _verify_phone_code_(request, parameters['user_phone'], parameters['verification_code'])

                if is_verified:
                    new_user = models.User(
                        user_phone=parameters['user_phone'],
                        user_password=parameters['user_password']
                    )
                    new_user.save()

                    # session保存用户登录状态
                    request.session['user_id'] = new_user.user_id
                    request.session['is_login'] = True

                    data = {}
                    __ok__['data'] = data

                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
                else:
                    return HttpResponse(json.dumps(__wrongVerification__), content_type='application/json', charset='utf-8')
            else:
                return HttpResponse(json.dumps(__hasExistUser__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_profile(request):
    """PUT为完善或修改当前用户信息，GET为获取当前用户信息"""
    try:
        if request.session.get('is_login', None):
            if request.method == 'PUT':
                parameters = json.loads(request.body.decode('utf-8'))

                # 获取单个对象用get
                get_user = models.User.objects.get(user_id=request.session['user_id'])
                # 参数是图片byte数组转成的string，存入数据库时把string转回byte数组
                get_user.user_icon = bytes(parameters['user_icon'], encoding='utf-8')
                # 并将用户是否填写了个人信息置为1
                get_user.user_fillln = 1
                get_user.save()

                # 学生信息不存在则创建
                filter_student = models.Student.objects.filter(user_id=request.session['user_id'])
                if filter_student.__len__() == 0:
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
                    get_student = models.Student.objects.get(user_id=request.session['user_id'])

                    get_student.user_id = request.session['user_id']
                    get_student.student_number = parameters['student_number']
                    get_student.student_name = parameters['student_name']
                    get_student.student_university = parameters['student_university']
                    get_student.student_academy = parameters['student_academy']
                    get_student.student_gender = parameters['student_gender']
                    get_student.save()

                data = {}
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            elif request.method == 'GET':
                get_user = models.User.objects.get(user_id=request.session['user_id'])
                get_student = models.Student.objects.get(user_id=request.session['user_id'])

                data = {
                    'user': {
                        'user_id': get_user.user_id,
                        'user_phone': get_user.user_phone,
                        # 数据库里存的是图片的byte数组，需要转sting再传给前端
                        'user_icon': str(get_user.user_icon, encoding='utf-8'),
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
                }
                __ok__['data'] = data

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
            parameters = json.loads(request.body.decode('utf-8'))

            filter_user = models.User.objects.filter(user_phone=parameters['user_phone'])
            if filter_user.__len__() == 0:
                return HttpResponse(json.dumps(__notExistUser__), content_type='application/json', charset='utf-8')
            else:
                get_user = models.User.objects.get(user_phone=parameters['user_phone'])

                if parameters['user_password'] != get_user.user_password:
                    return HttpResponse(json.dumps(__wrongPassword__), content_type='application/json', charset='utf-8')
                else:
                    request.session['user_id'] = get_user.user_id
                    request.session['is_login'] = True

                    data = {
                        'user_fillln': get_user.user_fillln
                    }
                    __ok__['data'] = data

                    # 在cookie中设置csrftoken
                    get_token(request)

                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')


@csrf_exempt
def user_password(request):
    """找回密码-重置密码"""
    try:
        if request.method == 'PUT':
            parameters = json.loads(request.body.decode('utf-8'))

            is_verified = _verify_phone_code_(request, parameters['user_phone'], parameters['verification_code'])

            if is_verified:
                filter_user = models.User.objects.filter(user_phone=parameters['user_phone'])
                if filter_user.__len__() == 0:
                    return HttpResponse(json.dumps(__notExistUser__), content_type='application/json', charset='utf-8')
                else:
                    get_user = models.User.objects.get(user_phone=parameters['user_phone'])
                    get_user.user_password = parameters['user_password']
                    get_user.save()

                    data = {}
                    __ok__['data'] = data

                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
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
            parameters = json.loads(request.body.decode('utf-8'))

            is_verified = _verify_phone_code_(request, parameters['user_phone'], parameters['verification_code'])

            if is_verified:
                filter_user = models.User.objects.filter(user_phone=parameters['user_phone'])
                if filter_user.__len__() == 0:
                    return HttpResponse(json.dumps(__notExistUser__), content_type='application/json', charset='utf-8')
                else:
                    get_user = models.User.objects.get(user_phone=parameters['user_phone'])

                    request.session['user_id'] = get_user.user_id
                    request.session['is_login'] = True

                    data = {
                        'user_fillln': get_user.user_fillln
                    }
                    __ok__['data'] = data

                    # 在cookie中设置csrftoken
                    get_token(request)

                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            else:
                return HttpResponse(json.dumps(__wrongVerification__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_session(request):
    """退出登录"""
    try:
        if request.session.get('is_login', None):
            if request.method == 'DELETE':
                del request.session['user_id']
                del request.session['is_login']

                data = {}
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_balance(request):
    """获取当前用户的余额"""
    try:
        if request.session.get('is_login', None):
            get_user = models.User.objects.get(user_id=request.session['user_id'])

            data = {
                'user_balance': get_user.user_balance
            }
            __ok__['data'] = data

            return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_tasks(request, t_type):
    """获得当前用户发布/领取的所有任务id和共同属性"""
    try:
        if request.session.get('is_login', None):
            if request.method == 'GET':
                # 0为用户发布的，1为用户领取的
                filter_tasks = set()

                # 正则匹配的参数是str，应转为int
                t_type = int(t_type)

                if t_type == 0:  
                    filter_tasks = models.PublishTask.objects.filter(user_id=request.session['user_id'])
                elif t_type == 1:
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
                        'task_publishDate': get_task.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                    })

                # 给tasks对象数组按发布时间逆序排序，即最新的放在数组前面
                tasks.sort(key=lambda task: task['task_publishDate'])
                tasks.reverse()

                data = {
                    'tasks': tasks
                }
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_batch_information(request):
    """根据用户/关注的人/粉丝id获取用户信息(user_id/following_id/fan_id都适用)"""
    try:
        if request.session.get('is_login', None):
            if request.method == 'POST':
                parameters = json.loads(request.body.decode('utf-8'))

                users = []
                for user_id_object in parameters['user_ids']:
                    get_user = models.User.objects.get(user_id=user_id_object['user_id'])
                    # 若用户user_fillln为0，则没有student信息，此时get抛错，可以返回“服务器错误”信息，没影响
                    get_student = models.Student.objects.get(user_id=user_id_object['user_id'])

                    users.append({
                        'user': {
                            'user_id': get_user.user_id,
                            'user_phone': get_user.user_phone,
                            'user_icon': str(get_user.user_icon, encoding='utf-8'),
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

                data = {
                    'users': users
                }
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_following(request):
    """POST为当前用户关注其它用户，DELETE为当前用户取关其它用户"""
    try:
        if request.session.get('is_login', None):
            if request.method == 'POST':
                parameters = json.loads(request.body.decode('utf-8'))

                if request.session['user_id'] == parameters['user_id']:
                    return HttpResponse(json.dumps(__followMyselfError__), content_type='application/json', charset='utf-8')
                else:
                    # 操作 following 表
                    filter_following_dict = {
                        'user_id': request.session['user_id'],
                        'following_id': parameters['user_id']
                    }
                    filter_followings = models.Following.objects.filter(**filter_following_dict)

                    # 若未关注则关注
                    if filter_followings.__len__() == 0:
                        new_following = models.Following(
                            user_id=request.session['user_id'],
                            following_id=parameters['user_id']
                        )
                        new_following.save()

                    # 操作 fan 表
                    filter_fan_dict = {
                        'user_id': parameters['user_id'],
                        'fan_id': request.session['user_id']
                    }
                    filter_fans = models.Fan.objects.filter(**filter_fan_dict)

                    # 若粉丝列表不存在则添加
                    if filter_fans.__len__() == 0:
                        new_fan = models.Fan(
                            user_id=parameters['user_id'],
                            fan_id=request.session['user_id']
                        )
                        new_fan.save()

                    data = {}
                    __ok__['data'] = data

                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            elif request.method == 'DELETE':
                parameters = json.loads(request.body.decode('utf-8'))

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

                data = {}
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_followings(request):
    """获取当前用户关注的所有用户的id"""
    try:
        if request.session.get('is_login', None):
            if request.method == 'GET':
                followings = []
                filter_followings = models.Following.objects.filter(user_id=request.session['user_id'])
                for filter_following in filter_followings:
                    followings.append({
                        'following_id': filter_following.following_id
                    })

                data = {
                    'followings': followings
                }
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_fans(request):
    """获取当前用户的所有粉丝的id"""
    try:
        if request.session.get('is_login', None):
            if request.method == 'GET':
                fans = []
                filter_fans = models.Fan.objects.filter(user_id=request.session['user_id'])
                for filter_fan in filter_fans:
                    fans.append({
                        'fan_id': filter_fan.fan_id
                    })

                data = {
                    'fans': fans
                }
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_user_id_followings(request, u_id):
    """获取某个用户关注的所有用户的id"""
    try:
        if request.session.get('is_login', None):
            if request.method == 'GET':
                followings = []
                filter_followings = models.Following.objects.filter(user_id=u_id)
                for filter_following in filter_followings:
                    followings.append({
                        'following_id': filter_following.following_id
                    })

                data = {
                    'followings': followings
                }
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')



def user_user_id_fans(request, u_id):
    """获取某个用户的所有粉丝的id"""
    try:
        if request.session.get('is_login', None):
            if request.method == 'GET':
                fans = []
                filter_fans = models.Fan.objects.filter(user_id=u_id)
                for filter_fan in filter_fans:
                    fans.append({
                        'fan_id': filter_fan.fan_id
                    })

                data = {
                    'fans': fans
                }
                __ok__['data'] = data

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
