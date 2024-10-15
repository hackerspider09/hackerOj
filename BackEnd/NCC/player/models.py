from django.db import models
# from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
import datetime
import uuid
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from contest.models import Contest


class User(AbstractUser):
    isLogin = models.BooleanField(default=False)
    

#Team
class Team(models.Model):
    teamId = models.CharField(max_length=10, primary_key=True, editable=False)

    contest = models.ForeignKey(Contest,on_delete=models.CASCADE)

    user1 = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="user2", on_delete=models.CASCADE,blank=True,null=True)
    isLogin = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    isJunior = models.BooleanField(default=True)
    lastUpdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                'contest',
                'user1',
                name='user1_unique_per_contest',
            ),
            UniqueConstraint(
                'contest',
                'user2',
                name='user2_unique_per_contest',
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.teamId:
            self.teamId = str(uuid.uuid4())[:5]
        
        super().save(*args, **kwargs)
    

    def __str__(self) -> str:
        return f"{self.teamId}"
    

'''
Player model for supervision
use if necessory
'''
# class Player(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     teamId = models.OneTOOneField(Team, on_delete=models.CASCADE)
#     loginCount= models.IntegerField(default=0)
#     isStarted = models.BooleanField(default=False)
#     isLogedIn = models.BooleanField(default=False)
#     startTime = models.DateTimeField(null=True,blank=True)    
#     def __str__(self):
#         return f"{self.user}"


class LoginAllow(models.Model):
    '''
    Used to allow developers to login in system,
    when contest is not started.
    '''
    user = models.OneToOneField(User, verbose_name=("allowed user"), on_delete=models.CASCADE)



