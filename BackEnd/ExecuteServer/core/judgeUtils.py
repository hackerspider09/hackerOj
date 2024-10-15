from . import tasks
from .models import *
from django.conf import settings


# def runCodeDockerJudge(question,code,language,isSubmitted,container,timeLimit=1,input_data=None):

#     if not (isSubmitted):
#         # print(input_data)
#         TC_OP = execteRun(language,code,timeLimit,input_data)
#         return TC_OP

#     TC_OP = executeSubmit(language,code,timeLimit,question)
#     return TC_OP


# def deleteContainerById(obj):
#     container_id = obj[2].id
#     containerObj = ActivatedContainer.objects.create(containerId=container_id)

#     tasks.delete_container.delay()