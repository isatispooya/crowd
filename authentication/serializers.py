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


class addressesSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.addresses
        fields = '__all__'

    some_field = serializers.CharField(allow_blank=True, required=False)
    another_field = serializers.IntegerField(required=False, allow_null=True)

class accountsSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.accounts
        fields = '__all__'
    some_field = serializers.CharField(allow_blank=True, required=False)
    another_field = serializers.IntegerField(required=False, allow_null=True)

class privatePersonSerializer(serializers.ModelSerializer):
    uniqueIdentifier = serializers.CharField(source='user.uniqueIdentifier', read_only=True)    
    class Meta :
        model = models.privatePerson
        fields = '__all__'
    some_field = serializers.CharField(allow_blank=True, required=False)
    another_field = serializers.IntegerField(required=False, allow_null=True)

class jobInfoSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.jobInfo
        fields = '__all__'
    some_field = serializers.CharField(allow_blank=True, required=False)
    another_field = serializers.IntegerField(required=False, allow_null=True)

class tradingCodesSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.tradingCodes
        fields = '__all__'
    some_field = serializers.CharField(allow_blank=True, required=False)
    another_field = serializers.IntegerField(required=False, allow_null=True)

class financialInfoSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.financialInfo
        fields = '__all__'

    some_field = serializers.CharField(allow_blank=True, required=False)
    another_field = serializers.IntegerField(required=False, allow_null=True)

class legalPersonShareholdersSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.legalPersonShareholders
        fields = '__all__'

    some_field = serializers.CharField(allow_blank=True, required=False)
    another_field = serializers.IntegerField(required=False, allow_null=True)

class legalPersonStakeholdersSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.legalPersonStakeholders
        fields = '__all__'

    some_field = serializers.CharField(allow_blank=True, required=False)
    another_field = serializers.IntegerField(required=False, allow_null=True)

class LegalPersonSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.LegalPerson
        fields = '__all__'

    some_field = serializers.CharField(allow_blank=True, required=False)
    another_field = serializers.IntegerField(required=False, allow_null=True)


class UserLightSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.User
        fields = ['id', 'username', 'first_name', 'last_name' ,'uniqueIdentifier','mobile']


class UserListSerializer(serializers.ModelSerializer):
    private_person = serializers.SerializerMethodField()
    legal_person = serializers.SerializerMethodField()
    legal_person_stakeholders = serializers.SerializerMethodField()
    addresses = serializers.SerializerMethodField()
    accounts = serializers.SerializerMethodField()
    
    class Meta:
        model = models.User
        fields = ['id', 'mobile', 'status', 'type', 'uniqueIdentifier',
                 'private_person', 'legal_person', 'legal_person_stakeholders',
                 'addresses', 'accounts']

    def get_private_person(self, obj):
        if obj.type != 'LEGAL':  # اگر شخص حقیقی بود
            person = obj.privateperson_set.first()
            if person:
                return {
                    'firstName': person.firstName,
                    'lastName': person.lastName,
                    'birthDate': person.birthDate,
                    'gender': person.gender
                }
        return None

    def get_legal_person(self, obj):
        if obj.type == 'LEGAL':  # اگر شخص حقوقی بود
            legal_person = obj.legalperson_set.first()
            if legal_person:
                return {
                    'companyName': legal_person.companyName,
                    'economicCode': legal_person.economicCode,
                    'registerNumber': legal_person.registerNumber,
                    'registerDate': legal_person.registerDate
                }
        return None

    def get_legal_person_stakeholders(self, obj):
        if obj.type == 'LEGAL':  # اگر شخص حقوقی بود
            stakeholders = obj.legalpersonstakeholders_set.all()
            return [{
                'firstName': stake.firstName,
                'lastName': stake.lastName,
                'positionType': stake.positionType,
                'type': stake.type
            } for stake in stakeholders]
        return None

    def get_addresses(self, obj):
        address = obj.addresses_set.first()
        if address:
            return {
                'mobile': address.mobile
            }
        return None

    def get_accounts(self, obj):
        return [{
            'accountNumber': acc.accountNumber,
            'bank': acc.bank,
        } for acc in obj.accounts_set.all()]

