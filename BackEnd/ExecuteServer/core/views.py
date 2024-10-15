from .models import *
from .serializers import *
from django.views import View
from django.shortcuts import redirect,HttpResponse,get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.db.models import Q 
from rest_framework.generics import mixins
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from datetime import datetime 

from rest_framework import viewsets

import requests

from .utils import *
from .judgeUtils import *
from django.utils import timezone

from .tasks import *

import redis
from datetime import timedelta

class GetSubmissions(viewsets.ReadOnlyModelViewSet):
    '''This view get parameters from url'''
    
    queryset = Submission.objects.all()
    serializer_class = GetSubmissionSerializer
    lookup_field="id"

class GetActivatedContainer(viewsets.ReadOnlyModelViewSet):
    
    queryset = ActivatedContainer.objects.all()
    serializer_class = ActivatedContainerSerializer
    lookup_field="id"

class GetFetchedTestCaseDetail(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class SubmitQuestion(viewsets.GenericViewSet,mixins.CreateModelMixin):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        
        data = request.data

        # print("=> Requested Data ",data)
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():            
            try:
                    
                serializer.validated_data['mode'] = "SUB"
                serializer.validated_data['status'] = "PEN"
                serializer.validated_data['isCorrect'] = False
                submission = serializer.save()

                process_submission.delay(submission.id)


                # print(question.questionId)    #to get question id from question 
                # delete_container.delay(obj_id)
                return Response({'msg': "Submission queued", 'submission_id': submission.id},status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                print(e)
                # deallocate(container)
                print("some wong")
                return Response({'msg':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("*******Invalid*******")
            # print(request.data)
            return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
class RunQuestion(viewsets.GenericViewSet,mixins.CreateModelMixin):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        
        data = request.data

        # print("=> Requested Data ",data)
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():            
            try:
                    
                serializer.validated_data['mode'] = "RUN"
                serializer.validated_data['status'] = "PEN"
                serializer.validated_data['isCorrect'] = False
                submission = serializer.save()

                process_run_submission.delay(submission.id)


                # print(question.questionId)    #to get question id from question 
                # delete_container.delay(obj_id)
                return Response({'msg': "Submission queued", 'submission_id': submission.id},status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                print(e)
                # deallocate(container)
                print("some wong")
                return Response({'msg':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("*******Invalid*******")
            # print(request.data)
            return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

class GetTestCase(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            questionId = data.get('question')
            contestId = data.get('contest')

            if (questionId is not None or contestId is not None):

                print('question id ',questionId,"connest id",contestId)
                get_Testcase.delay(questionId,contestId)
                return Response({"msg": f"Testcase fetching queued for {questionId}"}, status=status.HTTP_200_OK)
            
            # is there is no quesiton id start to fectch testcase for all quesitons 
            return Response({"msg": f"ContestId/questionId Not mentioned"}, status=status.HTTP_400_BAD_REQUEST)

                    

        except Exception as e:
            print(e)
            return Response({"msg": f"Testcase fetching failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, *args, **kwargs):
        try:
            data = request.data
            questionId = data.get('question')
            contestId = data.get('contest') 

            print("question id ",questionId,"contestid ",contestId)

            if questionId is not None:
                cache_key = f"testcases_{questionId}"  
                questionQuery = TestcaseForQuestion.objects.get(question=questionId)
                questionQuery.isFetched = False
                questionQuery.save()

                cache.delete(cache_key)
                return Response({"msg": f"Testcases deleted for {questionId}"}, status=status.HTTP_200_OK)
            
            # is there is no quesiton id start to fectch testcase for all quesitons 
            if contestId is None:
                return Response({"msg": f"Contest id Not mentioned"}, status=status.HTTP_400_BAD_REQUEST)

            testCaseQuery = TestcaseForQuestion.objects.filter(contest=contestId)
            
            for quesData in testCaseQuery:

                quesData.isFetched = False
                quesData.save()

                cache_key = f"testcases_{quesData.question}"  
                cache.delete(cache_key)

            return Response({"msg": f"Testcase deleted for contest {contestId}"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"msg": f"Testcases delete failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CheckFetchedTestCase(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = request.data
            # questionId = data.get('question')
            questionquery = TestcaseForQuestion.objects.all()
            serializer = CheckTestcaseSerializer(questionquery,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"msg": f"something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)