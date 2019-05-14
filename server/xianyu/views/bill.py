from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
from time import strftime, localtime

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
def bill(request):
    if request.session.get('is_login', None) == True:
        if request.method == 'GET':
            try:
                filter_bills = models.Bill.objects.filter(user_id = request.session.get('user_id'))

                # 将QuerySet转换为数组
                bills = []
                for i in filter_bills: 
                    bills.append({
                        "bill_id":              i.bill_id,
                        "user_id":              i.user_id,
                        "bill_type":            i.bill_type,
                        "bill_number":          i.bill_number,
                        "bill_description":     i.bill_description,
                        "bill_time":            i.bill_time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                __ok__['data'] = {
                    'bills': bills
                }
                
                return HttpResponse(json.dumps(__ok__), content_type='application/json', charset='utf-8')
            except Exception as exc:
                print(exc)
                return HttpResponse(json.dumps(__error__), content_type='application/json', charset='utf-8')
    else: 
        return HttpResponse(json.dumps(__notLogin__), content_type='application/json', charset='utf-8')