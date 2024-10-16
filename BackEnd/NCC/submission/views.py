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

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from rest_framework.renderers import JSONRenderer

import requests

from contest.models import Contest
from .utils import *
from .judgeUtils import *
from django.utils import timezone

from core.permissions import TimecheckGlobal
from question import models as modelsQu
from .tasks import *

import redis
from datetime import timedelta

from django.conf import settings

# websocket
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
'''
channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'submission_{submission_id}',
        {
            'type': 'submission_status',
            'status': 'In Progress'
        }
    )
    # Run submission logic...
    # After submission:
    async_to_sync(channel_layer.group_send)(
        f'submission_{submission_id}',
        {
            'type': 'submission_status',
            'status': 'Completed'
        }
    )
'''

redis_client = redis.StrictRedis(host=settings.REDIS_HOST_IP, port=6379, db=0)
DispatcherURL="http://192.168.52.139"


#############################
#                           #
#    Submissions API        #
#                           #
#############################

class GetSubmissions(viewsets.GenericViewSet,mixins.ListModelMixin):
    '''This view get parameters from url'''
    
    queryset = Submission.objects.all()
    serializer_class = GetSubmissionSerializer
    lookup_field="question"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal] 

    def get_queryset(self):
        user = self.request.user
        contest_id = self.kwargs['contestId']
        print(contest_id)

        team = Team.objects.get(Q(user1 = user)| Q(user2 = user),contest=contest_id)
        queryset = super().get_queryset()
        queryset = queryset.filter(team = team).order_by("-id")
        

        question = self.request.query_params.get("question")
        print("question in submission ",question)
        if question:    
            # print("Users Question => ",question)
            queryset = queryset.filter(question=question,mode='SUB')
        
            
        return queryset
    
    # http://127.0.0.1:8000/api/submissions/?question=fa152
        

# callback api to get status form execution server
class CallbackApiForExecutionServer(APIView):
    def post(self, request, *args, **kwargs):
        print("submission executed update its status on main server")
        serializer = CallBackApiSerializer(data=request.data)
        if serializer.is_valid():
            submissionId = serializer.validated_data.get('submissionId')
            input_data = serializer.validated_data.get('input')
            output = serializer.validated_data.get('output')
            error = serializer.validated_data.get('error')
            mode = serializer.validated_data.get('mode')
            totalSubmissions = serializer.validated_data.get('totalSubmissions')
            correctSubmissions = serializer.validated_data.get('correctSubmissions')
            isCorrect = serializer.validated_data.get('isCorrect')
            statusOfSubmission = serializer.validated_data.get('status')
            
            try:
                submission = Submission.objects.get(id=submissionId)

                # Update fields if they are not None
                if mode is not None:
                    submission.mode = mode
                if input_data is not None:
                    submission.input = input_data
                if output is not None:
                    submission.output = output
                if error is not None:
                    submission.error = error
                if totalSubmissions is not None:
                    submission.totalSubmissions = totalSubmissions
                if correctSubmissions is not None:
                    submission.correctSubmissions = correctSubmissions
                if isCorrect is not None:
                    submission.isCorrect = isCorrect
                if statusOfSubmission is not None:
                    submission.status = statusOfSubmission



                if(mode=='SUB'):
                    questionQuery = modelsQu.Question.objects.get(questionId=submission.question)
                    teamQuery = modelP.Team.objects.get(teamId=submission.team)
                    
                    points = questionQuery.points
                    
                    try:
                        submissionQuery = Submission.objects.filter(team = teamQuery ,question = questionQuery,isCorrect=True,mode='SUB').exists()
                        if submissionQuery == False and isCorrect:
                            teamQuery.score += points
                            teamQuery.lastUpdate = timezone.now()
                            submission.points = points
                            teamQuery.save()
                    except Exception as e:
                        print("None value is returing ",e)
                        pass
                submission.save()

                if(mode=='RC'):
                    try:
                        questionQuery = modelsQu.Question.objects.get(questionId=submission.question)
                        redis_key = f"{questionQuery.questionId}:{input_data}"
                        redis_client.hset(questionQuery.questionId, input_data, submission.output)
                        redis_client.expire(redis_key, timedelta(seconds=20))
                        submission.delete()
                    except Exception as e:
                        print(e)

                

                # Send the submission data to the WebSocket group
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'submission_{submissionId}',
                    {
                        'type': 'submission_final_status',
                        'submission_data': {
                            'id': submission.id,
                            'input': submission.input,
                            'output': submission.output,
                            'error': submission.error,
                            'mode': submission.mode,
                            'totalSubmissions': submission.totalSubmissions,
                            'correctSubmissions': submission.correctSubmissions,
                            'isCorrect': submission.isCorrect,
                            'finalStat': submission.status,
                            'points': submission.points,
                            'submitted': True if submission.mode == 'SUB' else False
                        }
                    }
                )
                
                return Response({'msg': 'submission Updated'}, status=status.HTTP_200_OK)
            except Exception as e:
                print("Error in callback api",e)
                return Response({'msg': 'Error in saving submission'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StartSubmissionExecution(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StartSubmissionExecutionSerializer(data=request.data)
        print("submissions execution started notify user")
        if serializer.is_valid():
            submissionId = serializer.validated_data.get('submissionId')
            
            try:
                submission = Submission.objects.get(id=submissionId)
                
                # Notify the WebSocket group that the submission execution has started
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'submission_{submissionId}',
                    {
                        'type': 'submission_status_update',
                        'submission_data': {
                            'id': submission.id,
                            'status': 'Execution started',
                        }
                    }
                )

                return Response({'msg': 'Execution started for submission'}, status=status.HTTP_200_OK)
            except Submission.DoesNotExist:
                return Response({'msg': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print("Error in starting submission execution", e)
                return Response({'msg': 'Error in starting submission execution'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


#############################
#                           #
#         Submit API        #
#                           #
#############################


class Submit(viewsets.GenericViewSet,mixins.CreateModelMixin):

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'submit'

    def create(self, request, *args, **kwargs):
        
        data = request.data
        contest_id = self.kwargs['contestId']
        
        print("=> Requested Data ",contest_id)
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():            

            user = self.request.user
            userId = user.id
            team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contest_id)
            question = serializer.validated_data['question']
            contest = get_object_or_404(Contest, contestId=contest_id)
            

            # team = serializer.validated_data['team']

            try:
                    
                serializer.validated_data['mode'] = "SUB"
                serializer.validated_data['status'] = "PEN"
                serializer.validated_data['points'] = 0
                serializer.validated_data['isCorrect'] = False
                serializer.validated_data['team'] = team
                serializer.validated_data['contest'] = contest
                submission = serializer.save()


                payload = {
                    'submissionId': submission.id,
                    'code': data.get('code'), 
                    'language': data.get('language'),  
                    'timeLimit': question.timeLimit,  
                    'question': question.questionId,
                    'input':question.sampleIp
                }

                try:
                    server = getExecutionServer()
                    if not server:
                        return Response({'msg':"No available servers"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    server_ip = server['ip_address']
                    server_port = server['port']

                    server_url = f"http://{server_ip}:{server_port}/core/submit/"  
                    print("api rquest started",server_url)
                    response = requests.post(server_url, data=payload)
                    json_response = response.json() 

                    return Response({'msg': json_response.get('msg'),'submissionId':submission.id},status=status.HTTP_200_OK)


                except Exception as e:
                    print("RequestException:", e)
                    return Response({'msg': "Error communicating with Server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                print(e)
                # deallocate(container)
                print("some wong")
                return Response({'msg':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            print("*******Invalid*******")
            # print(request.data)
            return Response({'msg':serializer.errors})
        



#############################
#                           #
#       Run Code API        #
#                           #
#############################

class RunCode(generics.GenericAPIView):
    serializer_class = SubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'submit'

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        contest_id = self.kwargs['contestId']
        data = request.data

        if serializer.is_valid():
            
            user = self.request.user
            userId = user.id
            team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contest_id)
            question = serializer.validated_data['question']
            contest = get_object_or_404(Contest, contestId=contest_id)

            try:
                print("*******Valid but not saved*******")

                serializer.validated_data['mode'] = "RUN"
                serializer.validated_data['status'] = "PEN"
                serializer.validated_data['points'] = 0
                serializer.validated_data['isCorrect'] = False
                serializer.validated_data['team'] = team
                serializer.validated_data['contest'] = contest
                submission = serializer.save()

                payload = {
                    'submissionId': submission.id,
                    'code': data.get('code'), 
                    'language': data.get('language'),  
                    'timeLimit': question.timeLimit,  
                    'question': question.questionId,
                    'input':serializer.validated_data['input']
                }

                try:
                    server = getExecutionServer()
                    if not server:
                        return Response({'msg':"No available servers"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    server_ip = server['ip_address']
                    server_port = server['port']

                    server_url = f"http://{server_ip}:{server_port}/core/runsubmission/"  
                    print("api rquest started",server_url)
                    response = requests.post(server_url, data=payload)
                    json_response = response.json() 

                    return Response({'msg': json_response.get('msg'),'submissionId':submission.id},status=status.HTTP_200_OK)


                except Exception as e:
                    print("RequestException:", e)
                    return Response({'msg': "Error communicating with Server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
            except:
                return Response({'msg':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        return Response(serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)



def RunRcUtil(question,ip,container):

    correctCodeQuery = CorrectCode.objects.get(question__questionId = question)
    codeStatus=  runCode(correctCodeQuery.question,correctCodeQuery.correct_code,correctCodeQuery.language,False,container,ip)
    # print(codeStatus)
    return {"output":codeStatus.get('output')}

def get_result_from_cache(question_id, input_value):
    # Check if the question ID exists in Redis
    if redis_client.exists(question_id):
        # Check if the input exists for the given question ID
        cached_output = redis_client.hget(question_id, input_value)
        if cached_output is not None:
            # Return the cached output to the user
            return {"output":cached_output.decode('utf-8')}
        return None
        
    return None



class RunRc(generics.GenericAPIView):

    serializer_class = RcSubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'rc'

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        contest_id = self.kwargs['contestId']
        data = request.data

        if serializer.is_valid():
            question = serializer.validated_data['question']
            user_input = serializer.validated_data['input']

            # 1st tryfrom cache if ans is stored or not
            print("checking op")
            try:
                cached_op = get_result_from_cache(question, user_input)
                if cached_op is not None:
                    print("cached op is present")
                    serializer.validated_data['output'] = cached_op
                    cached_op.update(serializer.data)
                    return Response(cached_op)
            except:
                pass
            print("cached op is not present")


            user = self.request.user
            userId = user.id
            team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contest_id)
            question = get_object_or_404(Question, questionId=question)
            correct_code = get_object_or_404(CorrectCode,question=question)
            contest = get_object_or_404(Contest, contestId=contest_id)

            try:
                print("*******Valid but not saved*******")

                submission = Submission.objects.create(
                    mode='RC',
                    status='PEN',
                    team=team,
                    contest=contest,
                    input=user_input,
                    code=correct_code.correct_code,
                    question=question,
                    language=correct_code.language
                )

                payload = {
                    'submissionId': submission.id,
                    'code': correct_code.correct_code, 
                    'language': correct_code.language,  
                    'timeLimit': question.timeLimit,  
                    'question': question.questionId,
                    'input':user_input
                }

                try:
                    server = getExecutionServer()
                    if not server:
                        return Response({'msg':"No available servers"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    server_ip = server['ip_address']
                    server_port = server['port']

                    server_url = f"http://{server_ip}:{server_port}/core/runrcsubmission/"  
                    print("api rquest started",server_url)
                    response = requests.post(server_url, data=payload)
                    json_response = response.json() 

                    return Response({'msg': json_response.get('msg'),'submissionId':submission.id},status=status.HTTP_200_OK)


                except Exception as e:
                    print("RequestException:", e)
                    return Response({'msg': "Error communicating with Server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
            except Exception as e:
                print("Error :", e)
                return Response({'msg':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        return Response(serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)





#############################
#                           #
#         Submit API 2      #
#                           #
#############################
    # Used by integrating docker judge

from .dockerJudgeUtils import *


# class Submit2(viewsets.GenericViewSet,mixins.CreateModelMixin):

#     queryset = Submission.objects.all()
#     serializer_class = SubmissionSerializer
#     renderer_classes = [JSONRenderer]
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated,TimecheckGlobal]
#     throttle_classes = [ScopedRateThrottle]
#     throttle_scope = 'submit'

#     def create(self, request, *args, **kwargs):
        
#         data = request.data
#         contest_id = self.kwargs['contestId']
        
#         # print("=> Requested Data ",data)
#         serializer = SubmissionSerializer(data=data)
#         if serializer.is_valid():

#             container = getActivatedContainer()
#             if not container:
#                 return   Response({'msg':"Server is Busy"},status=status.HTTP_403_FORBIDDEN)
            

#             user = self.request.user
#             userId = user.id
#             team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contest_id)
#             contest = get_object_or_404(Contest, contestId=contest_id)

#             # team = serializer.validated_data['team']

#             code = serializer.validated_data['code']
#             language = serializer.validated_data['language']
#             question = serializer.validated_data['question']

#             input = serializer.validated_data.pop('input', "")
#             # print("=> Serialized Data ",input)
#             isSubmitted = True
#             try:
#                 print("*******Valid  and saved*******")
                
#                 codeStatus=  runCodeDockerJudge(question,code,language,isSubmitted,container,question.timeLimit,input)
#                 print("Output of users submission ",codeStatus)
#                 # return_code_testcase1 = codeStatus["testcase1"]["returnCode"]    #One method to get rc from runCode 
#                 # print("Return code of testcase1:", return_code_testcase1)
                
#                 # print(returnCodeList)
#                 if (codeStatus['finalStat'] == 'AC'):
#                     #It will work when user get all AC submission
                    
#                     serializer.validated_data['status'] = codeStatus['finalStat']

#                     score = self.getMaxScore(question,team,contest)
#                     print("************ score ",score )
#                     serializer.validated_data['points'] = score
#                     serializer.validated_data['isCorrect'] = True

#                     try:
#                         lastSubmissionNumber = Submission.objects.filter(question=question,team=team).last().attemptedNumber
#                         serializer.validated_data['attemptedNumber'] = lastSubmissionNumber+1
#                     except:
#                         serializer.validated_data['attemptedNumber'] = 1
#                     serializer.validated_data['team'] = team
#                     serializer.validated_data['contest'] = contest
#                     serializer.save()

#                     print("i am here")


#                     #This team query to save users score and last update in score
#                     teamQuery= Team.objects.get(teamId = team)

#                     if score !=0:
#                         '''to solve this bug
#                             # if user submite wrong submission there will no change in lastUpdate
#                             # but if user again submit submission there is'''
#                         teamQuery.score += score
#                         teamQuery.lastUpdate = timezone.now()
#                         teamQuery.save()

#                     # Add status of current submission ie pass or not
#                     codeStatus['Submitted'] = True
#                 else:
#                     #When answer is other than AC
#                     serializer.validated_data['status'] = codeStatus['finalStat']
            
#                     serializer.validated_data['points'] = 0
#                     serializer.validated_data['isCorrect'] = False

#                     try:
#                         lastSubmissionNumber = Submission.objects.filter(question=question,team=team).last().attemptedNumber
#                     except:
#                         lastSubmissionNumber = 0
#                     serializer.validated_data['attemptedNumber'] = lastSubmissionNumber+1
#                     serializer.validated_data['team'] = team
#                     serializer.validated_data['contest'] = contest
#                     serializer.save()

#                     # Add status of current submission ie pass or not
#                     codeStatus['Submitted'] = False


#                 # print(question.questionId)    #to get question id from question 
#                 # delete_container.delay(obj_id)
#                 return Response(codeStatus)
#             except Exception as e:
#                 print(e)
#                 # deallocate(container)
#                 print("some wong")
#                 return Response({'msg':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             print("*******Invalid*******")
#             # print(request.data)
#             return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

#     def getMaxScore(self,question,team,contest):
#         questionQuery = modelsQu.Question.objects.get(questionId=question.questionId)
#         # if (questionQuery.category != team.isJunior):
#         #     #if user is trying another category question
#         #     return 0
        
#         points = questionQuery.points
#         maxPoints = questionQuery.maxPoints
#         print("inside get score ",question , team)
        
#         try:
#             submissionQuery = Submission.objects.filter(team = team ,question = question,contest=contest,isCorrect=True).exists()
#             if submissionQuery:
#                 print("Right submission exits")
#                 return 0
#             else:
#                 if (questionQuery.points-1 >= 10):
#                     questionQuery.points -=1
#                     questionQuery.save()

#                 try:
#                     submissionQuery = Submission.objects.filter(team = team ,question = question,contest=contest,isCorrect = False).exists()
#                     if submissionQuery:
#                         penalty = Submission.objects.filter(team = team ,question = question,contest=contest).last().attemptedNumber
                        
#                         score = int(points - (penalty * 0.1 * points))
#                         # print("points -> ",points,"\n maxpoints -> ",maxPoints)
#                         # print("penalty -> ",penalty,"\nScore -> ",score)

#                         if score > 0:
#                             print("score > 0")
#                             print("hello score ",score)
#                             return score
#                         print("score < 0")
#                         #User will get 10 points if its score is negative for right submission
#                         return 10
#                     else:
#                         return points
#                 except:
#                     print("score = maxpoints")
#                     return points
#         except:
#             print("None value is returing ")
#             pass

class Submit2(viewsets.GenericViewSet,mixins.CreateModelMixin):

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'submit'

    def create(self, request, *args, **kwargs):
        
        data = request.data
        contest_id = self.kwargs['contestId']
        
        # print("=> Requested Data ",data)
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():

            container = getActivatedContainer()
            if not container:
                return   Response({'msg':"Server is Busy"},status=status.HTTP_403_FORBIDDEN)
            

            user = self.request.user
            userId = user.id
            team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contest_id)
            contest = get_object_or_404(Contest, contestId=contest_id)

            # team = serializer.validated_data['team']


            input = serializer.validated_data.pop('input', "")
            # print("=> Serialized Data ",input)
            isSubmitted = True
            try:
                    
                serializer.validated_data['status'] = "PEN"
                serializer.validated_data['points'] = 0
                serializer.validated_data['isCorrect'] = False
                serializer.validated_data['team'] = team
                serializer.validated_data['contest'] = contest
                submission = serializer.save()
                print("i am here")

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
        



#############################
#                           #
#       Run Code API 2      #
#                           #
#############################

class RunCode2(generics.GenericAPIView):
    serializer_class = SubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'submit'

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            container = getActivatedContainer()

            try:
                if not container:
                    print("df")
                    return   Response({'msg':"Server is Busy"},status=status.HTTP_403_FORBIDDEN)
            
                print("*******Valid but not saved*******")
                code = serializer.validated_data['code']
                language = serializer.validated_data['language']
                question = serializer.validated_data['question']
                input_data = serializer.validated_data['input']
                isSubmitted = False
                timeLimit = 1

                # print("my data",input_data)
                codeStatus=  runCodeDockerJudge(question,code,language,isSubmitted,container,timeLimit,input_data)
                # codeStatus = codeStatus.get()
                serializer.validated_data['input'] = input_data
                codeStatus.update(serializer.data)
                responce = codeStatus
                # print("responce => ",responce)
                return Response(codeStatus)
            
            except Exception as e:
                # deallocate(container)
                print("errorr => ",e)

                return Response({'msg':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#############################
#                           #
#       Run RC API 2        #
#                           #
#############################
    
def RunRcUtil2(question,ip,container):

    correctCodeQuery = CorrectCode.objects.get(question__questionId = question)
    question = modelsQu.Question.objects.get(questionId=question)
    codeStatus=  runCodeDockerJudge(question,correctCodeQuery.correct_code,correctCodeQuery.language,False,container,1,ip)

    # codeStatus=  runCode(correctCodeQuery.question,correctCodeQuery.correct_code,correctCodeQuery.language,False,container,ip)
    print(codeStatus)
    return {"output":codeStatus.get('output')}

    
class RunRc2(generics.GenericAPIView):

    queryset = Submission.objects.all()
    serializer_class = RcSubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'rc'
        
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            question = serializer.validated_data['question']
            input = serializer.validated_data['input']

            # 1st tryfrom cache if ans is stored or not
            print("checking op")
            try:
                cached_op = get_result_from_cache(question, input)
                if cached_op is not None:
                    print("cached op is present")
                    serializer.validated_data['output'] = cached_op
                    cached_op.update(serializer.data)
                    return Response(cached_op)
            except:
                pass
            print("cached op is not present")

            container = getActivatedContainer()

            try:
                if not container:
                    return   Response({'msg':"Server is Busy"},status=status.HTTP_403_FORBIDDEN)
            
                print("*******Rc IP OP functnality ******")
                
                codeStatus=  RunRcUtil2(question,input,container)
                # print("ffff => ",codeStatus['output'])
                serializer.validated_data['output'] = codeStatus
                codeStatus.update(serializer.data)

                # Storing op in redis
                redis_key = f"{question}:{input}"
                redis_client.hset(question, input, codeStatus['output'])
                redis_client.expire(redis_key, timedelta(seconds=10))
                # codeStatus = serializer.data
                # print("responce => ",codeStatus)
                # deallocate(container)
                return Response(codeStatus)
            
            except Exception as e:
                print(e)
                # deallocate(container)
                return Response({'msg':"Internal server error"},status=status.HTTP_403_FORBIDDEN)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

