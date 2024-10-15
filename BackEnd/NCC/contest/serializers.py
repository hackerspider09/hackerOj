from rest_framework import serializers
from .models import *


class GetTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = "__all__"

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = "__all__"


class ActivatedContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivatedContainer
        fields = ['id','containerId','disable','upTime','vm','uptime_in_minutes']

class ExecutionServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionServers
        fields = "__all__"