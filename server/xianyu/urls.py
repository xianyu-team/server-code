from django.urls import path, include

from .views import task

urlpatterns = [
    path('/task', task.task),
    path('/task/delivery/detail', task.task_delivery_detail),
    path('/task/questionnaire/detail', task.task_questionnaire_detail),
    path('/task/acceptance', task.task_acceptance),
    path('/task/delivery/complishment', task.task_delivery_complishment),
    path('/task/questionnaire', task.task_questionnaire),
    path('/task/questionnaire/answer', task.task_questionnaire_answer),
    path('/task/questionnaire/answerSheet', task.task_questionnaire_answerSheet),
    path('/task/questionnaire/Statistics', task.task_questionnaire_Statistics),
]