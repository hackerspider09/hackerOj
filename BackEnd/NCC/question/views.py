from .models import *
from .serializers import *
from django.views import View
from rest_framework import viewsets
from rest_framework.generics import mixins
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.db.models import Q 

from django.contrib.auth import authenticate
from datetime import datetime 

# JWT
from rest_framework_simplejwt.tokens import RefreshToken


import requests
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from player.models import Team
from rest_framework_simplejwt.authentication import JWTAuthentication


from core.permissions import TimecheckGlobal

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

#############################
#                           #
#     Question API          #
#                           #
#############################


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    To get question list respective to category (Junior,Senior,Both)
    To get specific question by question ID from URL
    '''
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field="questionId"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]    
    renderer_classes = [JSONRenderer]

    # @method_decorator(cache_page(30))  # Cache for 30 sec
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # @method_decorator(cache_page(60*5))  # Cache for 5 min
    def  retrieve(self, request, *args, **kwargs):
        return  super().retrieve(request, *args,**kwargs)
    

    def get_queryset(self):
        print(self.kwargs['contestId'])
        contestId = self.kwargs['contestId']
        user = self.request.user
        queryset = super().get_queryset()
        print("user ",user)
        team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contestId)
        return queryset.filter(Q(category= "junior" if team.isJunior else "senior" ) | Q(category="both"),contest = contestId).order_by("questionNumber")  #return  questions filtered with two  conditions







class GetTestcaseView(viewsets.ReadOnlyModelViewSet):
    queryset = Testcase.objects.all()
    serializer_class = TestcaseSerializer
    def get_queryset(self):
        print("get testcase for question")
        question_id = self.request.query_params.get('question_id')


        return Testcase.objects.filter(question=question_id).order_by('testcaseNumber')

    def list(self, request, *args, **kwargs):
        print("hello list")
        queryset = self.get_queryset()
        serializer = TestcaseSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetQuestionIdOnly(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionIdOnlySerializer

    def get_queryset(self):
        print("get quesiton id only")
        print(self.kwargs['contestId'])
        contestId = self.kwargs['contestId']
        queryset = super().get_queryset()
        return queryset.filter(contest = contestId).order_by("questionNumber")
