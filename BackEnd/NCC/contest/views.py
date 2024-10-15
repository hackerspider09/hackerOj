from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import mixins
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser


from question import models as modelQ
from submission import dockerJudgeUtils,models as modelS
import docker
from submission.tasks import get_Testcase

import redis
from django.core.cache import cache
from django.conf import settings
from rest_framework.renderers import JSONRenderer
import requests


redis_client = redis.StrictRedis(host=settings.REDIS_HOST_IP, port=6379, db=0)

client = docker.from_env()
#############################
#                           #
#   Get Contest Time Api    #
#                           #
#############################

class GetTime(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Contest.objects.all()
    serializer_class = GetTimeSerializer

    def list(self, request, *args, **kwargs):
        # Access the contestId from the URL kwargs
        contest_id = self.kwargs.get('contestId')
        print(contest_id)
        if not contest_id:
            return super().list(request, *args, **kwargs)
        try:
            contestQuery = Contest.objects.get(contestId = contest_id)
            serializer = self.serializer_class(contestQuery)
            return Response(serializer.data,status.HTTP_200_OK)
            # return super().list(request, *args, **kwargs)
        except:
            return Response({"msg":"Contest Does not Exists."},status=status.HTTP_404_NOT_FOUND)


class ActivatedContainers(viewsets.ModelViewSet):
    queryset = ActivatedContainer.objects.filter(disable=False)
    serializer_class=ActivatedContainerSerializer
    lookup_field='containerId'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def destroy(self, request, containerId=None):  # Accept containerId instead of pk
        # Delete a specific Docker container by containerId
        try:
            container = ActivatedContainer.objects.get(containerId=containerId)
        except ActivatedContainer.DoesNotExist:
            return Response({'msg':f"Container with id {containerId} not found"},status=status.HTTP_404_NOT_FOUND)

        try:
            running_container = client.containers.get(container.containerId)
            running_container.remove(force=True)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Mark the container as disabled in the database
        container.disable = True
        container.save()

        return Response({'msg':f"Container with id {containerId} deleted"},status=status.HTTP_200_OK) 
    
    
    def get_queryset(self):
        return super().get_queryset().filter(disable=False)
    

class CreateRCOp(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            contestId = data.get('contestId')
            questionId = data.get('question')
            inputStart = int(data.get('inputStart'))
            inputEnd = int(data.get('inputEnd'))

            try:
                question = modelQ.Question.objects.get(questionId=questionId)
                contest = Contest.objects.get(contestId=contestId)
                correctCode = modelS.CorrectCode.objects.get(question=question)
                rcOp = dockerJudgeUtils.executeRunRc(questionId,correctCode.language,inputStart,inputEnd,correctCode.correct_code)

                if (rcOp):                                
                    return Response({"msg": f"input and output added for question {questionId} from {inputStart} to {inputEnd}"}, status=status.HTTP_200_OK)
                return Response({"msg": f"input and output may not added for question {questionId} from {inputStart} to {inputEnd}"}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"msg": f"Contest/Question/CorrectCode is not found =>{e}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"msg": f"Error =>{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def patch(self, request, *args, **kwargs):
        data = request.data
        try:
            questionId = data.get('question')
            inputVal = data.get('input')
            outputVal = data.get('output')
            if (inputVal  and outputVal and questionId ):
                redis_client.hset(questionId, inputVal, outputVal)
                return Response({"msg": f"Input added for {questionId} for {inputVal}"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": f"Check body data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"msg": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            data = request.data
            questionId = data.get('question')

            if questionId:
                # Assuming you have a Redis client named redis_client
                redis_client.delete(questionId)
                
                return Response({"msg": f"Data related to question {questionId} deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "Question ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"msg": f"Error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
class GetTestCase(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            questionId = data.get('question')

            get_Testcase.delay(questionId)
            return Response({"msg": f"Testcase fetching started for {questionId}"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"msg": f"Testcase fetching failed"}, status=status.HTTP_200_OK)
        
    def delete(self, request, *args, **kwargs):
        try:
            data = request.data
            questionId = data.get('question')
            cache_key = f"testcases_{questionId}"  

            cache.delete(cache_key)
            return Response({"msg": f"Testcases deleted for {questionId}"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"msg": f"Testcases delete failed"}, status=status.HTTP_200_OK)
        

class GetContestsViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    
    '''
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    lookup_field="contestId"
    renderer_classes = [JSONRenderer]

class ExecutionServerListViewSet(viewsets.ModelViewSet):
    '''
    
    '''
    queryset = ExecutionServers.objects.all()
    serializer_class = ExecutionServerSerializer
    lookup_field="id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]    
    renderer_classes = [JSONRenderer]


class FetchTestCaseToExecutionServer(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            questionId = data.get('question')
            contestId = data.get('contest')
            server_ip = data.get('address')
            server_port = data.get('port')

            payload ={
                "question":questionId,
                "contest":contestId,
            }

            server_url = f"http://{server_ip}:{server_port}/core/getTestcase/"  
            print("api rquest started",server_url)

            response = requests.post(server_url, data=payload)
            json_response = response.json() 
            return Response({'msg': json_response.get('msg')},status=response.status_code)


        except Exception as e:
            print(e)
            return Response({"msg": f"Testcase fetching failed"}, status=status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
        try:
            data = request.data
            print("res ",data)
            questionId = data.get('question')
            contestId = data.get('contest')
            server_ip = data.get('address')
            server_port = data.get('port')

            payload ={
                "question":questionId,
                "contest":contestId,
            }

            server_url = f"http://{server_ip}:{server_port}/core/getTestcase/"  
            print("api rquest started",server_url)
            try:
                    
                response = requests.delete(server_url, json=payload)
                json_response = response.json() 
                return Response({'msg': json_response.get('msg')},status=response.status_code)

            except Exception as e:
                print(e)
                return Response({"msg": f"Testcase fetching failed from api call to server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            print(e)
            return Response({"msg": f"Testcase fetching failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)