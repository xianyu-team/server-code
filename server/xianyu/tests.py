'''
以下是各个API的单元测试
'''

from django.test import TestCase
from xianyu import models


class UserTest(TestCase):
    '''测试用户API'''
    def setUp(self):
        '''测试函数执行前执行'''
        pass


    def test_post_user(self):
        '''创建用户'''
        pass


    def test_put_user_profile(self):
        '''测试完善或修改当前用户的信息'''
        self.maxDiff = None
        
        new_user = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user.save()

        put_user_profile_data = {
            "user_icon": "",
            "student_name": "陈xx",
            "student_university": "中山大学",
            "student_academy": "数据科学与计算机学院",
            "student_number": "16340034",
            "student_gender": 1
        }
        response = self.client.put('/user/profile', data=put_user_profile_data, content_type='application/json')
        __notlogin__ = {
            'code': 401,
            'message': '未登录'
        }

        # 检验未登录状态
        self.assertEqual(response.json(), __notlogin__)
        # 检验 user_fillln = 0
        self.assertEqual(new_user.user_fillln, 0)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')
        response = self.client.put('/user/profile', data=put_user_profile_data, content_type='application/json')

        __ok__ = {
            "code": 200,
            "message": "OK",
            "data": {}
        }

        # 检验 ok 状态
        self.assertEqual(response.json(), __ok__)
        # 检验 user_fillln = 1
        self.assertEqual(new_user.user_fillln, 1)


    def test_get_user_profile(self):
        '''测试获取当前用户的信息'''
        self.maxDiff = None

        new_user = models.User(
            user_phone='15989061915',
            user_password='123456',
            user_icon=bytes('', encoding='utf-8'),
            user_fillln=1
        )
        new_user.save()
        new_user_id = new_user.user_id

        new_student = models.Student(
            user_id=new_user_id,
            student_number='16340034',
            student_name='陈xx',
            student_university='中山大学',
            student_academy='数据科学与计算机学院',
            student_gender=1
        )
        new_student.save()
        new_student_id = new_student.student_id

        __notlogin__ = {
            'code': 401,
            'message': '未登录'
        }

        response = self.client.get('/user/profile', content_type='application/json')

        # 检验未登录状态
        self.assertEqual(response.json(), __notlogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')
        response = self.client.get('/user/profile', content_type='application/json')

        __ok__ = {
            "code": 200,
            "message": 'OK',
            "data": {
                "user": {
                    "user_id": new_user_id,
                    "user_phone": '15989061915',
                    "user_icon": '',
                    "user_balance": 100,
                    "user_fillln": 1
                },
                "student": {
                    "student_id": new_student_id,
                    "user_id": new_user_id,
                    "student_number": '16340034',
                    "student_name": '陈xx',
                    "student_university": '中山大学',
                    "student_academy": '数据科学与计算机学院',
                    "student_gender": 1
                }
            }
        }

        # 检验 ok 状态
        self.assertEqual(response.json(), __ok__)


    def test_post_user_password_session(self):
        '''测试用户密码登录'''
        pass


    def tearDown(self):
        '''测试函数执行后执行'''
        # 每个测试函数执行后都删除所有数据
        models.User.objects.all().delete()
        models.Student.objects.all().delete()
        models.Task.objects.all().delete()
        models.Following.objects.all().delete()
        models.Fan.objects.all().delete()
        models.PickTask.objects.all().delete()
        models.PublishTask.objects.all().delete()
        models.Question.objects.all().delete()
        models.Questionnaire.objects.all().delete()
        models.Answer.objects.all().delete()
        models.AnswerSheet.objects.all().delete()
        models.Bill.objects.all().delete()
        models.Delivery.objects.all().delete()
