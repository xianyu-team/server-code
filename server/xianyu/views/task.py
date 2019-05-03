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

__notLogin__ = {
    'code': 401,
    'message': '未登录'
}


@csrf_exempt
def task(request):
    if request.session.get('login', None) == True:
        if request.method == 'GET':
            try:
                #最新任务
                if request.GET.type == 0:       
                    filter_tasks = models.Task.objects.all().order_by('-task_publishDate')
                    __ok__['tasks'] = filter_tasks
                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')

                #关注的用户发布的任务
                elif request.GET.type == 1:     
                    #获取关注的用户
                    filter_followers = models.Follower.objects.filter(id = request.session.get('user_id'))
                    tasks = []
                    #获取关注的用户发布的任务
                    for i in filter_followers:
                        filter_tasks = models.Task.objects.filter(user_id = i.follower_id)
                        tasks.append(filter_tasks)
                    __ok__['tasks'] = tasks
                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')

                #金额最高的任务
                elif request.GET.type == 2:     
                    filter_tasks = models.Task.objects.all().order_by('-task_bonus')
                    __ok__['tasks'] = filter_tasks
                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_delivery_detail(request):
    if request.session.get('login', None) == True:
        if request.method == 'GET':
            try:
                filter_delivery = models.Delivery.objects.filter(task_id = request.GET.task_id)
                __ok__['delivery'] = filter_delivery
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')

    
@csrf_exempt
def task_questionnaire_detail(request):
    if request.session.get('login', None) == True:
        if request.method == 'GET':
            try:
                filter_questionnaire = models.Questionnaire.objects.filter(task_id = request.GET.task_id)

                filter_questions = models.Question.objects.filter(questionnaire_id = filter_questionnaire.questionnaire_id)
                
                filter_questionnaire['questions'] = filter_questions
                __ok__['questionnaire'] = filter_questionnaire
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_acceptance(request):
    if request.session.get('login', None) == True:
        if request.method == 'POST':
            try:
                pickTask = models.PickTask()
                pickTask.user_id = request.session.get('user_id')
                pickTask.task_id = request.POST.task_id
                pickTask.save()
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_delivery_complishment(request):
    if request.session.get('login', None) == True:
        if request.method == 'POST':
            try:
                #将递送设置为已完成
                get_delivery = models.Delivery.objects.get(task_id = request.POST.task_id)
                get_delivery.delivery_complished = 1
                get_delivery.delivery_complishDate = strftime('%Y-%m-%d %H:%M:%S',localtime())
                get_delivery.save()

                #将钱给任务领取者
                filter_task = models.Task.objects.filter(task_id = request.POST.task_id)

                get_user = models.User.objects.get(id = request.session.get('user_id'))
                get_user.user_balance += filter_task.task_bonus
                get_user.save()

                #给任务领取者添加账单记录
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 0
                bill.bill_number = filter_task.task_bonus
                bill.bill_description = '完成任务: ' + filter_task.task_sketch
                bill.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')



@csrf_exempt
def task_delivery(request):
    if request.session.get('login', None) == True:
        if request.method == 'DELETE':
            try:
                #从任务列表删除任务
                get_task = models.Task.objects.get(task_id = request.DELETE.task_id)
                get_task.delete()

                #从用户发布任务列表删除任务
                get_publishTask = models.PublishTask.objects.get(task_id = request.DELETE.task_id)
                get_publishTask.delete()
                
                #从用户接取任务列表删除任务
                get_pickTask = models.PickTask.objects.get(task_id = request.DELETE.task_id)
                get_pickTask.delete()

                #从递送列表删除任务
                get_delivery = models.Delivery.objects.get(task_id = request.DELETE.task_id)
                get_delivery.delete()

                #将钱退回给发布者
                filter_task = models.Task.objects.filter(task_id = request.DELETE.task_id)

                get_user = models.User.objects.get(id = request.session.get('user_id'))
                get_user.user_balance += filter_task.task_bonus
                get_user.save()

                #给任务发布者添加一条账单
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 0
                bill.bill_number = filter_task.task_bonus
                bill.bill_description = '取消任务: ' + filter_task.task_sketch
                bill.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
        elif request.method == 'POST':
            try:
                #判断余额是否足够
                filter_user = models.User.objects.filter(id = request.session.get('user_id'))
                if filter_user.user_balance < request.POST.task.task_bonus:
                    __error__['message'] = '余额不足'
                    return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')

                #任务发布者扣除钱
                get_user = models.User.objects.get(id = request.session.get('user_id'))
                get_user.user_balance -= request.POST.task.task_bonus
                get_user.save()

                #给任务发布者添加一条账单
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 1
                bill.bill_number = request.POST.task.task_bonus
                bill.bill_description = '发布任务: ' + filter_task.task_sketch
                bill.save()

                #任务列表添加任务
                task = models.Task()
                task.task_type = request.POST.task.task_type
                task.task_sketch = request.POST.task.task_sketch
                task.task_bonus = request.POST.task.task_bonus
                task.save()

                #用户发布列表添加任务
                publishTask = models.PublishTask()
                publishTask.user_id = request.session.get('user_id')
                publishTask.task_id = task.id 
                publishTask.save()

                #递送列表添加递送
                delivery = models.Delivery()
                delivery.task_id = task.id
                delivery.delivery_detail = request.POST.delivery.delivery_detail
                delivery.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_questionnaire(request):
    if request.session.get('login', None) == True:
        if request.method == 'POST':
            try:
                #判断余额是否足够
                filter_user = models.User.objects.filter(id = request.session.get('user_id'))
                if filter_user.user_balance < request.POST.task.task_bonus * request.POST.questionnaire.questionnaire_number:
                    __error__['message'] = '余额不足'
                    return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')

                #任务发布者扣除钱
                get_user = models.User.objects.get(id = request.session.get('user_id'))
                get_user.user_balance -= request.POST.task.task_bonus * request.POST.questionnaire.questionnaire_number
                get_user.save()

                #给任务发布者添加一条账单
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 1
                bill.bill_number = request.POST.task.task_bonus * request.POST.questionnaire.questionnaire_number
                bill.bill_description = '发布问卷: ' + filter_task.task_sketch
                bill.save()

                #任务列表添加任务
                task = models.Task()
                task.task_type = request.POST.task.task_type
                task.task_sketch = request.POST.task.task_sketch
                task.task_bonus = request.POST.task.task_bonus
                task.save()

                #用户发布列表添加任务
                publishTask = models.PublishTask()
                publishTask.user_id = request.session.get('user_id')
                publishTask.task_id = task.id 
                publishTask.save()

                #问卷列表添加问卷
                questionnaire = models.Questionnaire()
                questionnaire.task_id = task.id
                questionnaire_number = request.POST.questionnaire.questionnaire_number

                #题目列表添加题目
                for i in request.POST.questionnaire.questions:
                    question = models.Question()
                    question.questionnaire_id = questionnaire.questionnaire_id 
                    question.question_description = i.question_description
                    question.question_type = i.question_type
                    question.question_a = i.question_a
                    question.question_b = i.question_b
                    question.question_c = i.question_c
                    question.question_d = i.question_d
                    question.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_questionnaire_answer(request):
    if request.session.get('login', None) == True:
        if request.method == 'POST':
            try:
                 #将问卷份数减一
                get_questionnaire = models.Questionnaire.objects.get(questionnaire_id = request.POST.questionnaire_id) 
                get_questionnaire.questionnaire_number -= 1
                get_questionnaire.save()

                #若问卷份数为0, 问卷停止
                filter_questionnaire = models.Questionnaire.objects.filter(questionnaire_id = request.POST.questionnaire_id) 
                if filter_questionnaire.questionnaire_number == 0:
                    filter_questionnaire.questionnaire_closed = 1
                    filter_questionnaire.questionnaire_deadline = strftime('%Y-%m-%d %H:%M:%S',localtime())

                #添加答卷
                answerSheet = models.AnswerSheet()
                answerSheet.questionnaire_id = request.POST.questionnaire_id
                answerSheet.user_id = request.session.get('user_id')
                answerSheet.save()

                #添加答案
                for i in request.POST.answers:
                    answer = models.Answer()
                    answer.answerSheet_id = answerSheet.id
                    answer.question_id = i.question_id
                    answer.answer_content = i.answer_content
                    answer.save()

                #添加用户接取任务
                pickTask = models.PickTask()
                pickTask.user_id = request.session.get('user_id')
                pickTask.task_id = filter_questionnaire.task_id
                pickTask.save()

                #将钱给问卷填写者
                filter_task = models.Task.objects.filter(task_id = filter_questionnaire.task_id)

                get_user = models.User.objects.get(id = request.session.get('user_id'))
                get_user.user_balance += filter_task.task_bonus
                get_user.save()

                #给问卷填写者添加账单记录
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 0
                bill.bill_number = filter_task.task_bonus
                bill.bill_description = '填写问卷: ' + filter_task.task_sketch
                bill.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')



@csrf_exempt
def task_questionnaire_answerSheet(request):
    if request.session.get('login', None) == True:
        if request.method == 'GET':
            try:
                #获取答卷
                filter_answerSheet = models.AnswerSheet.objects.filter(questionnaire_id = request.GET.questionnaire_id, user_id = request.session.get('user_id')) 
                
                #获取答案
                filter_answers = models.Answer.objects.filter(answerSheet_id = filter_answerSheet.id)

                #获取题目
                answerSheet = []
                for i in filter_answers:
                    ele = {}
                    filter_question = models.Question.objects.filter(id = i.question_id)
                    ele['question'] = filter_question
                    ele['answer'] = i
                    answerSheet.append(ele)

                __ok__['answerSheet'] = answerSheet

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')



@csrf_exempt
def task_questionnaire_Statistics(request):
    if request.session.get('login', None) == True:
        if request.method == 'GET':
            try:
                statistics = []

                #获取题目
                filter_questions = models.Question.objects.filter(questionnaire_id = request.GET.questionnaire_id)  

                #统计答案
                for i in filter_questions:
                    ele = {}
                    ele['question'] = i 
                    answer_gap_filling = []
                    answer = {
                        "answer_a_count": 0,
                        "answer_b_count": 0,
                        "answer_c_count": 0,
                        "answer_d_count": 0,
                        "answer_gap_filling" : answer_gap_filling
                    }
                    filter_answers = models.Answer.objects.filter(question_id = i.id) 
                    for j in filter_answers:
                        #填空题
                        if i.question_type == 2:
                            answer_gap_filling.append(j)
                        #选择题
                        else:
                            #解析答案
                            for c in j.answer_content:
                                if c == 'A':    
                                    answer["answer_a_count"] += 1 
                                if c == 'B':    
                                    answer["answer_b_count"] += 1 
                                if c == 'C':    
                                    answer["answer_c_count"] += 1 
                                if c == 'D':    
                                    answer["answer_d_count"] += 1 
                    ele['answer'] = answer 
                    statistics.append(ele)

                __ok__['statistics'] = statistics
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')



@csrf_exempt
def task_questionnaire_closure(request):
    if request.session.get('login', None) == True:
        if request.method == 'PUT':
            try:
                #问卷截止
                get_questionnaire = models.Questionnaire.objects.get(id = request.PUT.questionnaire_id)
                get_questionnaire.questionnaire_closed = 1
                get_questionnaire.questionnaire_deadline = strftime('%Y-%m-%d %H:%M:%S',localtime())
                get_questionnaire.save()

                #若问卷还有多余的
                filter_questionnaire = models.Questionnaire.objects.filter(id = request.PUT.questionnaire_id)
                if filter_questionnaire.questionnaire_number > 0:
                    #将钱退给发布者
                    filter_task = models.Task.objects.filter(id = filter_questionnaire.task_id)

                    get_user = models.User.objects.get(id = request.session.get('user_id'))
                    get_user.user_balance += filter_questionnaire.questionnaire_number * filter_task.task_bonus
                    get_user.save()

                    #添加账单
                    bill = models.Bill()
                    bill.user_id = request.session.get('user_id')
                    bill.bill_type = 0
                    bill.bill_number = filter_task.task_bonus
                    bill.bill_description = '多余问卷退回: ' + filter_task.task_sketch
                    bill.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')