from django.db import models
from datetime import datetime
import pytz


class Submission(models.Model):
    submissionId = models.TextField(null=True,blank=True)
    question = models.CharField(max_length=10)

    languageChoice = (
        ('python','python'),
        ('cpp','cpp'),
        ('c','c'),
        ('java','java'),
    )
    language = models.CharField(choices=languageChoice,max_length=10)
    code = models.TextField(null=True,blank=True)
    input = models.TextField(null=True,blank=True)
    output = models.TextField(null=True,blank=True)
    error = models.TextField(null=True,blank=True)
    submissionTime= models.DateTimeField(auto_now_add=True)

    modeChoice = (
        ('RUN','Run Submission'),
        ('SUB','Submit Submission'),
        ('RC','RC Submission'),

    )
    mode = models.CharField(max_length=5,choices=modeChoice,blank=True,null=True)
    statusChoice = (
        ('TLE','Time Limit Exceeded'),
        ('MLE','Memory Limit Exceeded'),
        ('CE','Compilation Error'),
        ('RE','Runtime Error'),
    	('WA','Wrong Answer'), 	
        ('AC' ,'Accepted'),
        ('PEN',"Pending"),
        ('ONF','Output Not Found'),
        ('UE','Unknown Error'),
    )
    status = models.CharField(max_length=5,choices=statusChoice,blank=True,null=True)
    isCorrect = models.BooleanField(default=False)
    correctSubmissions = models.IntegerField(default=0)
    totalSubmissions = models.IntegerField(default=0)

    timeLimit = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.id}"
    

class ActivatedContainer(models.Model):
    containerId = models.CharField(max_length=150)
    disable = models.BooleanField(default=False)
    upTime = models.DateTimeField(auto_now=True)



    @property
    def containerUpTime(self):
        '''To check Up time of container'''
        currentTime = datetime.now(tz=pytz.UTC)
        timeDifference = currentTime - self.upTime
        return timeDifference
    @property
    def uptime_in_minutes(self):
        uptime = datetime.utcnow() - self.upTime.replace(tzinfo=None)
        return int(uptime.total_seconds() / 60)

    def __str__(self) -> str:
        return str(self.containerId)


class TestcaseForQuestion(models.Model):
    question = models.CharField(max_length=10,unique=True)
    contest = models.CharField( max_length=10,blank=True)
    isFetched = models.BooleanField(default=False)