from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from user import models

__ok__ = {
    'code': 200,
    'message': 'OK'
}
__error__ = {
    'code': 400,
    'message': '服务器发生错误'
}

__notLogin__ = {
    'code': 401,
    'message': '未登录'
}

@csrf_exempt
def profile(request):
    if request.session.get('login', None):
        if request.method == 'POST':
            try:
                #更新头像
                filter_user = models.User.objects.filter(id = request.session.get('user_id'))
                filter_user.user_icon = request.POST.user_icon
                filter_user.save()

                # 若学生信息存在则更新, 不存在则创建
                filter_student = models.Student.objects.filter(user_id = request.session.get('user_id'))
                if filter_user.__len__() == 0:
                    student = models.Student()
                    student.student_name = request.POST['student_name'],
                    student.student_university = request.POST['student_university']
                    student.student_academy = request.POST['student_academy']
                    student.student_number = request.POST['student_number']
                    student.student_gender = request.POST['student_gender']
                    student.save()
                else:
                    filter_student.user_id = request.session.get('user_id')
                    filter_student.student_name = request.POST['student_name'],
                    filter_student.student_university = request.POST['student_university']
                    filter_student.student_academy = request.POST['student_academy']
                    filter_student.student_number = request.POST['student_number']
                    filter_student.student_gender = request.POST['student_gender']
                    filter_student.save()
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
                
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')

        elif request.method == 'GET':
            try:
                filter_user = models.User.objects.filter(id = request.session.get('user_id'))
                user_phone = filter_user.user_phone
                user_icon = filter_user.user_icon

                filter_student = models.Student.objects.filter(user_id = request.session.get('user_id'))
                student_name = filter_student.student_name
                student_university = filter_student.student_university
                student_academy = filter_student.student_academy
                student_number = filter_student.student_number
                student_gender = filter_student.student_gender

                __rep__ = {
                    'code': 200,
                    "message": "OK",
                    "user_phone": filter_user.user_phone,
                    "user_icon": filter_user.user_icon,   
                    "student_name": filter_student.student_name, 
                    "student_university": filter_student.student_university, 
                    "student_academy": filter_student.student_academy,   
                    "student_number": filter_student.student_number,  
                    "student_gender": filter_student.student_gender
                }
                return HttpResponse(json.dumps(__rep__), content_type='application/json', charset='utf-8')

            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')