from celery import shared_task
from .models import *
import docker
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
import redis
import requests

from . import dockerJudgeUtils
from .utils import *
from django.conf import settings
from django.utils import timezone


client = docker.from_env()

redis_client = redis.StrictRedis(host=settings.REDIS_HOST_IP, port=settings.REDIS_PORT, db=0)

# on same device dont use localhost use device ip
# or make network and add all services under same network


@shared_task
def run_submissions_scheduler():
    try:        
        submission = Submission.objects.filter(status="PEN",mode="SUB").first()
        if(submission is None):
            print("No Submissions")
            return
        

        isSubmitted = True
        input_data = ""
        code_status = dockerJudgeUtils.runCodeDockerJudge(submission.question, submission.code, submission.language, isSubmitted, submission.timeLimit, input_data)
        print('code op ',code_status)
        
        # Update submission status based on processing result
        submission.status = code_status['finalStat'] if code_status['finalStat'] is not None else 'UE'
        submission.totalSubmissions = code_status['totalTestcase']
        submission.correctSubmissions = code_status['status'].count('AC')

        if code_status['finalStat'] == 'AC':
            # Update submission details for correct submission
            submission.isCorrect = True
        else:
            # Update submission details for incorrect submission
            submission.isCorrect = False
        
        submission.save()

    except Exception as e:
        print(f"Error processing submission : {e}")


@shared_task()
def delete_container():

    try:
        activatedContainerQuery = ActivatedContainer.objects.filter(disable=False)
        print("container delete started")

        try:
            for container in activatedContainerQuery:
                # if container.uptime_in_minutes >2:
                #     print("my container ",container.containerId)
                runningContainer = client.containers.get(container.containerId)
                runningContainer.remove(force=True)
                container.disable = True
                container.save()
        except Exception as e:
            print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")


@shared_task
def check_container_uptime():
    print("beast worker")
    try:
        activatedContainerQuery = ActivatedContainer.objects.filter(disable=False)


        try:
            for container in activatedContainerQuery:
                if container.uptime_in_minutes >2:
                    print("my container ",container.containerId)
                    runningContainer = client.containers.get(container.containerId)
                    runningContainer.remove(force=True)
                    container.disable = True
                    container.save()
        except Exception as e:
            print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")



# @shared_task
# def get_Testcase(questionID):

#     try:
#         question = modelQ.Question.objects.get(questionId=questionID)
#         print("question ",question)
#         question.testcaseLoaded = False
#         cache_key = f"testcases_{question.questionId}"  
#         print("from tasks" ,cache_key)
#         cached_data = cache.get(cache_key)
#         try:
#             cache.delete(cache_key)
#         except:
#             pass
#         # if not cached_data:
#         print("testcase  caching start...")
#         testcases = modelQ.Testcase.objects.filter(question=question).order_by('testcaseNumber')
#         inputList = []
#         try:
#             for testcase in testcases:
#                 print("question ",question,"testcase ",testcase.testcaseNumber)
#                 ip_content = testcase.inputFile.read()
#                 op_content = testcase.outputFile.read()
#                 ip_content_str = ip_content.decode('utf-8').strip().replace('\r','')
#                 op_content_str = op_content.decode('utf-8').strip().replace('\r','')

#                 # Assuming ip_content_str and op_content_str are strings
#                 ip_content_bytes = ip_content_str.encode('utf-8')
#                 op_content_bytes = op_content_str.encode('utf-8')


#                 inputTuple = (ip_content_bytes, op_content_bytes)

#                 # print("ip filev ",inputTuple)
#                 inputList.append(inputTuple) 
#             cache.set(cache_key, inputList, timeout=60*60*3)  
#             question.testcaseLoaded = True
#         except:
#             question.testcaseLoaded = False
#         question.save()
#                 # print(cached_data)
#     except Exception as e:
#         print("error in testcase from dropbox ",e)


def testcaseUtil(testcases,questionID):
    inputList = []

    for testcase in testcases:
        print(f"Processing testcase {testcase['testcaseNumber']} for question {questionID}")
        # Decode the input and output files
        ip_content = requests.get(testcase['inputFile']).content
        op_content = requests.get(testcase['outputFile']).content
        ip_content_str = ip_content.decode('utf-8').strip().replace('\r', '')
        op_content_str = op_content.decode('utf-8').strip().replace('\r', '')
        # Encode back to bytes if needed
        ip_content_bytes = ip_content_str.encode('utf-8')
        op_content_bytes = op_content_str.encode('utf-8')
        # Create the tuple and add to the list
        inputTuple = (ip_content_bytes, op_content_bytes)
        inputList.append(inputTuple)

    return inputList

@shared_task
def get_Testcase(questionID,contestId):
    try:
        
        # Cache key
        cache_key = f"testcases_{questionID}"
        print("from tasks", cache_key)
        
        # Clear previous cache if any
        try:
            cache.delete(cache_key)
        except:
            pass

        if (contestId is not None and questionID is not None ):
            print("hiii")
            questionQuery,created = TestcaseForQuestion.objects.get_or_create(question=questionID,contest=contestId)
            
            # Make API call to fetch test cases
            api_url = f"{settings.MAIN_SERVER_URL}/question/gettestcases/?question_id={questionID}"
            response = requests.get(api_url)

            if response.status_code == 200:
                testcases = response.json()
                inputList = testcaseUtil(testcases,questionID)

                # Cache the processed test cases
                cache.set(cache_key, inputList, timeout=60*60*3)

                questionQuery.isFetched = True
                questionQuery.save()
                print(f"testcase fetch for {questionID}")
            else:
                print(f"Failed to fetch test cases from API, status code: {response.status_code}")

        elif(questionID is None and contestId is not None):
            api_url = f"{settings.MAIN_SERVER_URL}/question/{contestId}/get_questions_id/"
            response = requests.get(api_url)    
            # print(response.text)
            if(response.status_code==200):
                data = response.json() 
                for quesData in data:
                    questionQuery =  TestcaseForQuestion.objects.get_or_create(question=quesData['questionId'],contest=contestId)
                    get_Testcase.delay(quesData['questionId'],contestId)
        else:
            print("error in fetching testcases") 
    except Exception as e:
        print("Error in fetching or processing test cases from API:", e)

@shared_task
def process_submission(submission_id):
    print("hellllllo")
    try:
        
        submission = Submission.objects.get(id=submission_id)
        try:
            callBackForInform(submission)
        except:
            pass

        isSubmitted = True
        input_data = ""
        print("byeeee")
        code_status = dockerJudgeUtils.runCodeDockerJudge(submission.question, submission.code, submission.language, isSubmitted, submission.timeLimit, input_data)
        print('code op ',code_status)
        
        # Update submission status based on processing result
        submission.status = code_status['finalStat'] if code_status['finalStat'] is not None else 'UE'
        submission.totalSubmissions = code_status['totalTestcase']
        submission.correctSubmissions = code_status['status'].count('AC')

        if code_status['finalStat'] == 'AC':
            # Update submission details for correct submission
            submission.isCorrect = True
        else:
            # Update submission details for incorrect submission
            submission.isCorrect = False
        
        submission.save()

        try:
            callBackApiFunction(submission)
        except Exception as e:
            print("error in updating submission in main server")

    except Exception as e:
        print(f"Error processing submission {submission_id}: {e}")

@shared_task
def process_run_submission(submission_id):
    print("hellllllo")
    try:
        
        submission = Submission.objects.get(id=submission_id)
        try:
            callBackForInform(submission)
        except:
            pass

        isSubmitted = False
        input_data = submission.input
        print("byeeee")
        code_status = dockerJudgeUtils.runCodeDockerJudge(submission.question, submission.code, submission.language, isSubmitted, submission.timeLimit, input_data)
        print('code op ',code_status)
        
        # Update submission status based on processing result
        submission.status = code_status['status'] if code_status['status'] is not None else 'UE'
        submission.output = code_status['output']
        submission.error = code_status['error']

        if code_status['status'] == 'AC':
            # Update submission details for correct submission
            submission.isCorrect = True
        else:
            # Update submission details for incorrect submission
            submission.isCorrect = False
        
        submission.save()
        try:
            callBackApiFunction(submission)
        except Exception as e:
            print("error in updating submission in main server")

    except Exception as e:
        print(f"Error processing submission {submission_id}: {e}")

