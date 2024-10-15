from django.contrib import admin
from .models import *

class SubmissionAdmin (admin.ModelAdmin):
    list_display = ('id',"question","language","status","isCorrect","submissionTime")
admin.site.register(Submission,SubmissionAdmin)


class ActivatedContainerAdmin(admin.ModelAdmin):
    list_display= ("id","containerId","disable","containerUpTime","uptime_in_minutes")
admin.site.register(ActivatedContainer,ActivatedContainerAdmin)
