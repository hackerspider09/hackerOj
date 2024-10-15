from . import tasks
from contest import models as modelC
from django.conf import settings

crntVM = settings.VM

# def runCodeDockerJudge(question,code,language,isSubmitted,container,timeLimit=1,input_data=None):

#     if not (isSubmitted):
#         # print(input_data)
#         TC_OP = execteRun(language,code,timeLimit,input_data)
#         return TC_OP

#     TC_OP = executeSubmit(language,code,timeLimit,question)
#     return TC_OP


def deleteContainerById(obj):
    container_id = obj[2].id
    dockerJudgeContainerQuery = modelC.DockerJudgeContainer.objects.get(vm=crntVM)
    containerObj = modelC.ActivatedContainer.objects.create(containerId=container_id,vm=dockerJudgeContainerQuery)

    tasks.delete_container.delay()