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
    firstName = serializers.SerializerMethodField()  
    lastName = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = models.Participant
        fields = ['total_amount', 'amount', 'plan', 'id', 'firstName', 'lastName' ,'name_status' , 'name' , 'participant_new' , 'agreement' , 'risk_statement' , 'create_date' ]

    def get_firstName(self, obj):
        private_person = privatePerson.objects.filter(user=obj.participant_new).first()
        if private_person:
            return private_person.firstName
        return None

    def get_lastName(self, obj):
        private_person = privatePerson.objects.filter(user=obj.participant_new).first()
        if private_person:
            return private_person.lastName
        return None

    def get_name(self, obj):
        if obj.name_status:
            private_person = privatePerson.objects.filter(user=obj.participant_new).first()
            if private_person:
                return f"{private_person.firstName} {private_person.lastName}"
        return 'نامشخص'

class CommenttSerializer(serializers.ModelSerializer):
    firstName = serializers.SerializerMethodField()  
    lastName = serializers.SerializerMethodField() 

    class Meta:
        model = models.Comment
        fields = ['id', 'comment', 'status', 'known', 'firstName', 'lastName']

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


class DocumationRecieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentationRecieve
        fields = '__all__'