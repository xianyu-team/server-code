'''
以下是各个API的单元测试
'''


from django.test import TestCase
from xianyu import models
from time import strftime, localtime
import time
import string
import random

# 注意data字段，因为__ok__是全局变量，所以每次返回时都要对data进行赋值，即使赋值的是个空对象，以覆盖原来的data值
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


class SmsTest(TestCase):
    '''测试短信API'''
    def setUp(self):
        '''测试函数执行前执行'''
        pass


    def test_get_sms_verification_code(self):
        '''测试向手机发送验证码'''
        self.maxDiff = None

        user_phone = '15989061915'
        response = self.client.get('/sms/verification_code/' + user_phone, content_type='application/json')

        code = self.client.session[user_phone + '_verification_code']

        __ok__['data'] = {
            "verification_code": code
        }

        # 检验成功获取验证码
        self.assertEqual(response.json(), __ok__)


    '''
    def test_get_sms_verification_code(self):
        测试验证手机验证码
        self.maxDiff = None

        # 产生 4 位随机数
        seeds = string.digits
        random_str = []
        for i in range(4):
            random_str.append(random.choice(seeds))
        verification_code = "".join(random_str)

        user_phone = '15989061915'

        self.client.session[user_phone + '_verification_code'] = verification_code
        self.client.session[user_phone + '_get_verification_code_time'] = time.time()
        
        post_data = {
            "user_phone": user_phone,
            "verification_code": verification_code
        }
        
        response = self.client.post('/sms/verification', data=post_data, content_type='application/json')
        # 检验成功验证验证码
        print('--------------------------------------')
        print(self.client.session.get(user_phone + '_verification_code', 0))
        print(verification_code)
        print('--------------------------------------')
        __ok__['data'] = {}
        self.assertEqual(response.json(), __ok__)

        post_data = {
            "user_phone": user_phone,
            "verification_code": verification_code + '1'
        }
        response = self.client.post('/sms/verification', data=post_data, content_type='application/json')
        # 检验不成功验证验证码
        self.assertEqual(response.json(), __wrongVerification__)

        post_data = {
            "user_phone": user_phone + '1',
            "verification_code": verification_code
        }
        response = self.client.post('/sms/verification', data=post_data, content_type='application/json')
        # 检验不成功验证验证码
        self.assertEqual(response.json(), __wrongVerification__)
    '''


    def tearDown(self):
        '''测试函数执行后执行'''
        # 每个测试函数执行后都删除所有数据
        pass
    

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

        # 检验未登录状态
        self.assertEqual(response.json(), __notLogin__)

        get_user = models.User.objects.get(user_phone=15989061915)

        # 检验 user_fillln = 0
        self.assertEqual(get_user.user_fillln, 0)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.put('/user/profile', data=put_user_profile_data, content_type='application/json')

        data = {}
        __ok__['data'] = data

        # 检验 ok 状态
        self.assertEqual(response.json(), __ok__)

        get_user = models.User.objects.get(user_phone=15989061915)

        # 检验 user_fillln = 1
        self.assertEqual(get_user.user_fillln, 1)

        student_data = {
            "user_id": new_user.user_id,
            "student_name": "陈xx",
            "student_university": "中山大学",
            "student_academy": "数据科学与计算机学院",
            "student_number": "16340034",
            "student_gender": 1
        }
        get_student = models.Student.objects.get(user_id=new_user.user_id)
        get_student_data = {
            "user_id": get_student.user_id,
            "student_name": get_student.student_name,
            "student_university": get_student.student_university,
            "student_academy": get_student.student_academy,
            "student_number": get_student.student_number,
            "student_gender": get_student.student_gender
        }

        # 检验 student 是否正确添加数据，student_id 不用验证
        self.assertEqual(student_data, get_student_data)
    
    
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

        response = self.client.get('/user/profile', content_type='application/json')

        # 检验未登录状态
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.get('/user/profile', content_type='application/json')

        data = {
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
        __ok__['data'] = data

        # 检验 ok 状态
        self.assertEqual(response.json(), __ok__)
    

    def test_post_user_password_session(self):
        '''测试用户密码登录'''
        self.maxDiff = None

        new_user = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user.save()

        post_user_session_data = {
            "user_phone": "1598906191",
            "user_password": "123456"
        }
        response = self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        # 验证该用户不存在
        self.assertEqual(response.json(), __notExistUser__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "12345"
        }
        response = self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        # 验证密码错误
        self.assertEqual(response.json(), __wrongPassword__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        response = self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        data = {
            'user_fillln': 0
        }
        __ok__['data'] = data

        # 验证OK
        self.assertEqual(response.json(), __ok__)

        # 验证此时确实是已登录状态
        self.assertEqual(self.client.session['is_login'], True)
    
    
    def test_delete_user_session(self):
        '''测试用户退出登录'''
        self.maxDiff = None

        new_user = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user.save()

        response = self.client.delete('/user/session', content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.delete('/user/session', content_type='application/json')

        data = {}
        __ok__['data'] = data

        # 验证OK
        self.assertEqual(response.json(), __ok__)

        # 退出登录后，再验证此时是否确实是未登录状态
        self.assertEqual(self.client.session.get('is_login', None), None)


    def test_get_user_balance(self):
        '''测试获取当前用户的余额'''
        self.maxDiff = None

        new_user = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user.save()

        response = self.client.get('/user/balance', content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.get('/user/balance', content_type='application/json')

        data = {
            'user_balance': 100
        }
        __ok__['data'] = data

        # 验证OK
        self.assertEqual(response.json(), __ok__)


    def test_get_user_task_t_type(self):
        '''测试获得当前用户发布/领取的所有任务id和共同属性'''
        self.maxDiff = None
        # 新建三个用户
        new_user1 = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user1.save()
        new_user1_id = new_user1.user_id

        new_user2 = models.User(
            user_phone='15989060001',
            user_password='123456'
        )
        new_user2.save()
        new_user2_id = new_user2.user_id

        new_user3 = models.User(
            user_phone='15989060002',
            user_password='123456'
        )
        new_user3.save()
        new_user3_id = new_user3.user_id
        # 新建4个任务
        new_task1 = models.Task(
            user_id=new_user1_id,
            task_type=0,
            task_sketch='帮忙拿快递',
            task_bonus=2
        )
        new_task1.save()
        new_task1_id = new_task1.task_id

        new_task2 = models.Task(
            user_id=new_user1_id,
            task_type=1,
            task_sketch='帮忙填问卷',
            task_bonus=1
        )
        new_task2.save()
        new_task2_id = new_task2.task_id

        new_task3 = models.Task(
            user_id=new_user2_id,
            task_type=0,
            task_sketch='拿快递',
            task_bonus=2
        )
        new_task3.save()
        new_task3_id = new_task3.task_id

        new_task4 = models.Task(
            user_id=new_user3_id,
            task_type=1,
            task_sketch='填问卷',
            task_bonus=1
        )
        new_task4.save()
        new_task4_id = new_task4.task_id
        # 新建用户发布的任务 id 表
        new_publish_task1 = models.PublishTask(
            user_id=new_user1_id,
            task_id=new_task1_id
        )
        new_publish_task1.save()

        new_publish_task2 = models.PublishTask(
            user_id=new_user1_id,
            task_id=new_task2_id
        )
        new_publish_task2.save()
        # 新建用户领取的任务 id 表
        new_pick_task1 = models.PickTask(
            user_id=new_user1_id,
            task_id=new_task3_id
        )
        new_pick_task1.save()

        new_pick_task2 = models.PickTask(
            user_id=new_user1_id,
            task_id=new_task4_id
        )
        new_pick_task2.save()

        response = self.client.post('/user/tasks/0', content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.get('/user/tasks/0', content_type='application/json')

        data = {
            'tasks': [
                {
                    'task_id': new_task2_id,
                    'user_id': new_user1_id,
                    'task_type': 1,
                    'task_sketch': '帮忙填问卷',
                    'task_bonus': 1,
                    'task_publishDate': new_task2.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'task_id': new_task1_id,
                    'user_id': new_user1_id,
                    'task_type': 0,
                    'task_sketch': '帮忙拿快递',
                    'task_bonus': 2,
                    'task_publishDate': new_task1.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
        }
        __ok__['data'] = data

        # 验证用户发布的任务 OK 状态
        self.assertEqual(response.json(), __ok__)

        response = self.client.get('/user/tasks/1', content_type='application/json')

        data = {
            'tasks': [
                {
                    'task_id': new_task4_id,
                    'user_id': new_user3_id,
                    'task_type': 1,
                    'task_sketch': '填问卷',
                    'task_bonus': 1,
                    'task_publishDate': new_task4.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'task_id': new_task3_id,
                    'user_id': new_user2_id,
                    'task_type': 0,
                    'task_sketch': '拿快递',
                    'task_bonus': 2,
                    'task_publishDate': new_task3.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
        }
        __ok__['data'] = data

        # 验证用户领取的任务 OK 状态
        self.assertEqual(response.json(), __ok__)

    
    def test_post_batch_information(self):
        '''测试根据用户/关注的人/粉丝id批量获取用户信息(user_id/following_id/fan_id都适用)'''
        self.maxDiff = None
        # 新建三个用户
        new_user1 = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user1.save()
        new_user1_id = new_user1.user_id

        new_user2 = models.User(
            user_phone='15989060002',
            user_password='123456',
            user_icon=bytes('', encoding='utf-8'),
            user_fillln=1
        )
        new_user2.save()
        new_user2_id = new_user2.user_id

        new_user3 = models.User(
            user_phone='15989060003',
            user_password='123456',
            user_icon=bytes('', encoding='utf-8'),
            user_fillln=1
        )
        new_user3.save()
        new_user3_id = new_user3.user_id

        # 完善用户2和3的学生信息
        new_student2 = models.Student(
            user_id=new_user2_id,
            student_number='16340002',
            student_name='陈2',
            student_university='中山大学',
            student_academy='数据科学与计算机学院',
            student_gender=1
        )
        new_student2.save()

        new_student3 = models.Student(
            user_id=new_user3_id,
            student_number='16340003',
            student_name='陈3',
            student_university='中山大学',
            student_academy='数据科学与计算机学院',
            student_gender=0
        )
        new_student3.save()

        post_user_batch_information_data = {
            "user_ids":  [
                {
                    "user_id": new_user2_id
                },
                {
                    "user_id": new_user3_id
                }
            ]
        }

        response = self.client.post('/user/batch/information', data=post_user_batch_information_data, content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.post('/user/batch/information', data=post_user_batch_information_data, content_type='application/json')

        data = {
            'users': [
                {
                    'user': {
                        'user_id': new_user2_id,
                        'user_phone': '15989060002',
                        'user_icon': '',
                        'user_balance': 100,
                        'user_fillln': 1
                    },
                    'student': {
                        'student_id': new_student2.student_id,
                        'user_id': new_user2_id,
                        'student_number': '16340002',
                        'student_name': '陈2',
                        'student_university': '中山大学',
                        'student_academy': '数据科学与计算机学院',
                        'student_gender': 1
                    }
                },
                {
                    'user': {
                        'user_id': new_user3_id,
                        'user_phone': '15989060003',
                        'user_icon': '',
                        'user_balance': 100,
                        'user_fillln': 1
                    },
                    'student': {
                        'student_id': new_student3.student_id,
                        'user_id': new_user3_id,
                        'student_number': '16340003',
                        'student_name': '陈3',
                        'student_university': '中山大学',
                        'student_academy': '数据科学与计算机学院',
                        'student_gender': 0
                    }
                }
            ]
        }
        __ok__['data'] = data

        # 验证用户领取的任务 OK 状态
        self.assertEqual(response.json(), __ok__)


    def test_post_user_following(self):
        '''测试当前用户关注其它用户'''
        self.maxDiff = None
        # 新建三个用户
        new_user1 = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user1.save()
        new_user1_id = new_user1.user_id

        new_user2 = models.User(
            user_phone='15989060002',
            user_password='123456',
        )
        new_user2.save()
        new_user2_id = new_user2.user_id

        new_user3 = models.User(
            user_phone='15989060003',
            user_password='123456',
        )
        new_user3.save()
        new_user3_id = new_user3.user_id

        post_user_following_data = {
            "user_id": new_user1_id
        }

        response = self.client.post('/user/following', data=post_user_following_data, content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.post('/user/following', data=post_user_following_data, content_type='application/json')

        # 验证关注自己的错误
        self.assertEqual(response.json(), __followMyselfError__)

        post_user_following_data = {
            "user_id": new_user2_id
        }
        response = self.client.post('/user/following', data=post_user_following_data, content_type='application/json')
        post_user_following_data = {
            "user_id": new_user3_id
        }
        response = self.client.post('/user/following', data=post_user_following_data, content_type='application/json')

        data = {}
        __ok__['data'] = data

        # 验证关注用户的 ok 状态
        self.assertEqual(response.json(), __ok__)

        following_list = [
            {
                'user_id': new_user1_id,
                'following_id': new_user2_id
            },
            {
                'user_id': new_user1_id,
                'following_id': new_user3_id
            }
        ]
        filter_followings = models.Following.objects.filter(user_id=new_user1_id)
        filter_following_list = []
        for filter_following in filter_followings:
            filter_following_list.append({
                'user_id': filter_following.user_id,
                'following_id': filter_following.following_id
            })

        # 验证数据库里是否正确添加了关注列表
        self.assertEqual(following_list, filter_following_list)

        fan_list = [
            {
                'user_id': new_user2_id,
                'fan_id': new_user1_id
            },
            {
                'user_id': new_user3_id,
                'fan_id': new_user1_id
            }
        ]
        filter_fans = models.Fan.objects.filter(fan_id=new_user1_id)
        filter_fan_list = []
        for filter_fan in filter_fans:
            filter_fan_list.append({
                'user_id': filter_fan.user_id,
                'fan_id': filter_fan.fan_id
            })

        # 验证数据库里是否正确添加了粉丝列表
        self.assertEqual(fan_list, filter_fan_list)


    def delete_user_following(self):
        '''测试当前用户取关其它用户'''
        self.maxDiff = None
        # 新建三个用户
        new_user1 = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user1.save()
        new_user1_id = new_user1.user_id

        new_user2 = models.User(
            user_phone='15989060002',
            user_password='123456',
        )
        new_user2.save()
        new_user2_id = new_user2.user_id

        new_user3 = models.User(
            user_phone='15989060003',
            user_password='123456',
        )
        new_user3.save()
        new_user3_id = new_user3.user_id

        new_following1 = models.Following(
            user_id=new_user1_id,
            following_id=new_user2_id
        ).save()

        new_following2 = models.Following(
            user_id=new_user1_id,
            following_id=new_user3_id
        ).save()

        new_fan1 = models.Fan(
            user_id=new_user2_id,
            fan_id=new_user1_id
        ).save()

        new_fan2 = models.Fan(
            user_id=new_user3_id,
            fan_id=new_user1_id
        ).save()

        delete_user_following_data = {
            'user_id': new_user2_id
        }

        response = self.client.delete('/user/following', data=delete_user_following_data, content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.delete('/user/following', data=delete_user_following_data, content_type='application/json')

        # 验证 ok 状态
        data= {}
        __ok__['data'] = data
        self.assertEqual(response.json(), __ok__)

        following_list = [
            {
                'user_id': new_user1_id,
                'following_id': new_user3_id
            }
        ]
        filter_followings = models.Following.objects.filter(user_id=new_user1_id)
        filter_following_list = []
        for filter_following in filter_followings:
            filter_following_list.append({
                'user_id': filter_following.user_id,
                'following_id': filter_following.following_id
            })

        # 验证数据库 following 表，是否取关了用户2，只关注用户3
        self.assertEqual(following_list, filter_following_list)

        fan_list = [
            {
                'user_id': new_user3_id,
                'fan_id': new_user1_id
            }
        ]
        filter_fans = models.Fan.objects.filter(fan_id=new_user1_id)
        filter_fan_list = []
        for filter_fan in filter_fans:
            filter_fan_list.append({
                'user_id': filter_fan.user_id,
                'fan_id': filter_fan.fan_id
            })

        # 验证数据库 fan 表，用户1是否取关了用户2，只关注用户3
        self.assertEqual(fan_list, filter_fan_list)


    def test_get_user_followings(self):
        '''测试获取当前用户关注的所有用户的id'''
        self.maxDiff = None
        # 新建三个用户
        new_user1 = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user1.save()
        new_user1_id = new_user1.user_id

        new_user2 = models.User(
            user_phone='15989060002',
            user_password='123456',
        )
        new_user2.save()
        new_user2_id = new_user2.user_id

        new_user3 = models.User(
            user_phone='15989060003',
            user_password='123456',
        )
        new_user3.save()
        new_user3_id = new_user3.user_id

        new_following1 = models.Following(
            user_id=new_user1_id,
            following_id=new_user2_id
        ).save()

        new_following2 = models.Following(
            user_id=new_user1_id,
            following_id=new_user3_id
        ).save()

        new_fan1 = models.Fan(
            user_id=new_user2_id,
            fan_id=new_user1_id
        ).save()

        new_fan2 = models.Fan(
            user_id=new_user3_id,
            fan_id=new_user1_id
        ).save()

        response = self.client.get('/user/followings', content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.get('/user/followings', content_type='application/json')

        data = {
            'followings': [
                {
                    'following_id': new_user2_id
                },
                {
                    'following_id': new_user3_id
                }
            ]
        }
        __ok__['data'] = data

        # 验证 ok
        self.assertEqual(response.json(), __ok__)


    def test_get_fans(self):
        '''测试获取当前用户的所有粉丝的id'''
        self.maxDiff = None
        # 新建三个用户
        new_user1 = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user1.save()
        new_user1_id = new_user1.user_id

        new_user2 = models.User(
            user_phone='15989060002',
            user_password='123456',
        )
        new_user2.save()
        new_user2_id = new_user2.user_id

        new_user3 = models.User(
            user_phone='15989060003',
            user_password='123456',
        )
        new_user3.save()
        new_user3_id = new_user3.user_id

        new_following1 = models.Following(
            user_id=new_user2_id,
            following_id=new_user1_id
        ).save()

        new_following2 = models.Following(
            user_id=new_user3_id,
            following_id=new_user1_id
        ).save()

        new_fan1 = models.Fan(
            user_id=new_user1_id,
            fan_id=new_user2_id
        ).save()

        new_fan2 = models.Fan(
            user_id=new_user1_id,
            fan_id=new_user3_id
        ).save()

        response = self.client.get('/user/fans', content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.get('/user/fans', content_type='application/json')

        data = {
            'fans': [
                {
                    'fan_id': new_user2_id
                },
                {
                    'fan_id': new_user3_id
                }
            ]
        }
        __ok__['data'] = data

        # 验证 ok
        self.assertEqual(response.json(), __ok__)
    

    def test_get_user_user_id_followings(self):
        '''测试获取某个用户关注的所有用户的id'''
        self.maxDiff = None
        # 新建三个用户
        new_user1 = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user1.save()
        new_user1_id = new_user1.user_id

        new_user2 = models.User(
            user_phone='15989060002',
            user_password='123456',
        )
        new_user2.save()
        new_user2_id = new_user2.user_id

        new_user3 = models.User(
            user_phone='15989060003',
            user_password='123456',
        )
        new_user3.save()
        new_user3_id = new_user3.user_id

        new_following1 = models.Following(
            user_id=new_user1_id,
            following_id=new_user2_id
        ).save()

        new_following2 = models.Following(
            user_id=new_user1_id,
            following_id=new_user3_id
        ).save()

        new_fan1 = models.Fan(
            user_id=new_user2_id,
            fan_id=new_user1_id
        ).save()

        new_fan2 = models.Fan(
            user_id=new_user3_id,
            fan_id=new_user1_id
        ).save()

        response = self.client.get('/user/followings', content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.get('/user/' + new_user1_id.__str__() + '/followings', content_type='application/json')

        data = {
            'followings': [
                {
                    'following_id': new_user2_id
                },
                {
                    'following_id': new_user3_id
                }
            ]
        }
        __ok__['data'] = data

        # 验证 ok
        self.assertEqual(response.json(), __ok__)


    def test_get_fans(self):
        '''测试获取某个用户的所有粉丝的id'''
        self.maxDiff = None
        # 新建三个用户
        new_user1 = models.User(
            user_phone='15989061915',
            user_password='123456'
        )
        new_user1.save()
        new_user1_id = new_user1.user_id

        new_user2 = models.User(
            user_phone='15989060002',
            user_password='123456',
        )
        new_user2.save()
        new_user2_id = new_user2.user_id

        new_user3 = models.User(
            user_phone='15989060003',
            user_password='123456',
        )
        new_user3.save()
        new_user3_id = new_user3.user_id

        new_following1 = models.Following(
            user_id=new_user2_id,
            following_id=new_user1_id
        ).save()

        new_following2 = models.Following(
            user_id=new_user3_id,
            following_id=new_user1_id
        ).save()

        new_fan1 = models.Fan(
            user_id=new_user1_id,
            fan_id=new_user2_id
        ).save()

        new_fan2 = models.Fan(
            user_id=new_user1_id,
            fan_id=new_user3_id
        ).save()

        response = self.client.get('/user/fans', content_type='application/json')

        # 验证未登录
        self.assertEqual(response.json(), __notLogin__)

        post_user_session_data = {
            "user_phone": "15989061915",
            "user_password": "123456"
        }
        self.client.post('/user/password/session', data=post_user_session_data, content_type='application/json')

        response = self.client.get('/user/' + new_user1_id.__str__() + '/fans', content_type='application/json')

        data = {
            'fans': [
                {
                    'fan_id': new_user2_id
                },
                {
                    'fan_id': new_user3_id
                }
            ]
        }
        __ok__['data'] = data

        # 验证 ok
        self.assertEqual(response.json(), __ok__)


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
    


class TaskTest(TestCase):
    
    # 测试获取任务大厅所有任务的id和共同属性
    def test_task(self):
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建用户2
        user2 = models.User()
        user2.user_phone = '18928610979'
        user2.user_password = '123456'
        user2.save()

        # 用户1关注用户2
        fan1 = models.Fan()
        fan1.user_id = user1.user_id 
        fan1.fan_id = user2.user_id
        fan1.save()

        # 创建任务1
        task1 = models.Task()
        task1.user_id = user1.user_id
        task1.task_type = 0
        task1.task_sketch = "帮忙拿快递"
        task1.task_bonus = 2
        task1.save()

        # 睡眠3s, 以区分两个任务的时间
        time.sleep(3)

        # 创建任务2
        task2 = models.Task()
        task2.user_id = user2.user_id
        task2.task_type = 1
        task2.task_sketch = "大学生运动爱好调查"
        task2.task_bonus = 1
        task2.save()

        # 测试按最新发布排序
        response = self.client.get('/task/0')    
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'tasks': [
                    {
                        'task_id': task2.task_id, 
                        'user_id': user2.user_id, 
                        'task_type': 1, 
                        'task_sketch': '大学生运动爱好调查', 
                        'task_bonus': 1, 
                        'task_publishDate': task2.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                    }, 
                    {
                        'task_id': task1.task_id, 
                        'user_id': user1.user_id, 
                        'task_type': 0, 
                        'task_sketch': '帮忙拿快递', 
                        'task_bonus': 2, 
                        'task_publishDate': task1.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
            }
        }
        self.assertEqual(response.json(), get_data)   

        # 测试按关注用户排序
        response = self.client.get('/task/1') 
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'tasks': [
                    {
                        'task_id': task2.task_id, 
                        'user_id': user2.user_id, 
                        'task_type': 1, 
                        'task_sketch': '大学生运动爱好调查', 
                        'task_bonus': 1, 
                        'task_publishDate': task2.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
            }
        }
        self.assertEqual(response.json(), get_data)     

        # 测试按价格最高排序
        response = self.client.get('/task/2') 
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'tasks': [
                    {
                        'task_id': task1.task_id, 
                        'user_id': user1.user_id,  
                        'task_type': 0, 
                        'task_sketch': '帮忙拿快递', 
                        'task_bonus': 2, 
                        'task_publishDate': task1.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                    }, 
                    {
                        'task_id': task2.task_id, 
                        'user_id': user2.user_id, 
                        'task_type': 1, 
                        'task_sketch': '大学生运动爱好调查', 
                        'task_bonus': 1, 
                        'task_publishDate': task2.task_publishDate.strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
            }
        }
        self.assertEqual(response.json(), get_data) 

        # 删除数据项
        user1.delete()
        user2.delete()
        fan1.delete()
        task1.delete()
        task2.delete()
        
    
    # 测试根据任务id获取跑腿的详细信息
    def test_task_delivery_detail(self):
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建任务1
        task1 = models.Task()
        task1.user_id = user1.user_id
        task1.task_type = 0
        task1.task_sketch = "帮忙拿快递"
        task1.task_bonus = 2
        task1.save()

        # 创建递送1
        delivery1 = models.Delivery()
        delivery1.task_id = task1.task_id
        delivery1.delivery_detail = "菜鸟驿站5号柜包裹码xxxx-xxxx"
        delivery1.save()

        response = self.client.get('/task/delivery/detail/' + str(task1.task_id))
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'delivery': {
                    'delivery_id': delivery1.delivery_id, 
                    'task_id': task1.task_id, 
                    'delivery_detail': '菜鸟驿站5号柜包裹码xxxx-xxxx', 
                    'delivery_picked': 0, 
                    'delivery_complished': 0, 
                    'delivery_complishDate': 0
                }
            }
        }
        self.assertEqual(response.json(), get_data) 

        # 删除数据项
        user1.delete()
        task1.delete()
        delivery1.delete()



    # 测试根据任务id获取问卷和题目的详细信息
    def test_task_questionnaire(self):
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建任务1
        task1 = models.Task()
        task1.user_id = user1.user_id
        task1.task_type = 1
        task1.task_sketch = "大学生运动爱好调查"
        task1.task_bonus = 1
        task1.save()

        # 创建问卷1
        questionnaire1 = models.Questionnaire()
        questionnaire1.task_id = task1.task_id
        questionnaire1.questionnaire_number = 2
        questionnaire1.save()

        # 创建题目1
        question1 = models.Question()
        question1.questionnaire_id = questionnaire1.questionnaire_id 
        question1.question_description = "你的姓名"
        question1.question_type = 2
        question1.question_a = ""
        question1.question_b = ""
        question1.question_c = ""
        question1.question_d = ""
        question1.save()

        # 创建题目2
        question2 = models.Question()
        question2.questionnaire_id = questionnaire1.questionnaire_id 
        question2.question_description = "你喜欢什么运动?"
        question2.question_type = 1
        question2.question_a = "篮球"
        question2.question_b = "羽毛球"
        question2.question_c = "乒乓球"
        question2.question_d = "排球" 
        question2.save()

        response = self.client.get('/task/questionnaire/detail/' + str(task1.task_id))
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'questionnaire': {
                    'questionnaire_id': questionnaire1.questionnaire_id, 
                    'task_id': task1.task_id, 
                    'questionnaire_closed': 0, 
                    'questionnaire_deadline': questionnaire1.questionnaire_deadline.strftime('%Y-%m-%d %H:%M:%S'), 
                    'questions': [
                        {
                            'question_id': question1.question_id, 
                            'questionnaire_id': questionnaire1.questionnaire_id, 
                            'question_description': '你的姓名', 
                            'question_type': 2, 
                            'question_a': '', 
                            'question_b': '', 
                            'question_c': '', 
                            'question_d': ''
                        }, 
                        {
                            'question_id': question2.question_id, 
                            'questionnaire_id': questionnaire1.questionnaire_id, 
                            'question_description': '你喜欢什么运动?', 
                            'question_type': 1, 
                            'question_a': '篮球', 
                            'question_b': '羽毛球', 
                            'question_c': '乒乓球', 
                            'question_d': '排球'
                        }
                    ]
                }
            }
        }
        self.assertEqual(response.json(), get_data) 

        # 删除数据项
        user1.delete()
        task1.delete()
        questionnaire1.delete()
        question1.delete()
        question2.delete()

    
    # 测试接受一个跑腿的任务
    def test_task_acceptance(self):
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建任务1
        task1 = models.Task()
        task1.user_id = user1.user_id
        task1.task_type = 0
        task1.task_sketch = "帮忙拿快递"
        task1.task_bonus = 2
        task1.save()

        # 创建递送1
        delivery1 = models.Delivery()
        delivery1.task_id = task1.task_id
        delivery1.delivery_detail = "菜鸟驿站5号柜包裹码xxxx-xxxx"
        delivery1.save()


        post_data = {
            "task_id": task1.task_id
        }
        response = self.client.post('/task/acceptance', data=post_data, content_type='application/json')

        get_delivery = models.Delivery.objects.get(task_id = task1.task_id)

        self.assertEqual(get_delivery.delivery_picked, 1)

        # 删除数据项 
        pickTask1 = models.PickTask.objects.get(task_id = task1.task_id)
        pickTask1.delete()
        user1.delete()
        task1.delete()
        delivery1.delete()


    # 测试发布者取消一个跑腿的任务
    def test_task_delivery_delete(self):
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建任务1
        task1 = models.Task()
        task1.user_id = user1.user_id
        task1.task_type = 0
        task1.task_sketch = "帮忙拿快递"
        task1.task_bonus = 2
        task1.save()

        # 创建发布任务1
        publishTask1 = models.PublishTask()
        publishTask1.user_id = user1.user_id
        publishTask1.task_id = task1.task_id
        publishTask1.save()

        # 创建递送1
        delivery1 = models.Delivery()
        delivery1.task_id = task1.task_id
        delivery1.delivery_detail = "菜鸟驿站5号柜包裹码xxxx-xxxx"
        delivery1.save()

        self.client.delete('/task/delivery/' + str(task1.task_id))

        filter_delivery = models.Delivery.objects.filter(task_id = task1.task_id)

        self.assertEqual(filter_delivery.__len__(), 0)

        # 删除数据项 
        user1.delete()
        task1.delete()
        publishTask1.delete()
        delivery1.delete()

    
    # 测试新建一个跑腿任务
    def test_task_delivery(self):
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        post_data = {
            "task": {
                "task_type":                0,
                "task_sketch":              "帮忙拿快递",
                "task_bonus":               1
            },
            "delivery": {
                "delivery_detail":          "菜鸟驿站5号柜包裹码xxxx-xxxx"
            }
        }

        response = self.client.post('/task/delivery', data=post_data, content_type='application/json')

        task1 = models.Task.objects.get(task_id = response.json()['data']['task_id'])
        delivery1 = models.Delivery.objects.get(task_id = response.json()['data']['task_id'])
        publishTask1 = models.PublishTask.objects.get(task_id = response.json()['data']['task_id'])

        self.assertEqual(task1.task_sketch, "帮忙拿快递")
        self.assertEqual(delivery1.delivery_detail, "菜鸟驿站5号柜包裹码xxxx-xxxx")
        self.assertEqual(publishTask1.task_id, task1.task_id)

        # 删除数据项 
        user1.delete()
        task1.delete()
        delivery1.delete()
        publishTask1.delete()



    # 测试新建一个问卷任务
    def test_task_questionnaire(self):    
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        post_data = {
            "task": {
                "task_type":                1,
                "task_sketch":              "大学生运动爱好调查",
                "task_bonus":               1 
            },
            "questionnaire": {
                "questionnaire_number":			   2,	 
                "questions": [
                    {
                        "question_description":    "你的姓名",
                        "question_type":           2,
                        "question_a":              "",
                        "question_b":              "",
                        "question_c":              "",
                        "question_d":              ""
                    },
                    {
                        "question_description":    "你喜欢什么运动?",
                        "question_type":           1,
                        "question_a":              "篮球",     
                        "question_b":              "羽毛球",    
                        "question_c":              "乒乓球",    
                        "question_d":              "排球"     
                    }
                ]
            }
        }

        response = self.client.post('/task/questionnaire', data=post_data, content_type='application/json')

        task1 = models.Task.objects.get(task_id = response.json()['data']['task_id'])
        publishTask1 = models.PublishTask.objects.get(task_id = response.json()['data']['task_id'])
        questionnaire1 = models.Questionnaire.objects.get(task_id = response.json()['data']['task_id'])
        questions = models.Question.objects.filter(questionnaire_id = questionnaire1.questionnaire_id)
        
        self.assertEqual(task1.task_sketch, "大学生运动爱好调查")
        self.assertEqual(questionnaire1.questionnaire_number, 2)
        self.assertEqual(publishTask1.task_id, task1.task_id)
        self.assertEqual(questions[0].question_description, "你的姓名")
        self.assertEqual(questions[1].question_description, "你喜欢什么运动?")

        # 删除数据项 
        questionnaire1.delete()
        task1.delete()
        publishTask1.delete()
        question1 = models.Question.objects.get(question_id = questions[0].question_id)
        question2 = models.Question.objects.get(question_id = questions[1].question_id)
        question1.delete()
        question2.delete()
        user1.delete()



    # 测试提交问卷
    def test_task_questionnaire_answer(self):       
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建任务1
        task1 = models.Task()
        task1.user_id = user1.user_id
        task1.task_type = 1
        task1.task_sketch = "大学生运动爱好调查"
        task1.task_bonus = 1
        task1.save()

        # 创建问卷1
        questionnaire1 = models.Questionnaire()
        questionnaire1.task_id = task1.task_id
        questionnaire1.questionnaire_number = 2
        questionnaire1.save()

        # 创建题目1
        question1 = models.Question()
        question1.questionnaire_id = questionnaire1.questionnaire_id 
        question1.question_description = "你的姓名"
        question1.question_type = 2
        question1.question_a = ""
        question1.question_b = ""
        question1.question_c = ""
        question1.question_d = ""
        question1.save()

        # 创建题目2
        question2 = models.Question()
        question2.questionnaire_id = questionnaire1.questionnaire_id 
        question2.question_description = "你喜欢什么运动?"
        question2.question_type = 1
        question2.question_a = "篮球"
        question2.question_b = "羽毛球"
        question2.question_c = "乒乓球"
        question2.question_d = "排球" 
        question2.save()


        post_data = {
            "questionnaire_id":    questionnaire1.questionnaire_id,
            "answers": [
                {
                    "question_id":    question1.question_id,
                    "answer_content": "CoderUtil"
                },
                {
                    "question_id":    question2.question_id,
                    "answer_content": "AB"
                }
            ]
        }

        response = self.client.post('/task/questionnaire/answer', data=post_data, content_type='application/json')

        pickTask1 = models.PickTask.objects.get(user_id = user1.user_id)
        answerSheet1 = models.AnswerSheet.objects.get(user_id = user1.user_id)
        answers = models.Answer.objects.filter(answerSheet_id = answerSheet1.answerSheet_id)
        self.assertEqual(answers[0].answer_content, "CoderUtil")
        self.assertEqual(answers[1].answer_content, "AB")


        # 删除数据项 
        answer1 = models.Answer.objects.get(answer_id = answers[0].answer_id)
        answer2 = models.Answer.objects.get(answer_id = answers[1].answer_id)
        answer1.delete()
        answer2.delete()
        answerSheet1.delete()
        pickTask1.delete()
        questionnaire1.delete()
        task1.delete()
        question1.delete()
        question2.delete()
        user1.delete()


    
    # 测试获取自己填写过的答卷
    def test_task_questionnaire_answer(self): 
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建任务1
        task1 = models.Task()
        task1.user_id = user1.user_id
        task1.task_type = 1
        task1.task_sketch = "大学生运动爱好调查"
        task1.task_bonus = 1
        task1.save()

        # 创建问卷1
        questionnaire1 = models.Questionnaire()
        questionnaire1.task_id = task1.task_id
        questionnaire1.questionnaire_number = 2
        questionnaire1.save()

        # 创建题目1
        question1 = models.Question()
        question1.questionnaire_id = questionnaire1.questionnaire_id 
        question1.question_description = "你的姓名"
        question1.question_type = 2
        question1.question_a = ""
        question1.question_b = ""
        question1.question_c = ""
        question1.question_d = ""
        question1.save()

        # 创建题目2
        question2 = models.Question()
        question2.questionnaire_id = questionnaire1.questionnaire_id 
        question2.question_description = "你喜欢什么运动?"
        question2.question_type = 1
        question2.question_a = "篮球"
        question2.question_b = "羽毛球"
        question2.question_c = "乒乓球"
        question2.question_d = "排球" 
        question2.save()

        # 创建答卷1
        answerSheet1 = models.AnswerSheet()
        answerSheet1.questionnaire_id = questionnaire1.questionnaire_id
        answerSheet1.user_id = user1.user_id
        answerSheet1.save()

        # 创建答案1
        answer1 = models.Answer()
        answer1.answerSheet_id = answerSheet1.answerSheet_id
        answer1.question_id = question1.question_id
        answer1.answer_content = "CoderUtil"
        answer1.save()

        # 创建答案2
        answer2 = models.Answer()
        answer2.answerSheet_id = answerSheet1.answerSheet_id
        answer2.question_id = question2.question_id
        answer2.answer_content = "AB"
        answer2.save()

        response = self.client.get('/task/questionnaire/answerSheet/' + str(questionnaire1.questionnaire_id))
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'answerSheet': [
                    {
                        'question': {
                            'question_id': question1.question_id, 
                            'questionnaire_id': questionnaire1.questionnaire_id, 
                            'question_description': '你的姓名', 
                            'question_type': 2, 
                            'question_a': '', 
                            'question_b': '', 
                            'question_c': '', 
                            'question_d': ''
                        }, 
                        'answer': {
                            'answer_id': answer1.answer_id, 
                            'answerSheet_id': answerSheet1.answerSheet_id, 
                            'question_id': question1.question_id, 
                            'answer_content': 'CoderUtil'
                        }
                    }, 
                    {
                        'question': {
                            'question_id': question2.question_id, 
                            'questionnaire_id': questionnaire1.questionnaire_id, 
                            'question_description': '你喜欢什么运动?',
                            'question_type': 1, 
                            'question_a': '篮球', 
                            'question_b': '羽毛球', 
                            'question_c': '乒乓球', 
                            'question_d': '排球'
                        }, 
                        'answer': {
                            'answer_id': answer2.answer_id, 
                            'answerSheet_id': answerSheet1.answerSheet_id, 
                            'question_id': question2.question_id, 
                            'answer_content': 'AB'
                        }
                    }
                ]
            }
        }

        self.assertEqual(response.json(), get_data)

        # 删除数据项 
        user1.delete()
        task1.delete()
        questionnaire1.delete()
        question1.delete()
        question2.delete()
        answerSheet1.delete()
        answer1.delete()
        answer2.delete()



    # 测试查看问卷的统计信息
    def test_task_questionnaire_Statistics(self): 
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建任务1
        task1 = models.Task()
        task1.user_id = user1.user_id
        task1.task_type = 1
        task1.task_sketch = "大学生运动爱好调查"
        task1.task_bonus = 1
        task1.save()

        # 创建问卷1
        questionnaire1 = models.Questionnaire()
        questionnaire1.task_id = task1.task_id
        questionnaire1.questionnaire_number = 2
        questionnaire1.save()

        # 创建题目1
        question1 = models.Question()
        question1.questionnaire_id = questionnaire1.questionnaire_id 
        question1.question_description = "你的姓名"
        question1.question_type = 2
        question1.question_a = ""
        question1.question_b = ""
        question1.question_c = ""
        question1.question_d = ""
        question1.save()

        # 创建题目2
        question2 = models.Question()
        question2.questionnaire_id = questionnaire1.questionnaire_id 
        question2.question_description = "你喜欢什么运动?"
        question2.question_type = 1
        question2.question_a = "篮球"
        question2.question_b = "羽毛球"
        question2.question_c = "乒乓球"
        question2.question_d = "排球" 
        question2.save()

        # 创建答卷1
        answerSheet1 = models.AnswerSheet()
        answerSheet1.questionnaire_id = questionnaire1.questionnaire_id
        answerSheet1.user_id = user1.user_id
        answerSheet1.save()

        # 创建答案1
        answer1 = models.Answer()
        answer1.answerSheet_id = answerSheet1.answerSheet_id
        answer1.question_id = question1.question_id
        answer1.answer_content = "CoderUtil"
        answer1.save()

        # 创建答案2
        answer2 = models.Answer()
        answer2.answerSheet_id = answerSheet1.answerSheet_id
        answer2.question_id = question2.question_id
        answer2.answer_content = "AB"
        answer2.save()

        response = self.client.get('/task/questionnaire/Statistics/' + str(questionnaire1.questionnaire_id))
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'statistics': [
                    {
                        'question': {
                            'question_id': question1.question_id, 
                            'questionnaire_id': questionnaire1.questionnaire_id, 
                            'question_description': '你的姓名', 
                            'question_type': 2, 
                            'question_a': '', 
                            'question_b': '', 
                            'question_c': '', 
                            'question_d': ''
                        }, 
                        'answer': {
                            'answer_a_count': 0, 
                            'answer_b_count': 0, 
                            'answer_c_count': 0, 
                            'answer_d_count': 0, 
                            'answer_gap_filling': [
                                {
                                    'gap_filling_content': 'CoderUtil'
                                }
                            ]
                        }
                    }, 
                    {
                        'question': {
                            'question_id': question2.question_id, 
                            'questionnaire_id': questionnaire1.questionnaire_id, 
                            'question_description': '你喜欢什么运动?', 
                            'question_type': 1, 
                            'question_a': '篮球', 
                            'question_b': '羽毛球', 
                            'question_c': '乒乓球', 
                            'question_d': '排球'
                        }, 
                        'answer': {
                            'answer_a_count': 1, 
                            'answer_b_count': 1, 
                            'answer_c_count': 0, 
                            'answer_d_count': 0, 
                            'answer_gap_filling': []
                        }
                    }
                ]
            }
        }

        self.assertEqual(response.json(), get_data)

        # 删除数据项 
        user1.delete()
        task1.delete()
        questionnaire1.delete()
        question1.delete()
        question2.delete()
        answerSheet1.delete()
        answer1.delete()
        answer2.delete()

    
    # 测试发布者截止问卷
    def test_task_questionnaire_closure(self): 
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建任务1
        task1 = models.Task()
        task1.user_id = user1.user_id
        task1.task_type = 1
        task1.task_sketch = "大学生运动爱好调查"
        task1.task_bonus = 1
        task1.save()

        # 创建问卷1
        questionnaire1 = models.Questionnaire()
        questionnaire1.task_id = task1.task_id
        questionnaire1.questionnaire_number = 2
        questionnaire1.save()

        # 创建题目1
        question1 = models.Question()
        question1.questionnaire_id = questionnaire1.questionnaire_id 
        question1.question_description = "你的姓名"
        question1.question_type = 2
        question1.question_a = ""
        question1.question_b = ""
        question1.question_c = ""
        question1.question_d = ""
        question1.save()

        # 创建题目2
        question2 = models.Question()
        question2.questionnaire_id = questionnaire1.questionnaire_id 
        question2.question_description = "你喜欢什么运动?"
        question2.question_type = 1
        question2.question_a = "篮球"
        question2.question_b = "羽毛球"
        question2.question_c = "乒乓球"
        question2.question_d = "排球" 
        question2.save()

        put_data = {
            "questionnaire_id": questionnaire1.questionnaire_id
        }
        self.client.put('/task/questionnaire/closure', data=put_data, content_type='application/json')

        get_questionnaire = models.Questionnaire.objects.get(questionnaire_id = questionnaire1.questionnaire_id)
        self.assertEqual(get_questionnaire.questionnaire_closed, 1)

        # 删除数据项 
        user1.delete()
        task1.delete()
        questionnaire1.delete()
        question1.delete()
        question2.delete()



class BillTest(TestCase):

    # 测试获取当前用户的交易历史
    def test_bill(self): 
        # 创建用户1
        user1 = models.User()
        user1.user_phone = '15626259034'
        user1.user_password = '123456'
        user1.save()

        # 密码登录
        post_data = {
            'user_phone': '15626259034',
            'user_password': '123456'
        }
        self.client.post('/user/password/session', data=post_data, content_type='application/json')

        # 创建账单1
        bill1 = models.Bill()
        bill1.user_id = user1.user_id
        bill1.bill_type = 0
        bill1.bill_number = 1
        bill1.bill_description = ''
        bill1.save()

        response = self.client.get('/bill')
        get_data = {
            'code': 200, 
            'message': 'OK', 
            'data': {
                'bills': [
                    {
                        'bill_id': bill1.bill_id, 
                        'user_id': user1.user_id, 
                        'bill_type': 0, 
                        'bill_number': 1, 
                        'bill_description': '', 
                        'bill_time': bill1.bill_time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
            }
        }
    
        self.assertEqual(response.json(), get_data)

        # 删除数据项 
        user1.delete()
        bill1.delete()



