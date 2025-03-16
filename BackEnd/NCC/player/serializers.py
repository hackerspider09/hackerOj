from rest_framework import serializers
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import serializers
from contest import models

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    contestId = serializers.CharField(required=True)
    isTeam = serializers.BooleanField(default=False)
    isJunior = serializers.BooleanField(default=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        contestId = attrs.get('contestId')
        isTeam = attrs.get('isTeam')

        if not (models.Contest.objects.filter(contestId=contestId).exists()):
            raise serializers.ValidationError({"contestId":'Contest does not exists.'})

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                # raise serializers.ValidationError('Invalid username or password.')
                attrs['user'] = None

            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        return attrs

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    contestId = serializers.CharField()
    class Meta:
        model = User
        fields = ['username','password']
        extra_fields = ['contestId']
        

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        contest_id = validated_data.get('contestId')
        contest = models.Contest.objects.get(contestId=contest_id)
        team = Team.objects.create(user1=user, contest=contest)
        team.save()
        return user
    

class RegisterSingleUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password1']

    def validate(self, attrs):
        # Check if passwords match
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password":'Passwords do not match.'})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username":'This username is already taken.'})
        
        return attrs

    def create(self, validated_data):
        # Remove the password1 field from validated_data
        validated_data.pop('password1')
        
        user = User.objects.create_user(
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        
        return user

class CreateTeamSerializer(serializers.Serializer):
    username1 = serializers.CharField(max_length=30)
    username2 = serializers.CharField(max_length=30)
    contestId = serializers.CharField(write_only=True)
    isJunior = serializers.BooleanField(default=False)

    class Meta:
        model = Team
        fields = ['username1', 'username2', 'contestId','isJunior']

    def validate(self, attrs):
        
        print("SDfsdf")
        if not User.objects.filter(username=attrs['username1']).exists():
            raise serializers.ValidationError({"username":'username1 not exists.'})
        if not User.objects.filter(username=attrs['username2']).exists():
            raise serializers.ValidationError({"username":'username2 not exists.'})
        if not (models.Contest.objects.filter(contestId=attrs['contestId']).exists()):
            raise serializers.ValidationError({"contestId":'Contest does not exists.'})
            
        # check if users are not part of another team
        contest = Contest.objects.get(contestId=attrs['contestId'])
        user1 = User.objects.get(username=attrs['username1'])
        user2 = User.objects.get(username=attrs['username2'])
        print("kjsdfhkjsdf")
        # Check if the users are already part of a team in this contest
        isPartUser1 = Team.objects.filter(Q(user1=user1) | Q(user2=user1), contest=contest).first()
        isPartUser2 = Team.objects.filter(Q(user1=user2) | Q(user2=user2), contest=contest).first()
        
        if isPartUser1 and isPartUser2:
            # Both users are part of a team
            if isPartUser1.teamId == isPartUser2.teamId:

                raise serializers.ValidationError({"username":'Both users are already in the same team.'})
            else:
                raise serializers.ValidationError({"username":'Users are part of different teams. Register as single users or resolve the teams.'})

        elif isPartUser1 or isPartUser2:
            # One user is already in a team, but the other isn't
            raise serializers.ValidationError({"username":'One of the users is already part of a team. Contact the organiser.'})

        return attrs


    def create(self, validated_data):
        # Remove the password1 field from validated_data
        user1 = User.objects.get(username=validated_data['username1'])
        user2 = User.objects.get(username=validated_data['username2'])
        contest = Contest.objects.get(contestId=validated_data['contestId'])
        print(validated_data,"hello nashe")
        # Create and return the new team
        team = Team.objects.create(
            user1=user1,
            user2=user2,
            contest=contest,
            isJunior=validated_data['isJunior']
        )
        return team