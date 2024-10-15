from django.contrib import admin
from import_export.admin import ExportActionMixin
from .models import *



class ContestAdmin (admin.ModelAdmin):
    list_display = ("contestId","name","startTime","endTime","registrationOpen")
admin.site.register(Contest,ContestAdmin)




class ContainerAdmin(admin.ModelAdmin):
    list_display= ("id","containerId","count","status","containerUpTime")
admin.site.register(Container,ContainerAdmin)

class DockerJudgeContainerAdmin(admin.ModelAdmin):
    list_display= ("id","vm","maxNumber")
admin.site.register(DockerJudgeContainer,DockerJudgeContainerAdmin)

class ActivatedContainerAdmin(admin.ModelAdmin):
    list_display= ("id","containerId","vm","disable","containerUpTime","uptime_in_minutes")
admin.site.register(ActivatedContainer,ActivatedContainerAdmin)

class ExecutionServerAdmin(admin.ModelAdmin):
    list_display= ("id","address","port")
admin.site.register(ExecutionServers,ExecutionServerAdmin)





# class ResultAdmin(admin.ModelAdmin):
#     list_display= ('teamId','score','questions_attempted','questions_solved')
# admin.site.register(Result,ResultAdmin)


