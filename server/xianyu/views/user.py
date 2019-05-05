from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
from time import strftime, localtime

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

# 用户注册
@csrf_exempt
def user(request):
    try:
        if request.method == 'POST':
            parameters = request.POST
            # 先检查手机号是否唯一
            # 获取多个对象用filter
            filter_user = models.User.objects.filter(user_phone=parameters['user_phone'])
            if filter_user.__len__() == 0:
                new_user = models.User(
                    user_phone=parameters['user_phone'],
                    user_password=parameters['user_password']
                )
                new_user.save()
                request.session['user_id'] = new_user.user_id
                request.session['user_login'] = True
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            else:
                return HttpResponse(json.dumps(__hasExistUser__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')

@csrf_exempt
def user_profile(request):
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
def user_session(request):
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
                        # 时间解析
                    })
        else:
            return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')
    except Exception as exc:
        print(exc)
        return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
