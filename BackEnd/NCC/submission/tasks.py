from celery import shared_task
from contest import models as modelC  
from question import models as modelQ
from player import models as modelP
from . import models as modelsS
import docker
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
import redis

from . import dockerJudgeUtils
from .utils import *

from django.utils import timezone

crntVM = settings.VM

client = docker.from_env()

redis_client = redis.StrictRedis(host=settings.REDIS_HOST_IP, port=6379, db=0)

@shared_task
def run_submissions_scheduler():
    try:
        container = getActivatedContainer()
        if not container:
            return
        
        submission = modelsS.Submission.objects.filter(status="PEN").first()
        print(submission)
        if(submission is None):
            print("No Submissions")
            return
        
        question = modelQ.Question.objects.get(questionId=submission.question)
        team = modelP.Team.objects.get(teamId=submission.team)
        contest = modelC.Contest.objects.get(contestId=submission.contest)

        isSubmitted = True
        input_data = ""
        code_status = dockerJudgeUtils.runCodeDockerJudge(submission.question, submission.code, submission.language, isSubmitted, container, question.timeLimit, input_data)
        
        # Update submission status based on processing result
        if code_status['finalStat'] == 'AC':
            # Update submission details for correct submission
            score = getMaxScore(question,team,contest)

            submission.status = code_status['finalStat']
            submission.isCorrect = True
            submission.points = score

            if score !=0:
                '''to solve this bug
                    # if user submite wrong submission there will no change in lastUpdate
                    # but if user again submit submission there is'''
                team.score += score
                team.lastUpdate = timezone.now()
                team.save()


        else:
            # Update submission details for incorrect submission
            submission.status = code_status['finalStat']
            submission.points = 0
            submission.isCorrect = False
        
        submission.save()

    except Exception as e:
        print(f"Error processing submission : {e}")


@shared_task()
def delete_container():
    print(crntVM)

    try:
        containerCountQuery = modelC.DockerJudgeContainer.objects.get(vm=crntVM)
        activatedContainerQuery = modelC.ActivatedContainer.objects.filter(disable=False,vm=containerCountQuery)


        try:
            for container in activatedContainerQuery:
                # if container.uptime_in_minutes >2:
                #     print("my container ",container.containerId)
                try:
                    runningContainer = client.containers.get(container.containerId)
                    runningContainer.remove(force=True)
                    container.disable = True
                    container.save()
                except:
                    pass
        except Exception as e:
            print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")


@shared_task
def check_container_uptime():
    print("beast worker")
    try:
        containerCountQuery = modelC.DockerJudgeContainer.objects.get(vm=crntVM)
        activatedContainerQuery = modelC.ActivatedContainer.objects.filter(disable=False,vm=containerCountQuery)


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


@shared_task
def get_Testcases():

    events = modelC.Contest.objects.filter(isStarted=True)
    if (events.exists()):
        event = events[0]
        try:
            questions = modelQ.Question.objects.filter(contest=event.contestId)
            for question in questions:
                print("question ",question)
                question.testcaseLoaded = False
                cache_key = f"testcases_{question.questionId}"  
                # print("from tasks" ,cache_key)
                cached_data = cache.get(cache_key)
                # if not cached_data:
                print("testcase  caching start")
                testcases = modelQ.Testcase.objects.filter(question=question).order_by('testcaseNumber')
                inputList = []
                try:
                    for testcase in testcases:
                        print("question ",question,"testcase ",testcase.testcaseNumber)
                        ip_content = testcase.inputFile.read()
                        op_content = testcase.outputFile.read()
                        ip_content_str = ip_content.decode('utf-8').strip().replace('\r','')
                        op_content_str = op_content.decode('utf-8').strip().replace('\r','')

                        # Assuming ip_content_str and op_content_str are strings
                        ip_content_bytes = ip_content_str.encode('utf-8')
                        op_content_bytes = op_content_str.encode('utf-8')


                        inputTuple = (ip_content_bytes, op_content_bytes)
                        # print("ip filev ",inputTuple)
                        inputList.append(inputTuple) 
                    # print(inputList)
                    cache.set(cache_key, inputList, timeout=60*60*3)  
                    question.testcaseLoaded = True
                except Exception as e:
                    print(e)
                    question.testcaseLoaded = False
                question.save()
                    # print(cached_data)
        except Exception as e:
            print("error in testcase from dropbox ",e)
    else:
        print("There are multiple active events")

@shared_task
def get_Testcase(questionID):

    try:
        question = modelQ.Question.objects.get(questionId=questionID)
        print("question ",question)
        question.testcaseLoaded = False
        cache_key = f"testcases_{question.questionId}"  
        print("from tasks" ,cache_key)
        cached_data = cache.get(cache_key)
        try:
            cache.delete(cache_key)
        except:
            pass
        # if not cached_data:
        print("testcase  caching start...")
        testcases = modelQ.Testcase.objects.filter(question=question).order_by('testcaseNumber')
        inputList = []
        try:
            for testcase in testcases:
                print("question ",question,"testcase ",testcase.testcaseNumber)
                ip_content = testcase.inputFile.read()
                op_content = testcase.outputFile.read()
                ip_content_str = ip_content.decode('utf-8').strip().replace('\r','')
                op_content_str = op_content.decode('utf-8').strip().replace('\r','')

                # Assuming ip_content_str and op_content_str are strings
                ip_content_bytes = ip_content_str.encode('utf-8')
                op_content_bytes = op_content_str.encode('utf-8')


                inputTuple = (ip_content_bytes, op_content_bytes)

                # print("ip filev ",inputTuple)
                inputList.append(inputTuple) 
            cache.set(cache_key, inputList, timeout=60*60*3)  
            question.testcaseLoaded = True
        except:
            question.testcaseLoaded = False
        question.save()
                # print(cached_data)
    except Exception as e:
        print("error in testcase from dropbox ",e)

@shared_task
def process_submission(submission_id):
    print("hellllllo")
    try:
        container = getActivatedContainer()
        if not container:
            return
        
        submission = modelsS.Submission.objects.get(id=submission_id)
        question = modelQ.Question.objects.get(questionId=submission.question)
        team = modelP.Team.objects.get(teamId=submission.team)
        contest = modelC.Contest.objects.get(contestId=submission.contest)

        isSubmitted = True
        input_data = ""
        print("byeeee")
        code_status = dockerJudgeUtils.runCodeDockerJudge(submission.question, submission.code, submission.language, isSubmitted, container, question.timeLimit, input_data)
        
        # Update submission status based on processing result
        if code_status['finalStat'] == 'AC':
            # Update submission details for correct submission
            score = getMaxScore(question,team,contest)

            submission.status = code_status['finalStat']
            submission.isCorrect = True
            submission.points = score

            if score !=0:
                '''to solve this bug
                    # if user submite wrong submission there will no change in lastUpdate
                    # but if user again submit submission there is'''
                team.score += score
                team.lastUpdate = timezone.now()
                team.save()


        else:
            # Update submission details for incorrect submission
            submission.status = code_status['finalStat']
            submission.points = 0
            submission.isCorrect = False
        
        submission.save()

    except Exception as e:
        print(f"Error processing submission {submission_id}: {e}")

def getMaxScore(questionId,team,contest):
        questionQuery = modelQ.Question.objects.get(questionId=questionId)
        # if (questionQuery.category != team.isJunior):
        #     #if user is trying another category question
        #     return 0
        
        points = questionQuery.points
        maxPoints = questionQuery.maxPoints
        print("inside get score ",questionQuery , team)
        
        try:
            submissionQuery = modelsS.Submission.objects.filter(team = team ,question = questionQuery,contest=contest,isCorrect=True).exists()
            if submissionQuery:
                print("Right submission exits")
                return 0
            else:

                try:
                    submissionQuery = modelsS.Submission.objects.filter(team = team ,question = questionQuery,contest=contest,isCorrect = False).exists()
                    if submissionQuery:
                        penalty = modelsS.Submission.objects.filter(team = team ,question = questionQuery,contest=contest).last().attemptedNumber
                        
                        score = int(points - (penalty * 0.1 * points))
                        # print("points -> ",points,"\n maxpoints -> ",maxPoints)
                        # print("penalty -> ",penalty,"\nScore -> ",score)

                        if score > 0:
                            print("score > 0")
                            print("hello score ",score)
                            return score
                        print("score < 0")
                        #User will get 10 points if its score is negative for right submission
                        return 10
                    else:
                        return points
                except:
                    print("score = maxpoints")
                    return points
        except:
            print("None value is returing ")
            pass