from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'gettime', GetTime,basename='gettime_all')
router.register(r'gettime/(?P<contestId>[-\w]+)', GetTime,basename='gettime')
router.register(r'activated_containers', ActivatedContainers,basename='ActivatedContainers')
router.register(r'list_contest', GetContestsViewSet,basename='list_contest')
router.register(r'list_execution_server', ExecutionServerListViewSet,basename='list_server')


urlpatterns = [
    path('', include(router.urls)),
    path('CreateRCOp/', CreateRCOp.as_view(), name='create_rc_op'),
    path('get_testcase/', GetTestCase.as_view(), name='get_testcase'),
    path('get_testcase_on_execution_server/', FetchTestCaseToExecutionServer.as_view(), name='get_testcase_on_execution_server'),
    
    
]
