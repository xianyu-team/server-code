from django.test import TestCase
from xianyu import models
from django.test.client import Client

class UserTest(TestCase):

    # 初始化
    def setUp(self):
        # 创建用户
        user = models.User()
        user.user_phone = '15626259034'
        user.user_password = '123456'
        user.save()

        # 测试密码登录功能
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        response = self.client.post('/user/password/session', data=post_data, content_type='application/json')
        __ok__ = {
            'code': 200,
            'message': 'OK',
            'data': {
                'user_fillln': 0
            }
        }
        self.assertEqual(response.json(), __ok__)



    # 测试退出登录功能
    def test_user_session(self):
        response = self.client.delete('/user/session')
        __ok__ = {
            'code': 200,
            'message': 'OK',
            'data': {}
        }
        self.assertEqual(response.json(), __ok__)


    # 测试完善和获取个人信息功能
    def test_user_profile(self):
        # 测试完善个人信息功能
        put_data = {
            "user_icon": "",
            "student_name": "陈xx",
            "student_university": "中山大学",
            "student_academy": "数据科学与计算机学院",
            "student_number": "16340034",
            "student_gender": 1
        }
        response = self.client.put('/user/profile', data=put_data, content_type='application/json')
        __ok__ = {
            'code': 200,
            'message': 'OK',
            'data': {}
        }
        self.assertEqual(response.json(), __ok__)

        # 测试获取个人信息功能
        response = self.client.get('/user/profile')
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'user': {
                    'user_id': 1, 
                    'user_phone': '15626259034',
                    'user_icon': '', 
                    'user_balance': 100, 
                    'user_fillln': 1
                }, 
                'student': {
                    'student_id': 1, 
                    'user_id': 1, 
                    'student_number': 16340034, 
                    'student_name': '陈xx', 
                    'student_university': '中山大学', 
                    'student_academy': '数据科学与计算机学院', 
                    'student_gender': 1
                }
            }
        }
        self.assertEqual(response.json(), get_data)
        
    
    # 测试获取当前余额功能(user3)
    def test_user_balance(self):
        response = self.client.put('/user/balance')
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'user_balance': 100
            }
        }
        self.assertEqual(response.json(), get_data)

    # 测试获取发布任务的属性
    def test_user_tasks(self):
        #任务列表添加任务
        task = models.Task()
        task.user_id = 1
        task.task_type = 0
        task.task_sketch = "帮忙拿快递"
        task.task_bonus = 1
        task.save()

        #用户发布列表添加任务
        publishTask = models.PublishTask()
        publishTask.user_id = 1
        publishTask.task_id = 1
        publishTask.save()

        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'tasks': [{
                    'task_id': 1, 
                    'user_id': 1, 
                    'task_type': 0, 
                    'task_sketch': '帮忙拿快递', 
                    'task_bonus': 1, 
                    'task_publishDate': '2019-05-17 11:27:11'
                }]
            }
        }

        response = self.client.get('/user/tasks/0')
        self.assertEqual(response.json(), get_data)

  
    # 测试根据用户id获取用户信息
    def test_user_batch_information(self):
        post_data = {
            "user_ids":  [
                {
                    "user_id": 1
                }
            ]  
        }

        response = self.client.post('/user/batch/information', data=post_data, content_type='application/json')
        print(response.json())
