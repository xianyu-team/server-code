from django.urls import path

from .views import sms
from .views import user
from .views import task
from .views import bill

urlpatterns = [
    path('sms/verification_code', sms.sms_verification_code),
    path('sms/verification', sms.sms_verification),

    path('user', user.user),
    path('user/profile', user.user_profile),
    path('user/password/session', user.user_password_session),
    path('user/password', user.user_password),
    path('user/sms/session', user.user_sms_session),
    path('user/session', user.user_session),
    path('user/balance', user.user_balance),
    path('user/tasks', user.user_tasks),
    path('user/information', user.user_information),
    path('user/following', user.user_following),
    path('user/followings', user.user_followings),
    path('user/fans', user.user_fans),

    path('task', task.task),
    path('task/delivery/detail', task.task_delivery_detail),
    path('task/questionnaire/detail', task.task_questionnaire_detail),
    path('task/acceptance', task.task_acceptance),
    path('task/delivery/complishment', task.task_delivery_complishment),
    path('task/questionnaire', task.task_questionnaire),
    path('task/questionnaire/answer', task.task_questionnaire_answer),
    path('task/questionnaire/answerSheet', task.task_questionnaire_answerSheet),
    path('task/questionnaire/Statistics', task.task_questionnaire_Statistics),
    path('task/questionnaire/closure', task.task_questionnaire_closure),

    path('bill', bill.bill),
]
