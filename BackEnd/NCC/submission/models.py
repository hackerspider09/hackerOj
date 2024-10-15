from django.db import models
from question.models import Question
from player.models import Team
from contest.models import Contest

class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest,on_delete=models.CASCADE)
    input = models.TextField(null=True,blank=True)
    output = models.TextField(null=True,blank=True)
    error = models.TextField(null=True,blank=True)
    modeChoice = (
        ('RUN','Run Submission'),
        ('SUB','Submit Submission'),
        
    )
    mode = models.CharField(max_length=5,choices=modeChoice,blank=True,null=True)
    
    languageChoice = (
        ('python','python'),
        ('cpp','cpp'),
        ('c','c'),
        ('java','java'),
    )
    language = models.CharField(choices=languageChoice,max_length=10)
    code = models.TextField(null=True,blank=True)
    points = models.IntegerField(default=0)
    attemptedNumber = models.IntegerField(default=0)
    submissionTime= models.DateTimeField(auto_now_add=True)


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

    def __str__(self):
        return f"{self.team}"
    


class CorrectCode(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    
    correct_code = models.TextField()
    lang_choice = [
        ("python","python"),("cpp","cpp"),("c","c"),("java","java")
    ]
    language = models.CharField( max_length=10 , choices = lang_choice)

    def __str__(self):
        return f"{self.question.questionId}"

