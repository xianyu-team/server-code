from django.urls import path, re_path

from .views import sms
from .views import user
from .views import task
from .views import bill

urlpatterns = [
    re_path(r'^sms/verification_code/(?P<user_phone>\d{11})$', sms.sms_verification_code),
    path('sms/verification', sms.sms_verification),

    path('user', user.user),
    path('user/profile', user.user_profile),
    path('user/password/session', user.user_password_session),
    path('user/password', user.user_password),
    path('user/sms/session', user.user_sms_session),
    path('user/session', user.user_session),
    path('user/balance', user.user_balance),
    re_path(r'^user/tasks/(?P<t_type>\d)$', user.user_tasks),
    path('user/batch/information', user.user_batch_information),
    path('user/following', user.user_following_post),
    re_path(r'^user/following/(?P<user_id>\d+)$', user.user_following_delete),
    path('user/followings', user.user_followings),
    path('user/fans', user.user_fans),

    re_path(r'^task/(?P<t_type>\d)$', task.task),
    re_path(r'^task/delivery/detail/(?P<task_id>\d)$', task.task_delivery_detail),
    re_path(r'^task/questionnaire/detail/(?P<task_id>\d)$', task.task_questionnaire_detail),
    path('task/acceptance', task.task_acceptance),
    path('task/delivery/complishment', task.task_delivery_complishment),
    re_path(r'^task/delivery/(?P<task_id>\d)$', task.task_delivery_delete),
    path('task/delivery', task.task_delivery),
    path('task/questionnaire', task.task_questionnaire),
    path('task/questionnaire/answer', task.task_questionnaire_answer),
    re_path(r'^task/questionnaire/answerSheet/(?P<questionnaire_id>\d)$', task.task_questionnaire_answerSheet),
    re_path(r'^task/questionnaire/Statistics/(?P<questionnaire_id>\d)$', task.task_questionnaire_Statistics),
    path('task/questionnaire/closure', task.task_questionnaire_closure),

    path('bill', bill.bill),
]
