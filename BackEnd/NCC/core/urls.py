from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
# router.register(r'questions', QuestionViewSet)
# router.register(r'rating', RatingViewSet)
router.register(r'(?P<contestId>[-\w]+)/leaderboard', LeaderBoardViewSet,basename='leaderboard')
router.register(r'(?P<contestId>[-\w]+)/result', ResultAPIView,basename='result')
# router.register(r'submit', Submit,basename='submit')
# router.register(r'submit1', Submit1,basename='submit1')
# router.register(r'submissions', GetSubmissions,basename='submissions')
# router.register(r'gettime', GetTime,basename='gettime')
# router.register(r'register',RegisterApi)


# Only for Admin and Superuser (Emergency)
# secretRouter = routers.DefaultRouter()
# secretRouter.register(r'teamregister',TeamRegisterApi)

urlpatterns = [
    path('', include(router.urls)),
    path('gethost/', getHost, name='host'),
    # path('secret/api/', include(secretRouter.urls)),
    # path('api/login/', LoginApi.as_view(),name="login"),
    # path('tinymce/',include('tinymce.urls')),
    
]
