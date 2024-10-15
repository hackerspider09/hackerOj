from django.contrib import admin
from .models import *

class SubmissionAdmin (admin.ModelAdmin):
    list_display = ('id',"team","question","contest","language","status","isCorrect","submissionTime","points","attemptedNumber")
admin.site.register(Submission,SubmissionAdmin)

class CorrectCodeAdmin (admin.ModelAdmin):
    list_display = ("question","correct_code","language")
admin.site.register(CorrectCode,CorrectCodeAdmin)