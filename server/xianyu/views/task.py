from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
from time import strftime, localtime
import datetime

from xianyu import models

__ok__ = {
    'code': 200,
    'message': 'OK',
    "data": {

    }
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
def task(request, t_type):
    #将t_type转为数字类型
    t_type = int(t_type)

    if request.session.get('is_login', None) == True:
        if request.method == 'GET':
            try:
                #最新任务
                if t_type == 0:     
                    filter_tasks = models.Task.objects.all().order_by('-task_publishDate')
                    
                    # 将QuerySet转换为数组
                    tasks = []
                    for i in filter_tasks: 
                        tasks.append({
                            "task_id": i.task_id,
                            "user_id": i.user_id,
                            "task_type": i.task_type,
                            "task_sketch": i.task_sketch,
                            "task_bonus": i.task_bonus,
                            "task_publishDate": (i.task_publishDate + datetime.timedelta(hours = 8)).strftime('%Y-%m-%d %H:%M:%S')  # 将取出来的UTC时间转换为北京时间
                        })

                    __ok__['data'] = {
                        'tasks': tasks
                    }
                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')

                #关注的用户发布的任务
                elif t_type == 1:   
                    #获取关注的用户
                    filter_fans = models.Fan.objects.filter(user_id = request.session.get('user_id'))

                    # 若没有关注的用户, 直接返回
                    if filter_fans.__len__() == 0:
                        __ok__['data'] = {}
                        return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
                    
                    tasks = []
                    #获取关注的用户发布的任务
                    for i in filter_fans:
                        filter_tasks = models.Task.objects.filter(user_id = i.fan_id)
                        tasks.append(filter_tasks)

                    # 将QuerySet转换为数组
                    tasks = []
                    for i in filter_tasks: 
                        tasks.append({
                            "task_id": i.task_id,
                            "user_id": i.user_id,
                            "task_type": i.task_type,
                            "task_sketch": i.task_sketch,
                            "task_bonus": i.task_bonus,
                            "task_publishDate": (i.task_publishDate + datetime.timedelta(hours = 8)).strftime('%Y-%m-%d %H:%M:%S')  # 将取出来的UTC时间转换为北京时间
                        })

                    __ok__['data'] = {
                        'tasks': tasks
                    }

                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
                #金额最高的任务
                elif t_type == 2:     
                    filter_tasks = models.Task.objects.all().order_by('-task_bonus')

                    # 将QuerySet转换为数组
                    tasks = []
                    for i in filter_tasks: 
                        tasks.append({
                            "task_id": i.task_id,
                            "user_id": i.user_id,
                            "task_type": i.task_type,
                            "task_sketch": i.task_sketch,
                            "task_bonus": i.task_bonus,
                            "task_publishDate": (i.task_publishDate + datetime.timedelta(hours = 8)).strftime('%Y-%m-%d %H:%M:%S')  # 将取出来的UTC时间转换为北京时间
                        })

                    __ok__['data'] = {
                        'tasks': tasks
                    }
                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_delivery_detail(request, t_id):
    # 将_id转为int型
    t_id = int(t_id)

    if request.session.get('is_login', None) == True:
        if request.method == 'GET':
            try:
                get_delivery = models.Delivery.objects.get(task_id = t_id)

                __ok__['data'] = {
                    'delivery': get_delivery
                }

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')

    
@csrf_exempt
def task_questionnaire_detail(request, t_id):
    # 将t_id转为int型
    t_id = int(t_id)

    if request.session.get('is_login', None) == True:
        if request.method == 'GET':
            try:
                get_questionnaire = models.Questionnaire.objects.get(task_id = t_id)

                filter_questions = models.Question.objects.filter(questionnaire_id = filter_questionnaire['questionnaire_id'])
                
                # 将QuerySet转换为数组
                questions = []
                for i in filter_questions: 
                    questions.append({
                        "question_id":              i.question_id,
                        "questionnaire_id":         i.questionnaire_id,
                        "question_description":     i.question_description,
                        "question_type":            i.question_type,
                        "question_a":               i.question_a,
                        "question_b":               i.question_b,
                        "question_c":               i.question_c,
                        "question_d":               i.question_d
                    })
                get_questionnaire['questions'] = questions

                __ok__['data'] = {
                    'questionnaire': get_questionnaire
                }          

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_acceptance(request):
    if request.session.get('is_login', None) == True:
        if request.method == 'POST':
            try:
                parameters = json.loads(request.body)

                pickTask = models.PickTask()
                pickTask.user_id = request.session.get('user_id')
                pickTask.task_id = parameters['task_id']
                pickTask.save()
                __ok__['data'] = {}
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_delivery_complishment(request):
    if request.session.get('is_login', None) == True:
        if request.method == 'POST':
            try:
                parameters = json.loads(request.body)

                #将递送设置为已完成
                get_delivery = models.Delivery.objects.get(task_id = parameters['task_id'])
                get_delivery.delivery_complished = 1
                get_delivery.delivery_complishDate = strftime('%Y-%m-%d %H:%M:%S', localtime())
                get_delivery.save()

                #将钱给任务领取者
                get_task = models.Task.objects.get(task_id = parameters['task_id'])

                get_user = models.User.objects.get(user_id = request.session.get('user_id'))
                get_user.user_balance += get_task.task_bonus
                get_user.save()

                #给任务领取者添加账单记录
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 0
                bill.bill_number = get_task.task_bonus
                bill.bill_description = '完成任务: ' + get_task.task_sketch
                bill.save()
                __ok__['data'] = {}
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')

@csrf_exempt
def task_delivery_delete(request, t_id):
     # 将t_id转为int型
    t_id = int(t_id)

    if request.session.get('is_login', None) == True:
        if request.method == 'DELETE':
            try:
                #从任务列表删除任务
                get_task = models.Task.objects.get(task_id = t_id)
                get_task.delete()

                #从用户发布任务列表删除任务
                get_publishTask = models.PublishTask.objects.get(task_id = t_id)
                get_publishTask.delete()
                
                #从用户接取任务列表删除任务
                get_pickTask = models.PickTask.objects.get(task_id = t_id)
                get_pickTask.delete()

                #从递送列表删除任务
                get_delivery = models.Delivery.objects.get(task_id = t_id)
                get_delivery.delete()

                #将钱退回给发布者
                get_user = models.User.objects.get(user_id = request.session.get('user_id'))
                get_user.user_balance += get_task.task_bonus
                get_user.save()

                #给任务发布者添加一条账单
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 0
                bill.bill_number = get_task.task_bonus
                bill.bill_description = '取消任务: ' + get_task.task_sketch
                bill.save()
                __ok__['data'] = {}
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_delivery(request):
    if request.session.get('is_login', None):
        if request.method == 'POST':
            try:
                parameters = json.loads(request.body)
                
                #判断余额是否足够
                get_user = models.User.objects.get(user_id = request.session.get('user_id'))
                if get_user.user_balance < parameters['task']['task_bonus']:
                    __error__['message'] = '余额不足'
                    return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')

                #任务发布者扣除钱
                get_user.user_balance -= parameters['task']['task_bonus']
                get_user.save()

                #给任务发布者添加一条账单
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 1
                bill.bill_number = parameters['task']['task_bonus']
                bill.bill_description = '发布任务: ' + parameters['task']['task_sketch']
                bill.save()

                #任务列表添加任务
                task = models.Task()
                task.user_id = request.session.get('user_id')
                task.task_type = parameters['task']['task_type']
                task.task_sketch = parameters['task']['task_sketch']
                task.task_bonus = parameters['task']['task_bonus']
                task.save()

                #用户发布列表添加任务
                publishTask = models.PublishTask()
                publishTask.user_id = request.session.get('user_id')
                publishTask.task_id = task.task_id
                publishTask.save()

                #递送列表添加递送
                delivery = models.Delivery()
                delivery.task_id = task.task_id
                delivery.delivery_detail = parameters['delivery']['delivery_detail']
                delivery.save()
                __ok__['data'] = {}
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_questionnaire(request):
    if request.session.get('is_login', None) == True:
        if request.method == 'POST':
            try:
                parameters = json.loads(request.body)

                #判断余额是否足够
                get_user = models.User.objects.get(user_id = request.session.get('user_id'))
                if get_user.user_balance < parameters['task']['task_bonus'] * parameters['questionnaire']['questionnaire_number']:
                    __error__['message'] = '余额不足'
                    return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')

                #任务发布者扣除钱
                get_user.user_balance -= parameters['task']['task_bonus'] * parameters['questionnaire']['questionnaire_number']
                get_user.save()

                #给任务发布者添加一条账单
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 1
                bill.bill_number = parameters['task']['task_bonus'] * parameters['questionnaire']['questionnaire_number']
                bill.bill_description = '发布问卷: ' + parameters['task']['task_sketch']
                bill.save()

                #任务列表添加任务
                task = models.Task()
                task.user_id = request.session.get('user_id') 
                task.task_type = parameters['task']['task_type']
                task.task_sketch = parameters['task']['task_sketch']
                task.task_bonus = parameters['task']['task_bonus']
                task.save()

                #用户发布列表添加任务
                publishTask = models.PublishTask()
                publishTask.user_id = request.session.get('user_id')
                publishTask.task_id = task.task_id
                publishTask.save()

                #问卷列表添加问卷
                questionnaire = models.Questionnaire()
                questionnaire.task_id = task.task_id
                questionnaire_number = parameters['questionnaire']['questionnaire_number']
                questionnaire.save()

                #题目列表添加题目
                for i in parameters['questionnaire']['questions']:
                    question = models.Question()
                    question.questionnaire_id = questionnaire.questionnaire_id 
                    question.question_description = i['question_description']
                    question.question_type = i['question_type']
                    question.question_a = i['question_a']
                    question.question_b = i['question_b']
                    question.question_c = i['question_c']
                    question.question_d = i['question_d']
                    question.save()
                __ok__['data'] = {}
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')


@csrf_exempt
def task_questionnaire_answer(request):
    if request.session.get('is_login', None) == True:
        if request.method == 'POST':
            try:
                parameters = json.loads(request.body)

                 #将问卷份数减一
                get_questionnaire = models.Questionnaire.objects.get(questionnaire_id = parameters['questionnaire_id']) 
                get_questionnaire.questionnaire_number -= 1
                get_questionnaire.save()

                #若问卷份数为0, 问卷停止
                get_questionnaire = models.Questionnaire.objects.get(questionnaire_id = parameters['questionnaire_id']) 
                if get_questionnaire.questionnaire_number == 0:
                    get_questionnaire.questionnaire_closed = 1
                    get_questionnaire.questionnaire_deadline = strftime('%Y-%m-%d %H:%M:%S', localtime())

                #添加答卷
                answerSheet = models.AnswerSheet()
                answerSheet.questionnaire_id = parameters['questionnaire_id']
                answerSheet.user_id = request.session.get('user_id')
                answerSheet.save()

                #添加答案
                for i in parameters['answers']:
                    answer = models.Answer()
                    answer.answerSheet_id = answerSheet.id
                    answer.question_id = i['question_id']
                    answer.answer_content = i['answer_content']
                    answer.save()

                #添加用户接取任务
                pickTask = models.PickTask()
                pickTask.user_id = request.session.get('user_id')
                pickTask.task_id = get_questionnaire.task_id
                pickTask.save()

                #将钱给问卷填写者
                get_task = models.Task.objects.get(task_id = get_questionnaire.task_id)

                get_user = models.User.objects.get(user_id = request.session.get('user_id'))
                get_user.user_balance += get_task.task_bonus
                get_user.save()

                #给问卷填写者添加账单记录
                bill = models.Bill()
                bill.user_id = request.session.get('user_id')
                bill.bill_type = 0
                bill.bill_number = get_task.task_bonus
                bill.bill_description = '填写问卷: ' + get_task.task_sketch
                bill.save()
                __ok__['data'] = {}
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')



@csrf_exempt
def task_questionnaire_answerSheet(request, q_id):
    # 将q_id转为int型
    q_id = int(q_id)

    if request.session.get('is_login', None) == True:
        if request.method == 'GET':
            try:
                #获取答卷
                get_answerSheet = models.AnswerSheet.objects.get(questionnaire_id = q_id, user_id = request.session.get('user_id')) 
                
                #获取答案
                filter_answers = models.Answer.objects.filter(answerSheet_id = get_answerSheet.id)

                #获取题目
                answerSheet = []
                for i in filter_answers:
                    ele = {}
                    get_question = models.Question.objects.get(question_id = i.question_id)
                    ele['question'] = get_question
                    ele['answer'] = i
                    answerSheet.append(ele)

                __ok__['data'] = {
                    'answerSheet': answerSheet
                }

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')



@csrf_exempt
def task_questionnaire_Statistics(request, q_id):
    # 将q_id转为int型
    q_id = int(qe_id)

    if request.session.get('is_login', None) == True:
        if request.method == 'GET':
            try:
                statistics = []

                #获取题目
                filter_questions = models.Question.objects.filter(questionnaire_id = q_id)  

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

                __ok__['data'] = {
                    'statistics': statistics
                }

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')



@csrf_exempt
def task_questionnaire_closure(request):
    if request.session.get('is_login', None) == True:
        if request.method == 'PUT':
            try:
                parameters = json.loads(request.body)

                #问卷截止
                get_questionnaire = models.Questionnaire.objects.get(questionnaire_id = parameters['questionnaire_id'])
                get_questionnaire.questionnaire_closed = 1
                get_questionnaire.questionnaire_deadline = strftime('%Y-%m-%d %H:%M:%S', localtime())
                get_questionnaire.save()

                #若问卷还有多余的
                get_questionnaire = models.Questionnaire.objects.get(questionnaire_id = parameters['questionnaire_id'])
                if get_questionnaire.questionnaire_number > 0:
                    #将钱退给发布者
                    get_task = models.Task.objects.get(task_id = get_questionnaire.task_id)

                    get_user = models.User.objects.get(user_id = request.session.get('user_id'))
                    get_user.user_balance += get_questionnaire.questionnaire_number * get_task.task_bonus
                    get_user.save()

                    #添加账单
                    bill = models.Bill()
                    bill.user_id = request.session.get('user_id')
                    bill.bill_type = 0
                    bill.bill_number = get_task.task_bonus
                    bill.bill_description = '多余问卷退回: ' + get_task.task_sketch
                    bill.save()
                __ok__['data'] = {}
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')