from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models
from investor.serializers import CartSerializer




class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manager
        fields = '__all__'



class CartWithManagersSerializer(serializers.ModelSerializer):
    managers = ManagerSerializer(many=True, read_only=True, source='manager_set')

    class Meta:
        model = models.Cart
        fields = '__all__'

class ResumeSerializer (serializers.ModelSerializer):
    manager = ManagerSerializer(read_only=True)
    class Meta:
        model = models.Resume
        fields = '__all__'

class ShareholderSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Shareholder
        fields = '__all__'

class ValidationSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Validation
        fields = '__all__'
