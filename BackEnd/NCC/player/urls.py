from django.contrib import admin
from django.urls import path,include
from .views import LoginApi,RegisterApiView,RegisterSingleUserApiView,CreateTeamApiView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'direct_register/(?P<contestId>[-\w]+)', RegisterApiView,basename='direct-register-user')
router.register(r'register/(?P<contestId>[-\w]+)', RegisterSingleUserApiView,basename='register-user')
router.register(r'createteam/(?P<contestId>[-\w]+)', CreateTeamApiView,basename='create-user')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginApi.as_view(),name="login"),

]



