from .models import *
from .serializers import *
from django.views import View
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.db.models import Q 
from rest_framework import viewsets
from rest_framework.generics import mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.contrib.auth import authenticate
from datetime import datetime 

# JWT
from rest_framework_simplejwt.tokens import RefreshToken


import requests

from contest.models import Contest


from core.permissions import TimecheckLogin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import RegistrationOpenPermission

from .utils import *

#############################
#                           #
#        Login Api          #
#                           #
#############################

class LoginApi(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes=[TimecheckLogin]
    authentication_classes=[]
    
    
    def post(self, request, format=None):
        print("INside login...")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        contestId = serializer.validated_data.get('contestId')
        isTeam = serializer.validated_data.get('isTeam')

        user = authenticate(username=username, password=password)
        print("user ...",user)
        if user is not None:
        
            contest = Contest.objects.get(contestId=contestId)
            print("Authenticated but not in team")
            if isTeam:
                team = Team.objects.filter(Q(user1 = user) | Q(user2 = user),contest=contest)
                if ( not team.exists()):
                    return Response({'msg':'Team not found'}, status=status.HTTP_404_NOT_FOUND)
                team = team.first()
            else:
                # if single user
                team = Team.objects.filter(Q(user1 = user) | Q(user2 = user),contest=contest)
                if ( not team.exists()):
                    team,created = Team.objects.get_or_create(user1 = user ,contest=contest)
                else:
                    team = team.first()
                # check if user is in team but if he click isteam to false then check if it is actualy individul or in team and then return his object

                 
            try:
                print(team)
                if (team.isLogin):
                    return Response({'msg':'You are Already Logged in'}, status=status.HTTP_400_BAD_REQUEST)
                
                # if user is not None:
                token = RefreshToken.for_user(user=user)
                
                # team.isLogin = True
                team.save()
                data = {
                    'token': str(token.access_token),
                    'isJunior' : team.isJunior,
                    'contestId' : contestId
                }
                return Response(data, status=status.HTTP_200_OK)
            except:
                return Response({'msg':'Try to contact organiser'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If user not present in local db
            # Try on main website API
            # request 
            pass
                        
        return Response({'msg':'User not Found'},status=status.HTTP_404_NOT_FOUND)
    



# Write api to avoid mail service fail
'''
User will give its credential of main web not contest cred 
on main web just check is this user registered to event if yes give data

*Note - Make only if problem like CTD23 occures 
'''
        
class RegisterApiView(viewsets.GenericViewSet,mixins.CreateModelMixin):
    '''
    This register api will directly create user in db and its team of one user only
    
    '''
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [RegistrationOpenPermission] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
    
            return Response({'msg':'user created'},status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class RegisterSingleUserApiView(viewsets.GenericViewSet,mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSingleUserSerializer
    authentication_classes = []
    permission_classes = [RegistrationOpenPermission]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
    
            return Response({'msg':'user created'},status=status.HTTP_201_CREATED)
        except:
            return Response({'msg':'check username may be exists /contest ID '},status=status.HTTP_400_BAD_REQUEST)
            # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class CreateTeamApiView(viewsets.GenericViewSet,mixins.CreateModelMixin):
    queryset = Team.objects.all()
    serializer_class = CreateTeamSerializer
    authentication_classes = []
    permission_classes = [RegistrationOpenPermission]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
    
            return Response({'msg':'Team created'},status=status.HTTP_201_CREATED)
        except:
            return Response({'msg':'check username may not be exists /contest ID '},status=status.HTTP_400_BAD_REQUEST)
            # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    