from rest_framework import serializers
from .models import *
from django.db.models import Q

from django.contrib.auth import authenticate
from rest_framework import serializers

class GetSubmissionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Submission
        fields = ['id','team','question','contest','language','code','isCorrect','points','submissionTime','status']


class SubmissionSerializer(serializers.ModelSerializer):
    # input = serializers.CharField()
    input = serializers.CharField(required = False,default="")
    # question = serializers.CharField()
    class Meta:
        model = Submission
        fields = ['question','language','code','input']
        extra_fields = ["team",'contest','attemptedNumber','submissionTime','points','status','isCorrect']
        optional_fields = ['input' ]


class RcSubmissionSerializer(serializers.Serializer):
    input = serializers.CharField(default=None)
    question = serializers.CharField()

class CallBackApiSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    submissionId = serializers.CharField()
    mode = serializers.CharField()
    status = serializers.CharField()
    input = serializers.CharField(allow_blank=True, required=False)
    output = serializers.CharField(allow_blank=True, required=False)
    error = serializers.CharField(allow_blank=True, required=False)
    isCorrect = serializers.BooleanField()
    correctSubmissions = serializers.IntegerField()
    totalSubmissions = serializers.IntegerField()

class StartSubmissionExecutionSerializer(serializers.Serializer):
    submissionId = serializers.CharField()