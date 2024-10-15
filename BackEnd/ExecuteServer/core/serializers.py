from rest_framework import serializers
from .models import *

from django.contrib.auth import authenticate
from rest_framework import serializers


class GetSubmissionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Submission
        fields = ['id','submissionId','mode','status','input','output','error','isCorrect','correctSubmissions','totalSubmissions']

class ActivatedContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivatedContainer
        fields = ['id','containerId','disable','upTime','uptime_in_minutes']

class CheckTestcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestcaseForQuestion
        fields = "__all__"


class SubmissionSerializer(serializers.ModelSerializer):
    # input = serializers.CharField()
    input = serializers.CharField(required = False,default="")
    # question = serializers.CharField()
    class Meta:
        model = Submission
        fields = ['question','submissionId','language','code','timeLimit','input']
        extra_fields = ['submissionTime','status','mode','isCorrect']
        optional_fields = ['input' ]


class RcSubmissionSerializer(serializers.Serializer):
    input = serializers.CharField(default=None)
    question = serializers.CharField()

