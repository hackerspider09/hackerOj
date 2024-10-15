from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'(?P<contestId>[-\w]+)/questions', QuestionViewSet)
router.register(r'(?P<contestId>[-\w]+)/get_questions_id', GetQuestionIdOnly)
router.register(r'gettestcases', GetTestcaseView, basename='get-testcases')

urlpatterns = [
    path('', include(router.urls)),

]




