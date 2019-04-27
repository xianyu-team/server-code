from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json

from order import models
from balance import models

__ok__ = {
    'code': 200,
    'message': 'OK'
}
__error__ = {
    'code': 400,
    'message': '服务器发生错误'
}

_notLogin_ = {
    'code': 401,
    'message': '未登录'
}

@csrf_exempt
def order(request):
    if request.session.get('login', none):
        if request.method == 'GET':
            try:
                if request.GET.type == 0:
                    filter_orders = PublishOrder.objects.filter(id = request.session.get('user_id')).order('order_publishDate')
                    orders = []
                    for i in filter_orders:
                        order = {}
                        filter_order = Order.objects.filter(id = i.order_id)
                        order.id = filter_order.id
                        order.order_type = filter_order.order_type
                        order.order_bonus = filter_order.order_bonus
                        order.order_detail = filter_order.order_detail
                        order.order_publishDate = filter_order.order_publishDate
                        order.order_description = filter_order.order_description
                        order.order_picked = filter_order.order_picked
                        order.order_complished = filter_order.order_complished
                        order.order_complishDate = filter_order.order_complishDate
                        order.publisher_id = i.user_id
                        orders.append(filter_order)
                    __ok__['order'] = orders
                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
                elif request.GET.type == 1:
                    filter_orders = PublishOrder.objects.filter(id = request.session.get('user_id')).order('order_publishDate').reverse()
                    orders = []
                    for i in filter_orders:
                        order = {}
                        filter_order = Order.objects.filter(id = i.order_id)
                        order.id = filter_order.id
                        order.order_type = filter_order.order_type
                        order.order_bonus = filter_order.order_bonus
                        order.order_detail = filter_order.order_detail
                        order.order_publishDate = filter_order.order_publishDate
                        order.order_description = filter_order.order_description
                        order.order_picked = filter_order.order_picked
                        order.order_complished = filter_order.order_complished
                        order.order_complishDate = filter_order.order_complishDate
                        order.publisher_id = i.user_id
                        orders.append(filter_order)
                    __ok__['order'] = orders
                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
                elif request.GET.type == 2:
                    filter_orders = PublishOrder.objects.filter(id = request.session.get('user_id')).order('order_bonus')
                    orders = []
                    for i in filter_orders:
                        order = {}
                        filter_order = Order.objects.filter(id = i.order_id)
                        order.id = filter_order.id
                        order.order_type = filter_order.order_type
                        order.order_bonus = filter_order.order_bonus
                        order.order_detail = filter_order.order_detail
                        order.order_publishDate = filter_order.order_publishDate
                        order.order_description = filter_order.order_description
                        order.order_picked = filter_order.order_picked
                        order.order_complished = filter_order.order_complished
                        order.order_complishDate = filter_order.order_complishDate
                        order.publisher_id = i.user_id
                        orders.append(filter_order)
                    __ok__['order'] = orders
                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
                elif request.GET.type == 3:
                    filter_orders = PublishOrder.objects.filter(id = request.session.get('user_id')).order('order_bonus').reverse()
                    orders = []
                    for i in filter_orders:
                        order = {}
                        filter_order = Order.objects.filter(id = i.order_id)
                        order.id = filter_order.id
                        order.order_type = filter_order.order_type
                        order.order_bonus = filter_order.order_bonus
                        order.order_detail = filter_order.order_detail
                        order.order_publishDate = filter_order.order_publishDate
                        order.order_description = filter_order.order_description
                        order.order_picked = filter_order.order_picked
                        order.order_complished = filter_order.order_complished
                        order.order_complishDate = filter_order.order_complishDate
                        order.publisher_id = i.user_id
                        orders.append(filter_order)
                    __ok__['order'] = orders
                    return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')     
        if request.method == 'DELETE':
            try:
                user = User.objects.get(id=request.session.get('user_id', none))
                user.balance += order.order_bonus
                user.save()

                order = Order.objects.get(id=request.POST.order_id)
                order.delete()


                pick_order = PickOrder.objects.get(id=request.POST.order_id)
                pick_order.delete()

                publish_order = PublishOrder.objects.get(id=request.POST.order_id)
                publish_order.delete()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')     

        if request.method == 'POST':
            try:

                user = User.objects.filter(id=request.session.get('user_id', none))

                if user.balance < request.POST.order_bonus:
                    __error__['message'] = '余额不足'
                    return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')

                user = User.objects.get(id=request.session.get('user_id', none))
                user.balance -= request.POST.order_bonus
                user.save()

                order = Order()
                order.order_type = request.POST.order_type
                order.order_bonus = request.POST.order_bonus
                order.order_detail = request.POST.order_detail
                order.order_publishDate = request.POST.order_publishDate
                order.order_description = request.POST.order_description
                order.save()

                publish_order = PublishOrder()
                publish_order.user_id = request.session.get('user_id', none)
                publish_order.order_id = order.order_id
                publish_order.save()
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')        
            
    else: 
        return HttpResponse(json.dumps(notLogin), content_type='application/json', charset='utf-8')

    

@csrf_exempt
def order_pick(request):
    if request.session.get('login', none):
        if request.method == 'POST':
            try:
                order = Order.objects.filter(id=request.POST.order_id)
                order.order_pick = 1
                order.save()

                pick_order = PickOrder()
                pick_order.user_id = request.session.get('user_id', none)
                pick_order.order_id = request.POST.order_id
                pick_order.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')        
    else: 
        return HttpResponse(json.dumps(notLogin), content_type='application/json', charset='utf-8')


@csrf_exempt
def order_complish(request):
    if request.session.get('login', none):
        if request.method == 'POST':
            try:
                order = Order.objects.get(order_id=request.POST.order_id)
                order.order_complish = 1
                order.order_complishDate = request.POST.order_complishDate
                order.save()

                publish_order = PublishOrder.objects.get(order_id=request.POST.order_id)
                publish_user = User.objects.get(id=publish_order.user_id)
                publish_user.balance -= order.order_bonus
                
                pick_order = PickOrder.objects.get(order_id=request.POST.order_id)
                pick_user = User.objects.get(id=pick_order.user_id)
                pick_user.balance += order.order_bonus

                order = Order.objects.filter(order_id=request.POST.order_id)

                pickBill = Bill()
                pickBill.user_id = pick_order.user_id
                pickBill.bill_type = 1
                pickBill.bill_number = order.order_bonus
                pickBill.bill_description = order.order_description
                pickBill.bill_time = request.POST.order_complishDate
                pickBill.save()

                publishBill = Bill()
                publishBill.user_id = publish_order.user_id
                publishBill.bill_type = 1
                publishBill.bill_number = order.order_bonus
                publishBill.bill_description = order.order_description
                publishBill.bill_time = request.POST.order_complishDate
                publishBill.save()

                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')        
    else: 
        return HttpResponse(json.dumps(notLogin), content_type='application/json', charset='utf-8')
