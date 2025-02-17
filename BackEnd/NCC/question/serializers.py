from rest_framework import serializers
from .models import *
from submission import models as modelsSb
from player import models as modelsTm
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import serializers
from contest import models
from django.conf import settings
from django.core.files.storage import default_storage

class QuestionIdOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["questionId","questionNumber"]

class QuestionSerializer(serializers.ModelSerializer):
    solvedByTeam = serializers.SerializerMethodField()
    accuracy = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = "__all__"
        extra_fields = ["solvedByTeam","accuracy"]
        
    def get_solvedByTeam(self, obj):
        user = self.context['request'].user
        contest_id = self.context.get('request').parser_context.get('kwargs').get('contestId')

        team = modelsTm.Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contest_id)

        return modelsSb.Submission.objects.filter(team=team, question=obj, isCorrect=True,mode="SUB").exists()
        
    def get_accuracy(self,obj):
        submissions = modelsSb.Submission.objects.filter(question = obj,mode="SUB")
        
        actual_sub = len(submissions)
        right_sub=len(submissions.filter(isCorrect=True))
        try:
            accuracy = round((right_sub/actual_sub)*100)
        except:
            print("SDfsd")
            accuracy = 0

        return accuracy
    
class TestcaseSerializer(serializers.ModelSerializer):
    inputFile = serializers.SerializerMethodField()
    outputFile = serializers.SerializerMethodField()
    class Meta:
        model = Testcase
        fields = ['id', 'question', 'testcaseNumber', 'inputFile', 'outputFile']

    def get_inputFile(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.inputFile.url)

    def get_outputFile(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.outputFile.url)
