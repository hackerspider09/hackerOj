from rest_framework import viewsets
from rest_framework.generics import mixins
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from django.views import View
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
import json,io
from django.db.models import Q 

# from rest_framework.authentication import 
# Authentication and Permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer

from datetime import datetime 
# Custom Authentication
from .customAuth import *

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError , InvalidToken

# throttle
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle

import requests

from contest import models as modelsCo

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# class RegisterApi(viewsets.GenericViewSet,mixins.CreateModelMixin):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#     permission_classes=[IsAuthenticated,IsAdminUser]
#     authentication_classes = [SessionAuthentication]


# class TeamRegisterApi(viewsets.GenericViewSet,mixins.CreateModelMixin):
#     queryset = Team.objects.all()
#     serializer_class = TeamRegisterSerializer
#     permission_classes=[IsAuthenticated,IsAdminUser]
#     authentication_classes = [SessionAuthentication]

# class GetTime(viewsets.GenericViewSet,mixins.ListModelMixin):
#     queryset = ContestTime.objects.all()
#     serializer_class = GetTimeSerializer

import socket
import time
def getHost(request):
    # time.sleep(2)
    s= socket.gethostname()
    # ip_address = socket.gethostbyname(hostname)

    return HttpResponse(f"Hello Prash docker address : {s}")





# class RatingViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         serializer = RatingSerializer(data=data)
#         if serializer.is_valid():
#             user = self.request.user
#             serializer.validated_data["user"] = user
#             serializer.save()
#         return Response(serializer.data)
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset
    



#############################
#                           #
#      Leaderboard Api      #
#                           #
#############################
class LeaderBoardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = LeaderBoardSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [LeaderboardJwt]
    
    @method_decorator(cache_page(30)) # 30 sec cache
    def list(self, request, *args, **kwargs):
        contest_id = self.kwargs['contestId']
        if not modelsCo.Contest.objects.filter(contestId = contest_id).exists():
            return Response({'msg':'Contest Does not exists'},status=status.HTTP_404_NOT_FOUND)
        
        user = self.request.user
        junior_query = Team.objects.filter(isJunior=True,contest=contest_id).order_by("-score", "lastUpdate")
        senior_query = Team.objects.filter(isJunior=False,contest=contest_id).order_by("-score", "lastUpdate")

        junior_serializer = LeaderBoardSerializer(junior_query, many=True)
        senior_serializer = LeaderBoardSerializer(senior_query, many=True)

        response_data = {
            'juniorLeaderboard': junior_serializer.data,
            'seniorLeaderboard': senior_serializer.data,
        }
        return Response(response_data,status=status.HTTP_200_OK)        






class ResultAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = LeaderBoardSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        contest_id = self.kwargs['contestId']
        team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contest_id)
        if (team.isJunior):
            top6query = Team.objects.filter(isJunior=True,contest=contest_id).order_by("-score", "lastUpdate")
        else:
            top6query = Team.objects.filter(isJunior=False,contest=contest_id).order_by("-score", "lastUpdate")
        

        top6query_serializer = LeaderBoardSerializer(top6query,context={'contest_id': contest_id}, many=True)

        teamQuery = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contest_id)
        teamRank = IndividualLeaderBoardSerializer(teamQuery)
        totalSubmissions = Submission.objects.filter(team=teamQuery,contest=contest_id)
        rightSubmissions = totalSubmissions.filter(isCorrect  = True)
        response_data = {
            'personalRank':teamRank.data,
            'top6': top6query_serializer.data[:6],
            'totalSub':len(totalSubmissions),
            'rightSub':len(rightSubmissions)
        }
        return Response(response_data,status=status.HTTP_200_OK)