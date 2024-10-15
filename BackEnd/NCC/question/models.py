from django.db import models
import uuid
from django.db.models import UniqueConstraint


# Text Editor
from tinymce import models as mc
from contest import models as modelsCo

# Question model
class Question(models.Model):
    contest = models.ForeignKey(modelsCo.Contest,on_delete=models.CASCADE)

    questionId = models.CharField(max_length=10,primary_key=True,editable=False)
    questionNumber = models.IntegerField()

    title =models.CharField(max_length=100)
    description = mc.HTMLField(null=True,blank=True)
    
    # ipFormate = mc.HTMLField(null=True,blank=True)
    # opFormate = mc.HTMLField(null=True,blank=True)

    # constraints = mc.HTMLField(null=True,blank=True)

    # inputOutputBlock = mc.HTMLField(null=True,blank=True)

    sampleIp = models.TextField(null=True,blank=True)
    sampleOp = models.TextField(null=True,blank=True)
    
    difficultyText = models.CharField(default="Easy",max_length=10)
    difficultyLevel = models.IntegerField(default=0)
    maxPoints = models.IntegerField(default=0)  # remain constant till end
    points = models.IntegerField(default=0)   # can change (when submission is right points will be decresed)


    timeLimit = models.IntegerField(default=1)
    memoryLimit = models.IntegerField(default=524288)
    
    accuracy = models.IntegerField(default=0)
    totalSubmissions = models.IntegerField(default=0)
    author = models.CharField(max_length=100,default="")

    category_choice= [("junior","junior"),("senior","senior"),("both","both")]
    category = models.CharField(choices=category_choice, max_length=10,null=True)

    expose = models.BooleanField(default=True)   # Allow to question to expose to user (showable)
    testcaseLoaded = models.BooleanField(default=False)
    class Meta:
        
        constraints = [
                UniqueConstraint(
                    'contest',
                    'questionNumber',
                    name='contest_questionNumber_unique',
                ),
            ]
    def save(self,*args, **kwargs):
        if not self.questionId:
            self.questionId = str(uuid.uuid4())[:5]
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        # return str(self.questionNumber)
        return str(self.questionId)

#Testcases
def getIpPath(instance,filename):
    return str(f"testcases/question{instance.question}/input/{filename}")
def getOpPath(instance,filename):
    return str(f"testcases/question{instance.question}/output/{filename}")

class Testcase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    testcaseNumber = models.IntegerField()  
    inputFile = models.FileField( upload_to=getIpPath, blank=True,verbose_name="Testcase Input")
    outputFile = models.FileField( upload_to=getOpPath, blank=True,verbose_name="Testcase Output") 
    class Meta:
        
        constraints = [
                UniqueConstraint(
                    'question',
                    'testcaseNumber',
                    name='question_testcaseNumber_unique',
                ),
            ]
        
    def __str__(self):
        return f"{self.question}"
    
