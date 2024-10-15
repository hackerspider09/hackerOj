from rest_framework import serializers
from .models import *
from django.db.models import Q

from django.contrib.auth import authenticate
from rest_framework import serializers
# from .models import Result

from player.models import Team,User
from question.models import Question
from submission.models import Submission
      


# class RatingSerializer(serializers.ModelSerializer):
#      user = serializers.CharField(required = False)
#      rating = serializers.IntegerField()
#      class Meta:
#         model = Rating
#         fields = ["id","user","rating","feedBack"]


class IndividualLeaderBoardSerializer(serializers.ModelSerializer):
    '''
    this serializer gives leaderboard 
    with questions score 
    this serializer gives all player's required queryset
    in leaderboard api it get sorted accordingly 
    '''
    questionSolvedByUser = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    user1 = serializers.CharField()
    user2 = serializers.CharField()
    class Meta:
        model = Team
        fields = ('teamId','user1','user2','score', 'lastUpdate', 'questionSolvedByUser','rank')

    def get_questionSolvedByUser(self, obj):
        team = Team.objects.get(teamId = obj)
        questionQueryset = Question.objects.filter(Q(category= "junior" if obj.isJunior else "senior" ) | Q(category="both"),contest=team.contest).order_by("questionNumber")    #return  questions filtered with two same conditions
        QDict = {}
        submissionQueryset = Submission.objects.filter(isCorrect  = True,team=team)
        i=1
        for question in questionQueryset:
            try:
                q = submissionQueryset.filter(question = question.questionId , isCorrect = True , points__gt=0).last()
                QDict[f"Q{i}"]=q.points
            except:
                QDict[f"Q{i}"]=0
            i+=1

        return QDict
    
    def get_rank(self,obj):
        queryset = Team.objects.filter(isJunior=obj.isJunior,contest=obj.contest).order_by('-score', 'lastUpdate')
        ranked_queryset = list(enumerate(queryset, start=1))  # Enumerate the queryset with ranks

        for rank, player in ranked_queryset:
            if player.teamId == obj.teamId:  # Find the player in the ranked queryset
                return rank

        return None
    

class LeaderBoardSerializer(IndividualLeaderBoardSerializer):
    class Meta:
        model = Team
        fields = ('teamId','user1','user2','score', 'lastUpdate', 'questionSolvedByUser','rank')




# class RegisterSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True, required=True)
#     password1 = serializers.CharField(write_only=True, required=True)


#     class Meta:
#         model = User
#         fields = ('username','password', 'password1','email','first_name', 'last_name')
#         extra_kwargs = {

#             'first_name': {'required': False},
#             'last_name': {'required': False},
#         }

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password1']:
#             raise serializers.ValidationError({"password": "Password fields didn't match For user ."})
        
#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#         user.set_password(validated_data['password'])
#         user.save()

#         return user
    
# class TeamRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = ['user1','user2','isJunior']
#         extra_kwargs = {
#             'score': {'required': False},
#             'lastUpdate': {'required': False},
#         }
    

# class GetTimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContestTime
#         fields = "__all__"

# # class ResultSerializer(serializers.ModelSerializer):
# #     teamId =serializers.CharField(max_length=10, editable=False)
# #     isLogin = serializers.BooleanField(default=False)
# #     score = serializers.IntegerField(default=0)
# #     isJunior = serializers.BooleanField(default=True)
# #     questions_attempted = serializers.IntegerField(default=0)
# #     questions_solved = serializers.IntegerField(default=0)

# #     class Meta :
# #         model = Result
# #         field= ('teamId','score','questions_attempted','questions_solved')
    