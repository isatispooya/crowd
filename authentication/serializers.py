from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class OtpSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.Otp
        fields = '__all__'



class AdminSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.Admin
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.Admin
        fields = '__all__'


class addressesSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.addresses
        fields = '__all__'


class accountsSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.accounts
        fields = '__all__'


class privatePersonSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.privatePerson
        fields = '__all__'


class jobInfoSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.jobInfo
        fields = '__all__'


class tradingCodesSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.tradingCodes
        fields = '__all__'


class financialInfoSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.financialInfo
        fields = '__all__'

