from django.db import models
import uuid
from datetime import datetime
import pytz

class Contest(models.Model):
    contestId = models.CharField(max_length=10, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    startTime = models.DateTimeField(blank=True)
    endTime = models.DateTimeField(blank=True)
    isStarted = models.BooleanField(default=False)
    registrationOpen = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.contestId:
            self.contestId = str(uuid.uuid4())[:5]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.contestId}"






class Container(models.Model):
    containerId = models.IntegerField(unique=True)
    status = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    upTime = models.DateTimeField(auto_now=True)


    @property
    def containerUpTime(self):
        '''To check Up time of container'''
        currentTime = datetime.now(tz=pytz.UTC)
        timeDifference = currentTime - self.upTime
        return timeDifference
        # return 2

class DockerJudgeContainer(models.Model):
    vm = models.IntegerField(default=0)
    maxNumber= models.IntegerField(default=10)

    def __str__(self) -> str:
        return str(f'{self.vm}')



class ActivatedContainer(models.Model):
    vm=models.ForeignKey(DockerJudgeContainer, on_delete=models.CASCADE)
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

# class Result(models.Model):
#     teamId = models.CharField(max_length=10, primary_key=True, editable=False)
#     isLogin = models.BooleanField(default=False)
#     score = models.IntegerField(default=0)
#     isJunior = models.BooleanField(default=True)
#     questions_attempted = models.IntegerField(default=0)
#     questions_solved = models.IntegerField(default=0)


class ExecutionServers(models.Model):
    address = models.CharField(max_length=50, unique=True,blank=False)
    port = models.CharField(max_length=10,blank=False)

    def __str__(self) -> str:
        return str(self.address)
