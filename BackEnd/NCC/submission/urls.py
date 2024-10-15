from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'(?P<contestId>[-\w]+)/submissions', GetSubmissions,basename='submissions')
router.register(r'(?P<contestId>[-\w]+)/submit', Submit,basename='submit')
router.register(r'(?P<contestId>[-\w]+)/submit2', Submit2,basename='submit2')



urlpatterns = [
    path('', include(router.urls)),
    path('<str:contestId>/runcode/',RunCode.as_view(),name="Run code"),
    path('<str:contestId>/runcode2/',RunCode2.as_view(),name="Run code"),
    path('<str:contestId>/runrccode/',RunRc.as_view(),name="Run rc code"),
    path('<str:contestId>/runrccode2/',RunRc2.as_view(),name="Run rc code2"),

    path('updatesubmission/', CallbackApiForExecutionServer.as_view(),name="callback_url_for_execution_server"),
    path('startsubmission/', StartSubmissionExecution.as_view(),name="callback_url_for_start_server"),
]
