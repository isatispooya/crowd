from rest_framework import serializers
from . import models
from authentication.serializers import UserSerializer



class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = '__all__'



class DocumentationSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(many=True, read_only=True, source='plan_set')
    class Meta:
        model = models.DocumentationFiles
        fields = '__all__'



class AppendicesSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(many=True, read_only=True, source='plan_set')
    class Meta:
        model = models.Appendices
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(many=True, read_only=True, source='plan_set')
    class Meta:
        model = models.Participant
        fields = '__all__'


class CommenttSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(many=True, read_only=True, source='plan_set')
    user = UserSerializer(many=True, read_only=True, source='user_set')
    class Meta:
        model = models.Comment
        fields = '__all__'

