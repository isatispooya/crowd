from rest_framework.views import APIView
from rest_framework.response import Response
from GuardPyCaptcha.Captch import GuardPyCaptcha
from rest_framework import status 
import requests
from .models import User,OneTimeLoginUuid , Otp , Captcha , Admin , accounts ,addresses ,BlacklistedToken, financialInfo , jobInfo , privatePerson ,tradingCodes  , legalPersonShareholders , legalPersonStakeholders , LegalPerson
from . import serializers
import uuid
import datetime
from . import fun
import json
import random
import os
from persiantools.jdatetime import JalaliDate
from utils.message import Message 
from utils.user_notifier import UserNotifier
from plan.views import check_legal_person
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit   
from django.utils.decorators import method_decorator
from django.conf import settings
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class CaptchaViewset(APIView) :
    @method_decorator(ratelimit(**settings.RATE_LIMIT['GET']), name='get')
    def get (self,request):
        captcha = GuardPyCaptcha ()
        captcha = captcha.Captcha_generation(num_char=4 , only_num= True)
        Captcha.objects.create(encrypted_response=captcha['encrypted_response'])
        captcha_obj = Captcha.objects.filter(encrypted_response=captcha['encrypted_response'],enabled=True).first()


        return Response ({'captcha' : captcha} , status = status.HTTP_200_OK)


# otp for user
class OtpViewset(APIView) :
    @method_decorator(ratelimit(**settings.RATE_LIMIT['POST']), name='post')
    def post (self,request) :
        encrypted_response = request.data['encrypted_response'].encode()
        captcha_obj = Captcha.objects.filter(encrypted_response=request.data['encrypted_response'],enabled=True).first()
        if not captcha_obj :
            return Response ({'message' : 'کپچا صحیح نیست'} , status=status.HTTP_400_BAD_REQUEST)
        captcha_obj.delete()
        if isinstance(encrypted_response, str):
            encrypted_response = encrypted_response.encode('utf-8')
        captcha = GuardPyCaptcha()

        captcha = captcha.check_response(encrypted_response, request.data['captcha'])
        if True:#not settings.DEBUG : 
            if not captcha :
                return Response ({'message' : 'کد کپچا صحیح نیست'} , status=status.HTTP_400_BAD_REQUEST)
            if request.data['captcha'] == '' :
                return Response ({'message' : 'کد کپچا خالی است'} , status=status.HTTP_400_BAD_REQUEST)

        uniqueIdentifier = request.data['uniqueIdentifier']
        if not uniqueIdentifier :
            return Response ({'message' : 'کد ملی را وارد کنید'} , status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter (uniqueIdentifier = uniqueIdentifier).first()
        
        if user :
            otp = Otp.objects.filter(mobile=user.mobile).first()
            code = random.randint(10000,99999)


            if not otp:
                otp = Otp(mobile=user.mobile, code=code , expire = timezone.now () + timedelta(minutes=2))
            elif otp.expire > timezone.now() :
                return Response({'error': 'برای ارسال کد مجدد 2 دقیقه منتظر بمانید '}, status=status.HTTP_400_BAD_REQUEST)
            elif otp.expire < timezone.now():
                otp.code = code 
                otp.expire = timezone.now () + timedelta(minutes=2)
            otp.save()
            notifier = UserNotifier(mobile=user.mobile, email=None)
            try:
                address = addresses.objects.filter(user=user).first()
                if address:
                    notifier.email = address.email

                notifier.send_otp_sms(code)

                if notifier.email:
                    try:
                        notifier.send_otp_email(code)  
                    except Exception as e:
                        print(f"Failed to send OTP via email")
            except Exception as e:
                print(f"Error sending notifications")
                notifier.send_otp_sms(code)

           
        
        if not user:
            url = "http://31.40.4.92:8870/otp"
            payload = json.dumps({
            "uniqueIdentifier": uniqueIdentifier
            })
            headers = {
            'X-API-KEY': os.getenv('X-API-KEY'),
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code >=300 :
                return Response ({ 'message' : 'کد تایید ارسال شد'},status=status.HTTP_200_OK)
            return Response ({ 'message' : 'کد تایید ارسال شد'},status=status.HTTP_200_OK)

        return Response ({ 'message' : 'کد تایید ارسال شد'},status=status.HTTP_200_OK)
                
     
class LoginViewset(APIView):
    @method_decorator(ratelimit(**settings.RATE_LIMIT['POST']), name='post')
    def post (self, request) :
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        otp = request.data.get('otp')
        referal = request.data.get('referal','')
        user = None
        if not uniqueIdentifier or not otp:
            return Response({'message': 'کد ملی و کد تأیید الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(uniqueIdentifier=uniqueIdentifier)
            if user.is_locked():
                return Response({'message': 'حساب شما قفل است، لطفاً بعد از مدتی دوباره تلاش کنید.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except  :
            pass
        if user : 
            try:
                mobile = user.mobile
                otp_obj = Otp.objects.filter(mobile=mobile , code = otp ).order_by('-date').first()
                if otp_obj is None:
                    user.attempts += 1  
                    if user.attempts >= 3:
                        user.lock() 
                        return Response({'message': 'تعداد تلاش‌های شما بیش از حد مجاز است. حساب شما برای 5 دقیقه قفل شد.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

                    user.save()  
                    return Response({'message': 'کد تأیید اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)

                if otp_obj.expire and timezone.now() > otp_obj.expire:
                    return Response({'message': 'زمان کد منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'message': 'کد تأیید نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
            user.attempts = 0
            user.save()
            otp_obj.delete()
            token = fun.encryptionUser(user)
            return Response({'access': token}, status=status.HTTP_200_OK)
        url = "http://31.40.4.92:8870/information"
        payload = json.dumps({
        "uniqueIdentifier": uniqueIdentifier,
        "otp": otp
        })
        headers = {
        'X-API-KEY': os.getenv('X-API-KEY'),
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.content)
        try :
            data = response['data']
        except:
            return Response({'message' :'مجددا تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)
        if data == None :
            return Response({'message' :'مجددا تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)
        if not data.get('uniqueIdentifier'):
            return Response({'message' :'مجددا تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)
        if not data.get('mobile'):
            return Response({'message' :'مجددا تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)
        
        new_user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
        try :
            with transaction.atomic():
                if  not new_user :
                    new_user  =User(
                    agent = data.get('agent'),
                    email = data.get('email'),
                    mobile = data.get('mobile'),
                    status = data.get('status'),
                    type = data.get('type'),
                    uniqueIdentifier = data.get('uniqueIdentifier'),
                    referal = referal,
                )
                new_user.save()
                

                try :
                    agent = data.get('agent')
                    if isinstance(agent, dict):
                        new_agent = {
                        'user': new_user,
                        'description': agent.get('description', ''),
                        'expiration_date': agent.get('expirationDate', ''),
                        'first_name': agent.get('firstName', ''),
                        'is_confirmed': agent.get('isConfirmed', ''),
                        'last_name': agent.get('lastName', ''),
                        'type': agent.get('type', ''),
                        'father_uniqueIdentifier': agent.get('uniqueIdentifier', ''),
                    }
                            
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - اطلاعات وکیل')

                try :
                    accounts_data = data.get('accounts',[])
                    print(accounts_data)
                    if accounts_data:
                        for account_data in accounts_data:
                            accountNumber = account_data.get('accountNumber') or ''
                            bank = ''
                            branchCity = ''
                            branchCode = ''
                            branchName = ''
                            isDefault = 'False'
                            modifiedDate = ''
                            type = ''
                            sheba = ''

                            if account_data.get('bank') and isinstance(account_data['bank'], dict):
                                bank = account_data['bank'].get('name', '')
                                
                            if account_data.get('branchCity') and isinstance(account_data['branchCity'], dict):
                                branchCity = account_data['branchCity'].get('name', '')
                                
                            branchCode = account_data.get('branchCode') or ''
                            branchName = account_data.get('branchName') or ''
                            isDefault = account_data.get('isDefault', False)
                            modifiedDate = account_data.get('modifiedDate', '')
                            type = account_data.get('type') or ''
                            sheba = account_data.get('sheba', '')

                            accounts.objects.create(
                                user=new_user,
                                accountNumber=accountNumber,
                                bank=bank,
                                branchCity=branchCity,
                                branchCode=branchCode,
                                branchName=branchName,
                                isDefault=isDefault,
                                modifiedDate=modifiedDate,
                                type=type,
                                sheba=sheba
                            )
                except :
                    raise Exception('خطا در ثبت اطلاعات اصلی کاربر - حساب ها')

                
                try :
                    jobInfo_data = data.get('jobInfo')
                    if isinstance(jobInfo_data, dict):
                        jobInfo.objects.create(
                            user=new_user,
                            companyAddress=jobInfo_data.get('companyAddress', ''),
                            companyCityPrefix=jobInfo_data.get('companyCityPrefix', ''),
                            companyEmail=jobInfo_data.get('companyEmail', ''),
                            companyFax=jobInfo_data.get('companyFax', ''),
                            companyFaxPrefix=jobInfo_data.get('companyFaxPrefix', ''),
                            companyName=jobInfo_data.get('companyName', ''),
                            companyPhone=jobInfo_data.get('companyPhone', ''),
                            companyPostalCode=jobInfo_data.get('companyPostalCode', ''),
                            companyWebSite=jobInfo_data.get('companyWebSite', ''),
                            employmentDate=jobInfo_data.get('employmentDate', ''),
                            job=jobInfo_data.get('job', {}).get('title', ''),
                            jobDescription=jobInfo_data.get('jobDescription', ''),
                            position=jobInfo_data.get('position', ''),
                        )
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شغلی')

                try :
                    privatePerson_data = data.get('privatePerson',{})
                    if isinstance(privatePerson_data, dict):
                        birthDate = ''
                        fatherName = ''
                        firstName = ''
                        gender = ''
                        lastName = ''
                        placeOfBirth = ''
                        placeOfIssue = ''
                        seriSh = ''
                        serial = ''
                        shNumber = ''
                        signatureFile = None


                        birthDate = privatePerson_data.get('birthDate', '') or ''
                        fatherName = privatePerson_data.get('fatherName', '') or ''
                        firstName = privatePerson_data.get('firstName', '') or ''
                        gender = privatePerson_data.get('gender', '') or ''
                        lastName = privatePerson_data.get('lastName', '') or ''
                        placeOfBirth = privatePerson_data.get('placeOfBirth', '') or ''
                        placeOfIssue = privatePerson_data.get('placeOfIssue', '') or ''
                        seriSh = privatePerson_data.get('seriSh', '') or ''
                        serial = privatePerson_data.get('serial', '') or ''
                        shNumber = privatePerson_data.get('shNumber', '') or ''
                        signatureFile = privatePerson_data.get('signatureFile', None)

                        privatePerson.objects.create(
                            user=new_user,
                            birthDate=birthDate,
                            fatherName=fatherName,
                            firstName=firstName,
                            gender=gender,
                            lastName=lastName,
                            placeOfBirth=placeOfBirth,
                            placeOfIssue=placeOfIssue,
                            seriSh=seriSh,
                            serial=serial,
                            shNumber=shNumber,
                            signatureFile=signatureFile
                        )
                except :
                    raise Exception('خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شخص حقیقی')

                try :
                    trading_codes = data.get('tradingCodes', [])
                    print(trading_codes)
                    if trading_codes:
                        for tradingCodes_data in trading_codes:
                            code = tradingCodes_data.get('code')
                            if not code:
                                raise Exception('خطا در ثبت اطلاعات اصلی کاربر - کد های بورسی')

                            firstPart = ''
                            secondPart = ''
                            thirdPart = ''
                            type = ''

                            firstPart = tradingCodes_data.get('firstPart', '') or ''
                            secondPart = tradingCodes_data.get('secondPart', '') or ''
                            thirdPart = tradingCodes_data.get('thirdPart', '') or ''
                            type = tradingCodes_data.get('type', '') or ''


                                
                            tradingCodes.objects.create(
                                user = new_user,
                                code = code,
                                firstPart = firstPart,
                                secondPart = secondPart,
                                thirdPart = thirdPart,
                                type = type,
                            )
                except :
                    raise Exception ('خطا در ثبت اطلاعات اصلی کاربر - کد های بورسی')

                try :
                    financialInfo_data = data.get('financialInfo')
                    if isinstance(financialInfo_data, dict):
                        assetsValue = financialInfo_data.get('assetsValue', '')
                        cExchangeTransaction = financialInfo_data.get('cExchangeTransaction', '')
                        companyPurpose = financialInfo_data.get('companyPurpose', '')
                        try:
                            financialBrokers = ', '.join([broker.get('broker', {}).get('title', '') for broker in financialInfo_data.get('financialBrokers', [])])
                        except:
                            financialBrokers = ''
                        inComingAverage = financialInfo_data.get('inComingAverage', '')
                        outExchangeTransaction = financialInfo_data.get('outExchangeTransaction', '')
                        rate = financialInfo_data.get('rate', '')
                        rateDate = financialInfo_data.get('rateDate', '')
                        referenceRateCompany = financialInfo_data.get('referenceRateCompany', '')
                        sExchangeTransaction = financialInfo_data.get('sExchangeTransaction', '')
                        tradingKnowledgeLevel = financialInfo_data.get('tradingKnowledgeLevel', None)
                        transactionLevel = financialInfo_data.get('transactionLevel', None)

                        financialInfo.objects.create(
                            user=new_user,
                            assetsValue=assetsValue,
                            cExchangeTransaction=cExchangeTransaction,
                            companyPurpose=companyPurpose,
                            financialBrokers=financialBrokers,
                            inComingAverage=inComingAverage,
                            outExchangeTransaction=outExchangeTransaction,
                            rate=rate,
                            rateDate=rateDate,
                            referenceRateCompany=referenceRateCompany,
                            sExchangeTransaction=sExchangeTransaction,
                            tradingKnowledgeLevel=tradingKnowledgeLevel,
                            transactionLevel=transactionLevel,
                        )
                except:
                    print('خطا در ثبت اطلاعات اصلی کاربر - پرسش های مالی')

                try :   
                    address = data.get('addresses',[])
                    for addresses_data in address:
                        alley = ''
                        city = ''
                        cityPrefix = ''
                        country = ''
                        countryPrefix = ''
                        email = ''
                        emergencyTel = ''
                        emergencyTelCityPrefix = ''
                        emergencyTelCountryPrefix = ''
                        fax = ''
                        faxPrefix = ''
                        mobile = ''
                        plaque = ''
                        postalCode = ''
                        province = ''
                        remnantAddress = ''
                        section = ''
                        tel = ''
                        website = ''
                        alley = addresses_data.get('alley', '') or ''
                        if addresses_data.get('city') and isinstance(addresses_data['city'], dict):
                            city = addresses_data['city'].get('name', '')
                        cityPrefix = addresses_data.get('cityPrefix', '') or ''
                        if addresses_data.get('country') and isinstance(addresses_data['country'], dict):
                            country = addresses_data['country'].get('name', '')
                        countryPrefix = addresses_data.get('countryPrefix', '') or ''
                        email = addresses_data.get('email', '') or ''
                        emergencyTel = addresses_data.get('emergencyTel', '') or ''
                        emergencyTelCityPrefix = addresses_data.get('emergencyTelCityPrefix', '') or ''
                        emergencyTelCountryPrefix = addresses_data.get('emergencyTelCountryPrefix', '') or ''
                        fax = addresses_data.get('fax', '') or ''
                        faxPrefix = addresses_data.get('faxPrefix', '') or ''
                        mobile = addresses_data.get('mobile', '') or ''
                        plaque = addresses_data.get('plaque', '') or ''
                        postalCode = addresses_data.get('postalCode', '') or ''
                        province = addresses_data.get('province', {}).get('name', '') or ''
                        remnantAddress = addresses_data.get('remnantAddress', '') or ''
                        section = addresses_data.get('section', {}).get('name', '') or ''
                        tel = addresses_data.get('tel', '') or ''
                        website = addresses_data.get('website', '') or ''
                        addresses.objects.create(
                            user = new_user,
                            alley = alley,
                            city = city,
                            cityPrefix = cityPrefix,
                            country = country,
                            countryPrefix = countryPrefix,
                            email = email,
                            emergencyTel = emergencyTel,
                            emergencyTelCityPrefix = emergencyTelCityPrefix,
                            emergencyTelCountryPrefix = emergencyTelCountryPrefix,
                            fax = fax,
                            faxPrefix = faxPrefix,
                            mobile = mobile,
                            plaque = plaque,
                            postalCode = postalCode,
                            province = province,
                            remnantAddress = remnantAddress,
                            section = section,
                            tel = tel,
                            website = website,
                            )
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - آدرس ها')

                try :
                    if len(data.get('legalPersonStakeholders', [])) > 0:
                        for stakeholder_data in data['legalPersonStakeholders']:
                            legalPersonStakeholders.objects.create(
                                user=new_user,
                                uniqueIdentifier=stakeholder_data.get('uniqueIdentifier', ''),
                                type=stakeholder_data.get('type', ''),
                                startAt=stakeholder_data.get('startAt', ''),
                                positionType=stakeholder_data.get('positionType', ''),
                                lastName=stakeholder_data.get('lastName', ''),
                            isOwnerSignature=stakeholder_data.get('isOwnerSignature', False),
                            firstName=stakeholder_data.get('firstName', ''),
                                endAt=stakeholder_data.get('endAt', '')
                            )
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - هیئت مدیره')


                try :   
                    legal_person_data = data.get('legalPerson', {})
                    if legal_person_data:
                        LegalPerson.objects.create(
                            user=new_user,
                            citizenshipCountry=legal_person_data.get('citizenshipCountry', ''),
                            companyName=legal_person_data.get('companyName', ''),
                            economicCode=legal_person_data.get('economicCode', ''),
                            evidenceExpirationDate=legal_person_data.get('evidenceExpirationDate', ''),
                            evidenceReleaseCompany=legal_person_data.get('evidenceReleaseCompany', ''),
                            evidenceReleaseDate=legal_person_data.get('evidenceReleaseDate', ''),
                            legalPersonTypeSubCategory=legal_person_data.get('legalPersonTypeSubCategory', ''),
                            registerDate=legal_person_data.get('registerDate', ''),
                            legalPersonTypeCategory=legal_person_data.get('legalPersonTypeCategory', ''),
                            registerPlace=legal_person_data.get('registerPlace', ''),
                            registerNumber=legal_person_data.get('registerNumber', '')
                        )
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شرکت')


                try :   
                    if data.get('legalPersonShareholders'):
                        for legalPersonShareholders_data in data['legalPersonShareholders']:
                            legalPersonShareholders.objects.create(
                                user = new_user,
                                uniqueIdentifier = legalPersonShareholders_data.get('uniqueIdentifier', ''),
                                postalCode = legalPersonShareholders_data.get('postalCode', ''),
                                positionType = legalPersonShareholders_data.get('positionType', ''),
                                percentageVotingRight = legalPersonShareholders_data.get('percentageVotingRight', ''),
                                firstName = legalPersonShareholders_data.get('firstName', ''),
                                lastName = legalPersonShareholders_data.get('lastName', ''),
                                address = legalPersonShareholders_data.get('address', '')
                            )
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - سهامداران')
                        
        except Exception as e:
            print(e)
            return Response({'message': 'خطایی نامشخص رخ داده است'}, status=status.HTTP_400_BAD_REQUEST)

        token = fun.encryptionUser(new_user)

        return Response({'message': True , 'access' :token} , status=status.HTTP_200_OK)


# done
class InformationViewset (APIView) :
    @method_decorator(ratelimit(**settings.RATE_LIMIT['GET']), name='get')
    def get (self,request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_401_UNAUTHORIZED)
        user = user.first()   
        user = User.objects.filter(id=user.id).first() if user else None
        
        if not user:
            return Response({'error': 'User not found in database'}, status=status.HTTP_404_NOT_FOUND)
        serializer_user = serializers.UserSerializer(user).data
        user_accounts = accounts.objects.filter(user=user)
        serializer_accounts = serializers.accountsSerializer(user_accounts , many = True).data
        user_addresses = addresses.objects.filter(user=user)
        serializer_addresses = serializers.addressesSerializer(user_addresses , many = True).data
        user_privatePerson = privatePerson.objects.filter(user=user)
        serializer_privatePerson = serializers.privatePersonSerializer(user_privatePerson , many = True).data
        user_financialInfo = financialInfo.objects.filter(user=user)
        serializer_financialInfo = serializers.financialInfoSerializer(user_financialInfo , many = True).data
        user_jobInfo = jobInfo.objects.filter(user=user)
        serializer_jobInfo = serializers.jobInfoSerializer(user_jobInfo , many = True).data
        user_tradingCodes = tradingCodes.objects.filter(user=user)
        serializer_tradingCodes = serializers.tradingCodesSerializer(user_tradingCodes , many = True).data
        user_legalPersonStakeholders = legalPersonStakeholders.objects.filter(user=user)
        serializer_legalPersonStakeholders = serializers.legalPersonStakeholdersSerializer(user_legalPersonStakeholders , many = True).data
        user_LegalPerson = LegalPerson.objects.filter(user=user)
        serializer_LegalPerson = serializers.legalPersonStakeholdersSerializer(user_LegalPerson , many = True).data
        user_legalPersonShareholders = legalPersonShareholders.objects.filter(user=user)
        serializer_legalPersonShareholders = serializers.legalPersonStakeholdersSerializer(user_legalPersonShareholders , many = True).data
        combined_data = {
            **serializer_user,  
            'accounts': serializer_accounts,   
            'addresses': serializer_addresses,  
            'private_person': serializer_privatePerson,  
            'financial_info': serializer_financialInfo,  
            'job_info': serializer_jobInfo,    
            'trading_codes': serializer_tradingCodes,     
            'legalPersonStakeholders': serializer_legalPersonStakeholders,     
            'LegalPerson': serializer_LegalPerson,     
            'legalPersonShareholders': serializer_legalPersonShareholders,     
        }
        return Response({'received_data': True ,  'acc' : combined_data})
    

#otp for admin
# done
class OtpAdminViewset(APIView) :
    @method_decorator(ratelimit(**settings.RATE_LIMIT['POST']), name='post')
    def post (self,request) :
        captcha = GuardPyCaptcha()
        encrypted_response = request.data['encrypted_response']
        captcha_obj = Captcha.objects.filter(encrypted_response=encrypted_response,enabled=True).first()
        if not captcha_obj :
            return Response ({'message' : 'کپچا صحیح نیست'} , status=status.HTTP_400_BAD_REQUEST)
        captcha_obj.delete()
        if isinstance(encrypted_response, str):
            encrypted_response = encrypted_response.encode('utf-8')
        captcha = captcha.check_response(encrypted_response , request.data['captcha'])
        if not settings.DEBUG : 
            if not captcha :
                return Response ({'message' : 'کد کپچا صحیح نیست'} , status=status.HTTP_400_BAD_REQUEST)
            if request.data['captcha'] == '' :
                return Response ({'message' : 'کد کپچا خالی است'} , status=status.HTTP_400_BAD_REQUEST)
        uniqueIdentifier = request.data['uniqueIdentifier']
        if not uniqueIdentifier :
            return Response ({'message' : 'کد ملی را وارد کنید'} , status=status.HTTP_400_BAD_REQUEST)
        admin = Admin.objects.filter(uniqueIdentifier = uniqueIdentifier).first()
        if admin :
            otp = Otp.objects.filter(mobile=admin.mobile).first()
            code = random.randint(10000,99999)

            if not otp:
                otp = Otp(mobile=admin.mobile, code=code , expire = timezone.now () + timedelta(minutes=2))
            elif otp.expire > timezone.now() :
                return Response({'error': 'برای ارسال کد مجدد 2 دقیقه منتظر بمانید '}, status=status.HTTP_400_BAD_REQUEST)
            elif otp.expire < timezone.now():
                otp.code = code 
                otp.expire = timezone.now () + timedelta(minutes=2)
            otp.save()
            notifier = UserNotifier(mobile=admin.mobile, email=admin.email)
            notifier.send_otp_sms(code)  

            try:
                notifier.send_otp_email(code) 
            except Exception as e:
                print(f'Error sending otp email: {e}')
            
            return Response({'message': 'کد تایید ارسال شد'}, status=status.HTTP_200_OK)

        return Response({'message': 'کد تایید ارسال شد'}, status=status.HTTP_200_OK)


# login for admin
# done
class LoginAdminViewset(APIView) :
    @method_decorator(ratelimit(**settings.RATE_LIMIT['POST']), name='post')
    def post (self,request) :
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        code = request.data.get('code')
        if not uniqueIdentifier or not code:
            return Response({'message': 'کد ملی و کد تأیید الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(uniqueIdentifier=uniqueIdentifier)
            if admin.is_locked():
                return Response({'message': 'حساب شما قفل است، لطفاً بعد از مدتی دوباره تلاش کنید.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except:
            return Response({'message': ' کد ملی  موجود نیست لطفا ثبت نام کنید'}, status=status.HTTP_404_NOT_FOUND)
        try:
            mobile = admin.mobile
            otp_obj = Otp.objects.filter(mobile=mobile , code = code ).order_by('-date').first()
            if otp_obj is None:
                admin.attempts += 1  
                if admin.attempts >= 3:
                    admin.lock() 
                    return Response({'message': 'تعداد تلاش‌های شما بیش از حد مجاز است. حساب شما برای 5 دقیقه قفل شد.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

                admin.save()  
                return Response({'message': 'کد تأیید اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
            if otp_obj.expire and timezone.now() > otp_obj.expire:
                return Response({'message': 'زمان کد منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': 'کد تأیید نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
        admin.attempts = 0
        admin.save()
        otp_obj.delete()
        token = fun.encryptionadmin(admin)
        return Response({'access': token}, status=status.HTTP_200_OK)


class RefreshTokenAdminViewset(APIView):
    @method_decorator(ratelimit(**settings.RATE_LIMIT['POST']), name='post')
    def post(self, request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_401_UNAUTHORIZED)
        admin = admin.first()
        token = fun.encryptionadmin(admin)
        return Response({'access': token}, status=status.HTTP_200_OK)


# done
class UserListViewset(APIView):

    @method_decorator(ratelimit(**settings.RATE_LIMIT['GET']), name='get')
    def get(self, request):
        Authorization = request.headers.get('Authorization')    
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        admin = admin.first()

        # اضافه کردن prefetch برای مدل‌های حقوقی
        users = User.objects.prefetch_related(
            'privateperson_set',
            'legalperson_set',
            'legalpersonstakeholders_set',
            'addresses_set',
            'accounts_set',
        ).all()

        serializer = serializers.UserListSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



# done
class UserOneViewset(APIView) :
    @method_decorator(ratelimit(**settings.RATE_LIMIT['GET']), name='get')
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')    
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_401_UNAUTHORIZED)
        admin = admin.first()
        user = User.objects.filter(id=id).first()
        if not user :
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user_serializer = serializers.UserSerializer(user).data
        privateperson = privatePerson.objects.filter(user=user)
        privateperson_serializer = serializers.privatePersonSerializer(privateperson, many=True).data

        user_addresses = addresses.objects.filter(user=user)
        serializer_addresses = serializers.addressesSerializer(user_addresses, many=True).data

        user_financialInfo = financialInfo.objects.filter(user=user)
        serializer_financialInfo = serializers.financialInfoSerializer(user_financialInfo, many=True).data

        user_jobInfo = jobInfo.objects.filter(user=user)
        serializer_jobInfo = serializers.jobInfoSerializer(user_jobInfo, many=True).data

        user_tradingCodes = tradingCodes.objects.filter(user=user)
        serializer_tradingCodes = serializers.tradingCodesSerializer(user_tradingCodes, many=True).data

        user_accounts = accounts.objects.filter(user=user)
        serializer_accounts = serializers.accountsSerializer(user_accounts, many=True).data
        legal_person_data = {}
        if check_legal_person(user.uniqueIdentifier):
            legal_person_data = {
                'legal_person_shareholder': serializers.legalPersonShareholdersSerializer(
                    legalPersonShareholders.objects.filter(user=user), many=True
                ).data,
                'legal_person': serializers.LegalPersonSerializer(
                    LegalPerson.objects.filter(user=user), many=True
                ).data,
                'legal_person_stakeholders': serializers.legalPersonStakeholdersSerializer(
                    legalPersonStakeholders.objects.filter(user=user), many=True
                ).data,
            }
        combined_data = {
            **user_serializer, 
            'addresses': serializer_addresses,
            'private_person': privateperson_serializer,
            'financial_info': serializer_financialInfo,
            'job_info': serializer_jobInfo,
            'trading_codes': serializer_tradingCodes,
            'accounts': serializer_accounts,
            **legal_person_data,
        }

        return Response({'success': combined_data}, status=status.HTTP_200_OK)


# done
class OtpUpdateViewset(APIView) :
    @method_decorator(ratelimit(**settings.RATE_LIMIT['POST']), name='post')
    def post (self,request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_401_UNAUTHORIZED)
        admin = admin.first()
        uniqueIdentifier = request.data.get("uniqueIdentifier")
        if not uniqueIdentifier :
            return Response ({'errot' : 'کاربر یافت نشد '} ,  status=status.HTTP_400_BAD_REQUEST) 
        url = "http://31.40.4.92:8870/otp"
        payload = json.dumps({
        "uniqueIdentifier": uniqueIdentifier
        })
        headers = {
        'X-API-KEY': os.getenv('X-API-KEY'),
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code >=300 :
            return Response ({'message' :'ارسال از طریق سجام امکان پذیر نیست '} , status=status.HTTP_400_BAD_REQUEST)
        return Response ({'message' : 'کد تایید از طریق سامانه سجام ارسال شد'},status=status.HTTP_200_OK)
            

# done
class UpdateInformationViewset(APIView):
    @method_decorator(ratelimit(**settings.RATE_LIMIT['PATCH']), name='patch')
    def patch(self, request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_401_UNAUTHORIZED)
        
        admin = admin.first()
        
        otp = request.data.get('otp')
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        if not otp:
            return Response({'error': 'otp not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # API call and data validation
        url = "http://31.40.4.92:8870/information"
        payload = json.dumps({
            "uniqueIdentifier": uniqueIdentifier,
            "otp": otp
        })
        headers = {
            'X-API-KEY': os.getenv('X-API-KEY'),
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.content)
        try:
            data = response['data']
        except:
            return Response({'message': 'دوباره تلاش کن'}, status=status.HTTP_400_BAD_REQUEST)
        
        if data is None:
            return Response({'message': 'بیشتر تلاش کن'}, status=status.HTTP_400_BAD_REQUEST)
        new_user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
        print(new_user)
        
        if new_user:
            new_user.agent = data.get('agent', new_user.agent)
            new_user.email = data.get('email', new_user.email)
            new_user.mobile = data.get('mobile', new_user.mobile)
            new_user.status = data.get('status', new_user.status)
            new_user.type = data.get('type', new_user.type)
            new_user.save()

            if accounts.objects.filter(user=new_user).first():
                accounts.objects.filter(user=new_user).delete()
            try:
                accounts_data = data.get('accounts',[])
                
                if accounts_data:
                    for account_data in accounts_data:
                        accountNumber = account_data.get('accountNumber') or ''
                        bank = ''
                        branchCity = ''
                        branchCode = ''
                        branchName = ''
                        isDefault = 'False'
                        modifiedDate = ''
                        type = ''
                        sheba = ''
                        accountNumber = account_data.get('accountNumber') or ''
                        if account_data.get('bank') and isinstance(account_data['bank'], dict):
                            bank = account_data['bank'].get('name', '')
                            
                        if account_data.get('branchCity') and isinstance(account_data['branchCity'], dict):
                            branchCity = account_data['branchCity'].get('name', '')
                            
                        branchCode = account_data.get('branchCode') or ''
                        branchName = account_data.get('branchName') or ''
                        isDefault = account_data.get('isDefault', False)
                        modifiedDate = account_data.get('modifiedDate', '')
                        type = account_data.get('type') or ''
                        sheba = account_data.get('sheba', '')
                        accounts.objects.create(
                            user=new_user,
                            accountNumber=accountNumber,
                            bank=bank,
                            branchCity=branchCity,
                            branchCode=branchCode, 
                            branchName=branchName,
                            isDefault=isDefault,
                            modifiedDate=modifiedDate,
                            type=type,
                            sheba=sheba
                        )
            except :
                raise Exception('خطا در ثبت اطلاعات اصلی کاربر - حساب ها')
            
            if addresses.objects.filter(user=new_user).first():
                addresses.objects.filter(user=new_user).delete()
            try:
                address = data.get('addresses',[])
                for addresses_data in address:
                    alley = ''
                    city = ''
                    cityPrefix = ''
                    country = ''
                    countryPrefix = ''
                    email = ''
                    emergencyTel = ''
                    emergencyTelCityPrefix = ''
                    emergencyTelCountryPrefix = ''
                    fax = ''
                    faxPrefix = ''
                    mobile = ''
                    plaque = ''
                    postalCode = ''
                    province = ''
                    remnantAddress = ''
                    section = ''
                    tel = ''
                    website = ''
                    alley = addresses_data.get('alley', '') or ''
                    if addresses_data.get('city') and isinstance(addresses_data['city'], dict):
                        city = addresses_data['city'].get('name', '')
                    cityPrefix = addresses_data.get('cityPrefix', '') or ''
                    if addresses_data.get('country') and isinstance(addresses_data['country'], dict):
                        country = addresses_data['country'].get('name', '')
                    countryPrefix = addresses_data.get('countryPrefix', '') or ''
                    email = addresses_data.get('email', '') or ''
                    emergencyTel = addresses_data.get('emergencyTel', '') or ''
                    emergencyTelCityPrefix = addresses_data.get('emergencyTelCityPrefix', '') or ''
                    emergencyTelCountryPrefix = addresses_data.get('emergencyTelCountryPrefix', '') or ''
                    fax = addresses_data.get('fax', '') or ''
                    faxPrefix = addresses_data.get('faxPrefix', '') or ''
                    mobile = addresses_data.get('mobile', '') or ''
                    plaque = addresses_data.get('plaque', '') or ''
                    postalCode = addresses_data.get('postalCode', '') or ''
                    province = addresses_data.get('province', {}).get('name', '') or ''
                    remnantAddress = addresses_data.get('remnantAddress', '') or ''
                    section = addresses_data.get('section', {}).get('name', '') or ''
                    tel = addresses_data.get('tel', '') or ''
                    website = addresses_data.get('website', '') or ''
                        
                    addresses.objects.create(
                            user = new_user,
                            alley = alley,
                            city = city,
                            cityPrefix = cityPrefix,
                            country = country,
                            countryPrefix = countryPrefix,
                            email = email,
                            emergencyTel = emergencyTel,
                            emergencyTelCityPrefix = emergencyTelCityPrefix,
                            emergencyTelCountryPrefix = emergencyTelCountryPrefix,
                            fax = fax,
                            faxPrefix = faxPrefix,
                            mobile = mobile,
                            plaque = plaque,
                            postalCode = postalCode,
                            province = province,
                            remnantAddress = remnantAddress,
                            section = section,
                            tel = tel,
                            website = website,
                            )
            except :
                print('خطا در ثبت اطلاعات آدرس ها')

            try :
                jobInfo_data = data.get('jobInfo')
                if isinstance(jobInfo_data, dict):
                    if jobInfo.objects.filter(user=new_user).first():
                        jobInfo.objects.filter(user=new_user).delete()
                    jobInfo.objects.create(
                        user=new_user,
                        companyAddress=jobInfo_data.get('companyAddress', ''),
                        companyCityPrefix=jobInfo_data.get('companyCityPrefix', ''),
                        companyEmail=jobInfo_data.get('companyEmail', ''),
                        companyFax=jobInfo_data.get('companyFax', ''),
                        companyFaxPrefix=jobInfo_data.get('companyFaxPrefix', ''),
                        companyName=jobInfo_data.get('companyName', ''),
                        companyPhone=jobInfo_data.get('companyPhone', ''),
                        companyPostalCode=jobInfo_data.get('companyPostalCode', ''),
                        companyWebSite=jobInfo_data.get('companyWebSite', ''),
                        employmentDate=jobInfo_data.get('employmentDate', ''),
                        job=jobInfo_data.get('job', {}).get('title', ''),
                        jobDescription=jobInfo_data.get('jobDescription', ''),
                        position=jobInfo_data.get('position', ''),
                    )
            except :
                print('خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شغلی')

            try :
                privatePerson_data = data.get('privatePerson')
                if isinstance(privatePerson_data, dict):
                    birthDate = ''
                    fatherName = ''
                    firstName = ''
                    gender = ''
                    lastName = ''
                    placeOfBirth = ''
                    placeOfIssue = ''
                    seriSh = ''
                    serial = ''
                    shNumber = ''
                    signatureFile = None


                    birthDate = privatePerson_data.get('birthDate', '') or ''
                    fatherName = privatePerson_data.get('fatherName', '') or ''
                    firstName = privatePerson_data.get('firstName', '') or ''
                    gender = privatePerson_data.get('gender', '') or ''
                    lastName = privatePerson_data.get('lastName', '') or ''
                    placeOfBirth = privatePerson_data.get('placeOfBirth', '') or ''
                    placeOfIssue = privatePerson_data.get('placeOfIssue', '') or ''
                    seriSh = privatePerson_data.get('seriSh', '') or ''
                    serial = privatePerson_data.get('serial', '') or ''
                    shNumber = privatePerson_data.get('shNumber', '') or ''
                    signatureFile = privatePerson_data.get('signatureFile', None)
                    if privatePerson.objects.filter(user=new_user).first():
                        privatePerson.objects.filter(user=new_user).delete()

                    privatePerson.objects.create(
                        user=new_user,
                        birthDate=birthDate,
                        fatherName=fatherName,
                        firstName=firstName,
                        gender=gender,
                        lastName=lastName,
                        placeOfBirth=placeOfBirth,
                        placeOfIssue=placeOfIssue,
                        seriSh=seriSh,
                        serial=serial,
                        shNumber=shNumber,
                        signatureFile=signatureFile
                    )
            except :
                raise Exception('خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شخص حقیقی')

            try : 
                financialInfo_data = data.get('financialInfo')
                if isinstance(financialInfo_data, dict):
                    assetsValue = financialInfo_data.get('assetsValue', '')
                    cExchangeTransaction = financialInfo_data.get('cExchangeTransaction', '')
                    companyPurpose = financialInfo_data.get('companyPurpose', '')
                    try:
                        financialBrokers = ', '.join([broker.get('broker', {}).get('title', '') for broker in financialInfo_data.get('financialBrokers', [])])
                    except:
                        financialBrokers = ''
                    inComingAverage = financialInfo_data.get('inComingAverage', '')
                    outExchangeTransaction = financialInfo_data.get('outExchangeTransaction', '')
                    rate = financialInfo_data.get('rate', '')
                    rateDate = financialInfo_data.get('rateDate', '')
                    referenceRateCompany = financialInfo_data.get('referenceRateCompany', '')
                    sExchangeTransaction = financialInfo_data.get('sExchangeTransaction', '')
                    tradingKnowledgeLevel = financialInfo_data.get('tradingKnowledgeLevel', None)
                    transactionLevel = financialInfo_data.get('transactionLevel', None)
                    if financialInfo.objects.filter(user=new_user).first():
                        financialInfo.objects.filter(user=new_user).delete()
                    financialInfo.objects.create(
                        user=new_user,
                        assetsValue=assetsValue,
                        cExchangeTransaction=cExchangeTransaction,
                        companyPurpose=companyPurpose,
                        financialBrokers=financialBrokers,
                        inComingAverage=inComingAverage,
                        outExchangeTransaction=outExchangeTransaction,
                        rate=rate,
                        rateDate=rateDate,
                        referenceRateCompany=referenceRateCompany,
                        sExchangeTransaction=sExchangeTransaction,
                        tradingKnowledgeLevel=tradingKnowledgeLevel,
                        transactionLevel=transactionLevel,
                    )
            except :
                print('خطا در ثبت اطلاعات اصلی کاربر - پرسش های مالی')


            try:
                if len(data.get('legalPersonStakeholders', [])) > 0:
                    for stakeholder_data in data['legalPersonStakeholders']:
                        legalPersonStakeholders.objects.update_or_create(
                            user=new_user,  
                            uniqueIdentifier=stakeholder_data.get('uniqueIdentifier', ''),
                            defaults={
                            'type':stakeholder_data.get('type', ''),
                            'startAt':stakeholder_data.get('startAt', ''),
                            'positionType':stakeholder_data.get('positionType', ''),
                            'lastName':stakeholder_data.get('lastName', ''),
                            'isOwnerSignature':stakeholder_data.get('isOwnerSignature', False),
                            'firstName':stakeholder_data.get('firstName', ''),
                            'endAt':stakeholder_data.get('endAt', '')
                        }
                    )
            except:
                print('خطا در ثبت اطلاعات اصلی کاربر - هیئت مدیره')

            try :
                legal_person_data = data.get('legalPerson', {})
                if legal_person_data:
                    LegalPerson.objects.update_or_create(
                        user=new_user,
                        defaults={
                        'citizenshipCountry':legal_person_data.get('citizenshipCountry', ''),
                        'companyName':legal_person_data.get('companyName', ''),
                        'economicCode':legal_person_data.get('economicCode', ''),
                        'evidenceExpirationDate':legal_person_data.get('evidenceExpirationDate', ''),
                        'evidenceReleaseCompany':legal_person_data.get('evidenceReleaseCompany', ''),
                        'evidenceReleaseDate':legal_person_data.get('evidenceReleaseDate', ''),
                        'legalPersonTypeSubCategory':legal_person_data.get('legalPersonTypeSubCategory', ''),
                        'registerDate':legal_person_data.get('registerDate', ''),
                        'legalPersonTypeCategory':legal_person_data.get('legalPersonTypeCategory', ''),
                        'registerPlace':legal_person_data.get('registerPlace', ''),
                        'registerNumber':legal_person_data.get('registerNumber', '')
                        }
                    )
            except :
                print('خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شرکت')
            try :
                if data.get('legalPersonShareholders'):
                    for legalPersonShareholders_data in data['legalPersonShareholders']:
                        legalPersonShareholders.objects.update_or_create(
                            user = new_user,
                            uniqueIdentifier = legalPersonShareholders_data.get('uniqueIdentifier', ''),
                            defaults={
                            'postalCode':legalPersonShareholders_data.get('postalCode', ''),
                            'positionType':legalPersonShareholders_data.get('positionType', ''),
                            'percentageVotingRight':legalPersonShareholders_data.get('percentageVotingRight', ''),
                            'firstName':legalPersonShareholders_data.get('firstName', ''),
                            'lastName':legalPersonShareholders_data.get('lastName', ''),
                            'address':legalPersonShareholders_data.get('address', '')
                        }
                    )
            except :
                print('خطا در ثبت اطلاعات اصلی کاربر - سهامداران')

        return Response({'success': True}, status=status.HTTP_200_OK)
    

class AddBoursCodeUserViewset(APIView):
    @method_decorator(ratelimit(**settings.RATE_LIMIT['POST']), name='post')
    def post (self, request) :
        Authorization = request.headers.get('Authorization')    
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_401_UNAUTHORIZED)
        user = user.first()
        legal = check_legal_person(user.uniqueIdentifier)
        if legal == True :
            bours_code = request.data.get('bours_code')
            if tradingCodes.objects.filter(user=user, code = bours_code).exists():
                return Response({'message': 'Bours code already exists'}, status=status.HTTP_200_OK)
            else:
                trading_code = tradingCodes.objects.create(user=user,code = bours_code)
                serializer = serializers.tradingCodesSerializer(trading_code)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Not a legal person'}, status=status.HTTP_200_OK)
    

class LogoutViewset(APIView):
    @method_decorator(ratelimit(**settings.RATE_LIMIT['POST']), name='post')
    def post(self, request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = Authorization.split('Bearer ')[1]
        except:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        black_list = BlacklistedToken.objects.create(token=token)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_201_CREATED)
    





class OneTimeLoginViewset(APIView):
    @method_decorator(ratelimit(**settings.RATE_LIMIT['POST']), name='post')
    def post(self, request):
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        x_key_api = request.headers.get('x-key-api')
        Authorization = request.headers.get('Authorization')

        if not uniqueIdentifier:
            return Response(
                {'error': 'شناسه کاربر الزامی است'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        is_admin = Authorization and fun.decryptionadmin(Authorization)
        if not (x_key_api == 'dj2n9#mK8$pL5@qR7vX4yH1wB9cF3tE6' or is_admin):
            return Response(
                {'error': 'مجوز دسترسی نامعتبر است'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        with transaction.atomic():
            # حذف UUIDهای منقضی شده
            OneTimeLoginUuid.objects.filter(
                user__uniqueIdentifier=uniqueIdentifier,
                created_at__lt=timezone.now() - timedelta(minutes=10)
            ).delete()

            # بررسی تعداد UUIDهای فعال
            active_uuids = OneTimeLoginUuid.objects.filter(
                user__uniqueIdentifier=uniqueIdentifier,
                status=True,
                created_at__gt=timezone.now() - timedelta(minutes=10)
            )

            if active_uuids.count() >= 3:
                return Response(
                    {'error': 'تعداد درخواست‌های ورود بیش از حد مجاز است'}, 
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            # دریافت کاربر
            user = User.objects.filter(
                uniqueIdentifier=uniqueIdentifier,
            ).first()

            if not user:
                return Response(
                    {'error': 'کاربر یافت نشد یا غیرفعال است'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # ایجاد UUID جدید
            login_uuid = OneTimeLoginUuid.objects.create(
                uuid=str(uuid.uuid4()),
                user=user
            )

            return Response({
                'uuid': login_uuid.uuid,
                'expires_in': '10 minutes'
            }, status=status.HTTP_200_OK)


    @method_decorator(ratelimit(**settings.RATE_LIMIT['GET']), name='get')
    def get(self, request, uuid):
        try:
            # بررسی اعتبار UUID
            uuid_obj = OneTimeLoginUuid.objects.filter(
                uuid=uuid,
                status=True,
                created_at__gt=timezone.now() - timedelta(minutes=10)
            ).select_related('user').first()

            if not uuid_obj:
                return Response(
                    {'error': 'لینک ورود نامعتبر یا منقضی شده است'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            user = uuid_obj.user

            # غیرفعال کردن UUID
            uuid_obj.status = False
            uuid_obj.save()

            # ایجاد توکن
            token = fun.encryptionUser(user)
            return Response({'token': token}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'خطای سیستمی: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegisterFromSpaceViewset(APIView):
    def post(self, request):
        try:
            data = request.data
            logger.info(f"Received data from space API: {data}")  # برای دیباگ

            uniqueIdentifier = data.get('uniqueIdentifier')
            if not uniqueIdentifier:
                return Response({'error': 'شناسه یکتا الزامی است'}, status=status.HTTP_400_BAD_REQUEST)

            # بررسی وجود کاربر
            existing_user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
            if existing_user:
                return Response({'message': 'کاربر وجود دارد'}, status=status.HTTP_200_OK)

            with transaction.atomic():
                # ایجاد کاربر
                user = User.objects.create(
                    uniqueIdentifier=uniqueIdentifier,
                    email=data.get('email'),
                    mobile=str(data.get('mobile', '')),
                    type=data.get('type', ''),
                    status=data.get('status', 'Sejami'),
                    agent=data.get('agent')
                )

                # ایجاد اطلاعات شخص حقیقی
                if data.get('privatePerson'):
                    private_person_data = data['privatePerson']
                    privatePerson.objects.create(
                        user=user,
                        birthDate=private_person_data.get('birthDate', ''),
                        fatherName=private_person_data.get('fatherName', ''),
                        firstName=private_person_data.get('firstName', ''),
                        gender=private_person_data.get('gender', ''),
                        lastName=private_person_data.get('lastName', ''),
                        placeOfBirth=private_person_data.get('placeOfBirth', ''),
                        placeOfIssue=private_person_data.get('placeOfIssue', ''),
                        seriSh=private_person_data.get('seriSh', ''),
                        seriShChar=private_person_data.get('seriShChar', ''),
                        serial=private_person_data.get('serial', ''),
                        shNumber=private_person_data.get('shNumber', ''),
                        signatureFile=private_person_data.get('signatureFile')
                    )

                # ایجاد حساب‌های بانکی
                for account_data in data.get('accounts', []):
                    accounts.objects.create(
                        user=user,
                        accountNumber=account_data.get('accountNumber', ''),
                        bank=account_data.get('bank', {}).get('name', ''),
                        branchCity=account_data.get('branchCity', {}).get('name', ''),
                        branchCode=account_data.get('branchCode', ''),
                        branchName=account_data.get('branchName', ''),
                        isDefault=account_data.get('isDefault', False),
                        modifiedDate=account_data.get('modifiedDate', ''),
                        type=account_data.get('type', ''),
                        sheba=account_data.get('sheba', '')
                    )

                # ایجاد آدرس‌ها
                for address_data in data.get('addresses', []):
                    addresses.objects.create(
                        user=user,
                        alley=address_data.get('alley', ''),
                        city=address_data.get('city', {}).get('name', ''),
                        cityPrefix=address_data.get('cityPrefix', ''),
                        country=address_data.get('country', {}).get('name', ''),
                        countryPrefix=address_data.get('countryPrefix', ''),
                        email=address_data.get('email', ''),
                        emergencyTel=address_data.get('emergencyTel', ''),
                        emergencyTelCityPrefix=address_data.get('emergencyTelCityPrefix', ''),
                        emergencyTelCountryPrefix=address_data.get('emergencyTelCountryPrefix', ''),
                        fax=address_data.get('fax', ''),
                        faxPrefix=address_data.get('faxPrefix', ''),
                        mobile=address_data.get('mobile', ''),
                        plaque=address_data.get('plaque', ''),
                        postalCode=address_data.get('postalCode', ''),
                        province=address_data.get('province', {}).get('name', ''),
                        remnantAddress=address_data.get('remnantAddress', ''),
                        section=address_data.get('section', {}).get('name', ''),
                        tel=address_data.get('tel', ''),
                        website=address_data.get('website', '')
                    )

                # ایجاد اطلاعات مالی
                if data.get('financialInfo'):
                    financial_info_data = data['financialInfo']
                    financialInfo.objects.create(
                        user=user,
                        assetsValue=financial_info_data.get('assetsValue', ''),
                        cExchangeTransaction=financial_info_data.get('cExchangeTransaction', ''),
                        companyPurpose=financial_info_data.get('companyPurpose', ''),
                        financialBrokers=', '.join([broker.get('broker', {}).get('title', '') for broker in financial_info_data.get('financialBrokers', [])]),
                        inComingAverage=financial_info_data.get('inComingAverage', ''),
                        outExchangeTransaction=financial_info_data.get('outExchangeTransaction', ''),
                        rate=financial_info_data.get('rate', ''),
                        rateDate=financial_info_data.get('rateDate', ''),
                        referenceRateCompany=financial_info_data.get('referenceRateCompany', ''),
                        sExchangeTransaction=financial_info_data.get('sExchangeTransaction', ''),
                        tradingKnowledgeLevel=financial_info_data.get('tradingKnowledgeLevel', ''),
                        transactionLevel=financial_info_data.get('transactionLevel', '')
                    )

                # ایجاد اطلاعات شغلی
                if data.get('jobInfo'):
                    job_info_data = data['jobInfo']
                    jobInfo.objects.create(
                        user=user,
                        companyAddress=job_info_data.get('companyAddress', ''),
                        companyCityPrefix=job_info_data.get('companyCityPrefix', ''),
                        companyEmail=job_info_data.get('companyEmail', ''),
                        companyFax=job_info_data.get('companyFax', ''),
                        companyFaxPrefix=job_info_data.get('companyFaxPrefix', ''),
                        companyName=job_info_data.get('companyName', ''),
                        companyPhone=job_info_data.get('companyPhone', ''),
                        companyPostalCode=job_info_data.get('companyPostalCode', ''),
                        companyWebSite=job_info_data.get('companyWebSite', ''),
                        employmentDate=job_info_data.get('employmentDate', ''),
                        job=job_info_data.get('job', {}).get('title', ''),
                        jobDescription=job_info_data.get('jobDescription', ''),
                        position=job_info_data.get('position', '')
                    )

                return Response({'message': 'کاربر با موفقیت ثبت شد'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f'خطا در ثبت اطلاعات: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
