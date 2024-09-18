from rest_framework import serializers
from . import models
from authentication.models import User , privatePerson


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
    firstName = serializers.SerializerMethodField()  # فیلد firstName از privatePerson
    lastName = serializers.SerializerMethodField()   # فیلد lastName از privatePerson
    mobile = serializers.CharField(source='user.mobile')
    uniqueIdentifier = serializers.CharField(source='user.uniqueIdentifier')
    referal = serializers.CharField(source='user.referal')

    class Meta:
        model = models.Comment
        fields = ['id', 'comment', 'status', 'known', 'firstName', 'lastName', 'mobile', 'uniqueIdentifier', 'referal']

    def get_firstName(self, obj):
        private_person = privatePerson.objects.filter(user=obj.user).first()
        if private_person:
            return private_person.firstName
        return None

    def get_lastName(self, obj):
        private_person = privatePerson.objects.filter(user=obj.user).first()
        if private_person:
            return private_person.lastName
        return None
