'''
以下是各个API的单元测试
'''


from django.test import TestCase
from xianyu import models
from time import strftime, localtime


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

        response = self.client.get('/user/profile', content_type='application/json')

        # 利用获取用户信息，验证此时确实是已登录状态
        self.assertNotEqual(response.json(), __notLogin__)


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

        response = self.client.get('/user/profile', content_type='application/json')

        # 退出登录后，利用获取用户信息再验证此时是否确实是未登录状态
        self.assertEqual(response.json(), __notLogin__)


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
