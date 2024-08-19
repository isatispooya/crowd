from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from GuardPyCaptcha.Captch import GuardPyCaptcha
from rest_framework import status 
import requests
from . import models
from . import serializers
import datetime
from . import fun
import json

class CaptchaViewset(APIView) :
    def get (self,request):
        captcha = GuardPyCaptcha ()
        captcha = captcha.Captcha_generation(num_char=4 , only_num= True)
        return Response ({'captcha' : captcha} , status = status.HTTP_200_OK)
    
    
# otp for user
class OtpViewset(APIView) :
    def post (self,request) :
        captcha = GuardPyCaptcha()
        captcha = captcha.check_response(request.data['encrypted_response'] , request.data['captcha'])
        if False : 
            return Response ({'message' : 'کد کپچا صحیح نیست'} , status=status.HTTP_400_BAD_REQUEST)
        uniqueIdentifier = request.data['uniqueIdentifier']
        if not uniqueIdentifier :
            return Response ({'message' : 'کد ملی را وارد کنید'} , status=status.HTTP_400_BAD_REQUEST)
        user = models.User.objects.filter (uniqueIdentifier = uniqueIdentifier).first()
        if user :
            mobile = user.mobile
            code = 11111 #random.randint(10000,99999)
            otp = models.Otp(mobile=mobile, code=code)
            otp.save()
            # SendSms(mobile ,code)
            return Response({'registered' : True  ,'message' : 'کد تایید ارسال شد' },status=status.HTTP_200_OK)
        
        if not user:
            url = "http://31.40.4.92:8870/otp"
            payload = json.dumps({
            "uniqueIdentifier": uniqueIdentifier
            })
            headers = {
            'X-API-KEY': 'zH7n^K8s#D4qL!rV9tB@2xEoP1W%0uNc',
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code >=300 :
                return Response ({'message' :'شما سجامی نیستید'} , status=status.HTTP_400_BAD_REQUEST)
            return Response ({'registered' :False , 'message' : 'کد تایید از طریق سامانه سجام ارسال شد'},status=status.HTTP_200_OK)

      
        return Response({'registered' : False , 'message' : 'اطلاعات شما یافت نشد'},status=status.HTTP_400_BAD_REQUEST)   
                



        
    

# login for user
class LoginViewset(APIView) :
    def post (self,request) :
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        code = request.data.get('code')
        if not uniqueIdentifier or not code:
            return Response({'message': 'کد ملی و کد تأیید الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = models.User.objects.get(uniqueIdentifier=uniqueIdentifier)
        except:
            result = {'message': ' کد ملی  موجود نیست لطفا ثبت نام کنید'}
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        try:
            mobile = user.mobile
            otp_obj = models.Otp.objects.filter(mobile=mobile , code = code ).order_by('-date').first()
        except :
            return Response({'message': 'کد تأیید نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = serializers.OtpSerializer(otp_obj).data
        if otp['code']== None :
            result = {'message': 'کد تأیید نامعتبر است'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
        otp = serializers.OtpSerializer(otp_obj).data
        dt = datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(otp['date'].replace("Z", "+00:00"))
        
        dt = dt.total_seconds()

        if dt >120 :
            result = {'message': 'زمان کد منقضی شده است'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
        otp_obj.delete()
        token = fun.encryptionUser(user)
        return Response({'access': token} , status=status.HTTP_200_OK)


class SignUpViewset(APIView):
    def post (self, request) :
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        otp = request.data.get('otp')
        if not uniqueIdentifier or not otp:
            return Response({'message': 'کد ملی و کد تأیید الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
        
        url = "http://31.40.4.92:8870/information"
        payload = json.dumps({
        "uniqueIdentifier": uniqueIdentifier,
        "otp": otp
        })
        headers = {
        'X-API-KEY': 'zH7n^K8s#D4qL!rV9tB@2xEoP1W%0uNc',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.content)
        
        return Response({'message': True})











#otp for admin
class OtpAdminViewset(APIView) :
    def post (self,request) :
        captcha = GuardPyCaptcha()
        captcha = captcha.check_response(request.data['encrypted_response'] , request.data['captcha'])
        if False : 
            return Response ({'message' : 'کد کپچا صحیح نیست'} , status=status.HTTP_400_BAD_REQUEST)
        uniqueIdentifier = request.data['uniqueIdentifier']
        if not uniqueIdentifier :
            return Response ({'message' : 'کد ملی را وارد کنید'} , status=status.HTTP_400_BAD_REQUEST)
        try :
            admin = models.Admin.objects.get(uniqueIdentifier = uniqueIdentifier)
        except models.Admin.DoesNotExist:
            return Response({'error': 'Admin not found'}, status=404)

        admin.save()
        mobile = admin.mobile
        result = {'registered' : True , 'message' : 'کد تایید ارسال شد'}    
        code = 11111 #random.randint(10000,99999)
        otp = models.Otp( mobile=mobile, code=code)
        otp.save()
        # SendSms(mobile ,code)
        return Response(result,status=status.HTTP_200_OK)
    




class LoginAdminViewset(APIView) :
    def post (self,request) :
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        code = request.data.get('code')
        if not uniqueIdentifier or not code:
            return Response({'message': 'کد ملی و کد تأیید الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            admin = models.Admin.objects.get(uniqueIdentifier=uniqueIdentifier)
        except:
            result = {'message': ' کد ملی  موجود نیست لطفا ثبت نام کنید'}
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        try:
            mobile = admin.mobile
            otp_obj = models.Otp.objects.filter(mobile=mobile , code = code ).order_by('-date').first()
        except :
            return Response({'message': 'کد تأیید نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = serializers.OtpSerializer(otp_obj).data
        if otp['code']== None :
            result = {'message': 'کد تأیید نامعتبر است'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
        otp = serializers.OtpSerializer(otp_obj).data
        dt = datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(otp['date'].replace("Z", "+00:00"))
        
        dt = dt.total_seconds()

        if dt >120 :
            result = {'message': 'زمان کد منقضی شده است'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
        otp_obj.delete()
        token = fun.encryptionUser(admin)
        return Response({'access': token} , status=status.HTTP_200_OK)
