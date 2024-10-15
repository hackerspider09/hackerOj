from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'submit', SubmitQuestion,basename='submit')
router.register(r'runsubmission', RunQuestion,basename='run')
router.register(r'getsubmission', GetSubmissions,basename='get_submission')
router.register(r'getactivatedcontainer', GetActivatedContainer,basename='get_activated_container')


urlpatterns = [
    path('', include(router.urls)),
    path('getTestcase/', GetTestCase.as_view(), name='get_testcase'),
    path('get_testcase_detail/', CheckFetchedTestCase.as_view(), name='get_testcase_detail'),
]
