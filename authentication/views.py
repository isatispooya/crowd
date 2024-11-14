from rest_framework.views import APIView
from rest_framework.response import Response
from GuardPyCaptcha.Captch import GuardPyCaptcha
from rest_framework import status 
import requests
from .models import User , Otp , Captcha , Admin , accounts ,addresses ,BlacklistedToken, financialInfo , jobInfo , privatePerson ,tradingCodes , Reagent , legalPersonShareholders , legalPersonStakeholders , LegalPerson
from . import serializers
import datetime
from . import fun
import json
import random
import os
from utils.message import Message
from plan.views import check_legal_person
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit   
from django.utils.decorators import method_decorator
from django.conf import settings
from django.db import transaction


class CaptchaViewset(APIView) :
    @method_decorator(ratelimit(key='ip', rate='20/m', method='GET', block=True))
    def get (self,request):
        captcha = GuardPyCaptcha ()
        captcha = captcha.Captcha_generation(num_char=4 , only_num= True)
        Captcha.objects.create(encrypted_response=captcha['encrypted_response'])
        captcha_obj = Captcha.objects.filter(encrypted_response=captcha['encrypted_response'],enabled=True).first()


        return Response ({'captcha' : captcha} , status = status.HTTP_200_OK)

# otp for user
class OtpViewset(APIView) :
    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST', block=True))
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
        if not settings.DEBUG : 
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
            try : 
                address = addresses.objects.filter(user=user).first()
                address_email = address.email
                message = Message(code,user.mobile,address_email)
                message.otpSMS()
                try:
                    message.otpEmail()
                except Exception as e:
                    print(f"Failed to send OTP via email: {e}")

            except:
                message = Message(code, user.mobile, None)
                message.otpSMS()
            

            return Response({'message' : 'کد تایید ارسال شد' },status=status.HTTP_200_OK)
        
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
                

        
# login or sign up user
# done
class LoginViewset(APIView):
    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST', block=True))
    def post (self, request) :
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        otp = request.data.get('otp')
        reference = request.data.get('reference')  
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
            return Response({'message' :'1دوباره تلاش کن '}, status=status.HTTP_400_BAD_REQUEST)
        if data == None :
            return Response({'message' :'بیشتر تلاش کن '}, status=status.HTTP_400_BAD_REQUEST)
        new_user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
        try :
            with transaction.atomic():
                if  not new_user :
                    new_user  =User(
                    agent = data ['agent'],
                    email = data ['email'],
                    mobile = data ['mobile'],
                    status = data ['status'],
                    type = data ['type'],
                    uniqueIdentifier = data ['uniqueIdentifier'],
                    referal = data ['uniqueIdentifier'],
                )
                new_user.save()
                if reference:
                    try :
                        reference_user = User.objects.get(uniqueIdentifier=reference)
                        Reagent.objects.create(reference=reference_user, referrer=new_user)
                    except User.DoesNotExist:
                        pass
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
                            
                   

                try :
                    accounts_data = data.get('accounts',[])
                    print(accounts_data)
                    if accounts_data:
                        for account_data in accounts_data:
                            accounts.objects.create(
                                user=new_user,
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
                except :
                    return Response({'message': 'خطا در ثبت اطلاعات اصلی کاربر - حساب ها'}, status=status.HTTP_400_BAD_REQUEST)

                
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
                    return Response({'message': 'خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شغلی'}, status=status.HTTP_400_BAD_REQUEST)


                try :
                    privatePerson_data = data.get('privatePerson')
                    if isinstance(privatePerson_data, dict):
                        birthDate = privatePerson_data.get('birthDate', '')
                        fatherName = privatePerson_data.get('fatherName', '')
                        firstName = privatePerson_data.get('firstName', '')
                        gender = privatePerson_data.get('gender', '')
                        lastName = privatePerson_data.get('lastName', '')
                        placeOfBirth = privatePerson_data.get('placeOfBirth', '')
                        placeOfIssue = privatePerson_data.get('placeOfIssue', '')
                        seriSh = privatePerson_data.get('seriSh', '')
                        serial = privatePerson_data.get('serial', '')
                        shNumber = privatePerson_data.get('shNumber', '')
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
                    return Response({'message': 'خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شخص حقیقی'}, status=status.HTTP_400_BAD_REQUEST)

                try :
                    trading_codes = data.get('tradingCodes', [])
                    if trading_codes:
                        for tradingCodes_data in trading_codes:
                            tradingCodes.objects.create(
                                user = new_user,
                            code = tradingCodes_data.get('code', ''),
                            firstPart = tradingCodes_data.get('firstPart', ''),
                            secondPart = tradingCodes_data.get('secondPart', ''),
                            thirdPart = tradingCodes_data.get('thirdPart', ''),
                                type = tradingCodes_data.get('type', ''),
                            )
                except :
                    return Response({'message': 'خطا در ثبت اطلاعات اصلی کاربر - کد های بورسی'}, status=status.HTTP_400_BAD_REQUEST)

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
                except :
                    return Response({'message': 'خطا در ثبت اطلاعات اصلی کاربر - پرسش های مالی'}, status=status.HTTP_400_BAD_REQUEST)



                try :   
                    address = data.get('addresses',[])
                    for addresses_data in address:
                        city_data = addresses_data.get('city', {}) or {}
                        country_data = addresses_data.get('country', {}) or {}
                        province_data = addresses_data.get('province', {}) or {}
                        section_data = addresses_data.get('section', {}) or {}
                    
                    addresses.objects.create(
                        user = new_user,
                        alley = addresses_data.get('alley', ''),
                        city = city_data.get('name', ''),
                        cityPrefix = addresses_data.get('cityPrefix', ''),
                        country = country_data.get('name', ''),
                        countryPrefix = addresses_data.get('countryPrefix', ''),
                        email = addresses_data.get('email', ''),
                        emergencyTel = addresses_data.get('emergencyTel', ''),
                        emergencyTelCityPrefix = addresses_data.get('emergencyTelCityPrefix', ''),
                        emergencyTelCountryPrefix = addresses_data.get('emergencyTelCountryPrefix', ''),
                        fax = addresses_data.get('fax', ''),
                        faxPrefix = addresses_data.get('faxPrefix', ''),
                        mobile = addresses_data.get('mobile', ''),
                        plaque = addresses_data.get('plaque', ''),
                        postalCode = addresses_data.get('postalCode', ''),
                        province = province_data.get('name', ''),
                        remnantAddress = addresses_data.get('remnantAddress', ''),
                        section = section_data.get('name', ''),
                        tel = addresses_data.get('tel', ''),
                            website = addresses_data.get('website', ''),
                        )
                except :
                    return Response({'message': 'خطا در ثبت اطلاعات اصلی کاربر - آدرس ها'}, status=status.HTTP_400_BAD_REQUEST)

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
                    return Response({'message': 'خطا در ثبت اطلاعات اصلی کاربر - هیئت مدیره'}, status=status.HTTP_400_BAD_REQUEST)


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
                    return Response({'message': 'خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شرکت'}, status=status.HTTP_400_BAD_REQUEST)


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
                    return Response({'message': 'خطا در ثبت اطلاعات اصلی کاربر - سهامداران'}, status=status.HTTP_400_BAD_REQUEST)
                        
        except Exception as e:
            print('ss',e)
            return Response({'message': 'خطایی نامشخص رخ داده است'}, status=status.HTTP_400_BAD_REQUEST)

        token = fun.encryptionUser(new_user)

        return Response({'message': True , 'access' :token} , status=status.HTTP_200_OK)


# done
class InformationViewset (APIView) :
    @method_decorator(ratelimit(key='ip', rate='20/m', method='GET', block=True))
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
    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST', block=True))
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
            message = Message(code,admin.mobile,admin.email)
            message.otpSMS()
            try:
                message.otpEmail()
            except Exception as e:
                print(f'Error sending otp email: {e}')
            return Response({'message' : 'کد تایید ارسال شد' },status=status.HTTP_200_OK)
    
        return Response({'message' : 'کد تایید ارسال شد' },status=status.HTTP_200_OK)




# login for admin
# done
class LoginAdminViewset(APIView) :
    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST', block=True))
    def post (self,request) :
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        code = request.data.get('code')
        if not uniqueIdentifier or not code:
            return Response({'message': 'کد ملی و کد تأیید الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            admin = Admin.objects.get(uniqueIdentifier=uniqueIdentifier)
            if admin.is_locked():
                return Response({'message': 'حساب شما قفل است، لطفاً بعد از مدتی دوباره تلاش کنید.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except admin.DoesNotExist:
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



# done
class UserListViewset (APIView) :
    @method_decorator(ratelimit(key='ip', rate='20/m', method='GET', block=True))
    def get (self, request) :
        Authorization = request.headers.get('Authorization')    
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_401_UNAUTHORIZED)
        admin = admin.first()
        user = User.objects.all()
        user_serializer = serializers.UserSerializer(user,many=True).data
        user_list = []

        for i, user_data in enumerate(user_serializer):
            i_user = user[i]  
            privateperson = privatePerson.objects.filter(user=i_user)
            privateperson_serializer = serializers.privatePersonSerializer(privateperson, many=True).data
            
            user_addresses = addresses.objects.filter(user=i_user)
            serializer_addresses = serializers.addressesSerializer(user_addresses , many=True).data
            
            user_financialInfo = financialInfo.objects.filter(user=i_user)
            serializer_financialInfo = serializers.financialInfoSerializer(user_financialInfo , many=True).data
            
            
            user_accounts = accounts.objects.filter(user=i_user)
            serializer_accounts = serializers.accountsSerializer(user_accounts , many=True).data
            
            user_jobInfo = jobInfo.objects.filter(user=i_user)
            serializer_jobInfo = serializers.jobInfoSerializer(user_jobInfo , many=True).data
            
            user_tradingCodes = tradingCodes.objects.filter(user=i_user)
            serializer_tradingCodes = serializers.tradingCodesSerializer(user_tradingCodes , many=True).data
            
            legal_person_shareholder = legalPersonShareholders.objects.filter(user=i_user)
            serializer_legal_person_shareholder = serializers.legalPersonShareholdersSerializer(legal_person_shareholder , many=True).data

            legal_person = LegalPerson.objects.filter(user=i_user)
            serializer_legal_person = serializers.LegalPersonSerializer(legal_person , many=True).data

            legal_person_stakeholders = legalPersonStakeholders.objects.filter(user=i_user)
            serializer_legal_person_stakeholders = serializers.legalPersonStakeholdersSerializer(legal_person_stakeholders , many=True).data

            combined_data = {
                **user_data,  
                'addresses': serializer_addresses,
                'accounts': serializer_accounts,
                'private_person': privateperson_serializer,
                'financial_info': serializer_financialInfo,
                'job_info': serializer_jobInfo,
                'trading_codes': serializer_tradingCodes,
                'legal_person_shareholder': serializer_legal_person_shareholder,
                'legal_person': serializer_legal_person,
                'legal_person_stakeholders': serializer_legal_person_stakeholders,
            }
            
            user_list.append(combined_data)

        return Response(user_list, status=status.HTTP_200_OK)


# done
class UserOneViewset(APIView) :
    @method_decorator(ratelimit(key='ip', rate='20/m', method='GET', block=True))
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')    
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_401_UNAUTHORIZED)
        admin = admin.first()
        user = User.objects.filter(id=id).first()
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

        combined_data = {
            **user_serializer, 
            'addresses': serializer_addresses,
            'private_person': privateperson_serializer,
            'financial_info': serializer_financialInfo,
            'job_info': serializer_jobInfo,
            'trading_codes': serializer_tradingCodes,
        }

        return Response({'success': combined_data}, status=status.HTTP_200_OK)

# done
class OtpUpdateViewset(APIView) :
    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST', block=True))
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
    @method_decorator(ratelimit(key='ip', rate='20/m', method='PATCH', block=True))
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
        
        if new_user:
            new_user.agent = data.get('agent', new_user.agent)
            new_user.email = data.get('email', new_user.email)
            new_user.mobile = data.get('mobile', new_user.mobile)
            new_user.status = data.get('status', new_user.status)
            new_user.type = data.get('type', new_user.type)
            new_user.referal = data.get('uniqueIdentifier', new_user.referal)
            new_user.save()

            if data.get('accounts'):
                    for accounts_data in data['accounts']:
                        accounts.objects.create(
                            user=new_user,
                            accountNumber=accounts_data.get('accountNumber', ''),
                            bank=accounts_data.get('bank', {}).get('name', ''),
                            branchCity=accounts_data.get('branchCity', {}).get('name', ''),
                            branchCode=accounts_data.get('branchCode', ''), 
                            branchName=accounts_data.get('branchName', ''),
                            isDefault=accounts_data.get('isDefault', False),
                            modifiedDate=accounts_data.get('modifiedDate', ''),
                            type=accounts_data.get('type', ''),
                            sheba=accounts_data.get('sheba', '')
                        )
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

            address = data.get('addresses',[])
            for addresses_data in address:
                    city_data = addresses_data.get('city', {}) or {}
                    country_data = addresses_data.get('country', {}) or {}
                    province_data = addresses_data.get('province', {}) or {}
                    section_data = addresses_data.get('section', {}) or {}
                    
                    addresses.objects.create(
                        user = new_user,
                        alley = addresses_data.get('alley', ''),
                        city = city_data.get('name', ''),
                        cityPrefix = addresses_data.get('cityPrefix', ''),
                        country = country_data.get('name', ''),
                        countryPrefix = addresses_data.get('countryPrefix', ''),
                        email = addresses_data.get('email', ''),
                        emergencyTel = addresses_data.get('emergencyTel', ''),
                        emergencyTelCityPrefix = addresses_data.get('emergencyTelCityPrefix', ''),
                        emergencyTelCountryPrefix = addresses_data.get('emergencyTelCountryPrefix', ''),
                        fax = addresses_data.get('fax', ''),
                        faxPrefix = addresses_data.get('faxPrefix', ''),
                        mobile = addresses_data.get('mobile', ''),
                        plaque = addresses_data.get('plaque', ''),
                        postalCode = addresses_data.get('postalCode', ''),
                        province = province_data.get('name', ''),
                        remnantAddress = addresses_data.get('remnantAddress', ''),
                        section = section_data.get('name', ''),
                        tel = addresses_data.get('tel', ''),
                        website = addresses_data.get('website', ''),
                    )

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
            
            privatePerson_data = data.get('privatePerson')
            if isinstance(privatePerson_data, dict):
                birthDate = privatePerson_data.get('birthDate', '')
                fatherName = privatePerson_data.get('fatherName', '')
                firstName = privatePerson_data.get('firstName', '')
                gender = privatePerson_data.get('gender', '')
                lastName = privatePerson_data.get('lastName', '')
                placeOfBirth = privatePerson_data.get('placeOfBirth', '')
                placeOfIssue = privatePerson_data.get('placeOfIssue', '')
                seriSh = privatePerson_data.get('seriSh', '')
                serial = privatePerson_data.get('serial', '')
                shNumber = privatePerson_data.get('shNumber', '')
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


        return Response({'success': True}, status=status.HTTP_200_OK)
    


class AddBoursCodeUserViewset(APIView):
    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST', block=True))
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
    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST', block=True))
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
    





