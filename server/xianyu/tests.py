'''
以下是各个API的单元测试
'''

from django.test import TestCase
from xianyu import models

class UserTest(TestCase):
    '''测试用户API'''
    def setUp(self):
        '''初始化'''
        pass


    def test_post_user(self):
        '''创建用户'''
        pass


    def test_put_user_profile(self):
        '''测试完善或修改当前用户的信息'''
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

    def test_post_user_password_session(self):
        '''测试用户密码登录'''
        pass
