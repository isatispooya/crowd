import datetime
from . import serializers
from .models import Cart , Message  , AddInformation 
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication import fun
from django.http import HttpResponse, HttpResponseNotAllowed
import random
from manager import models


# done
class RequestViewset(APIView):
    def post (self,request):
        Authorization = request.headers.get('Authorization')
        
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        user = fun.decryptionUser(Authorization)

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()

        
        data = request.data.copy()
        if data['date_newspaper'] :

            try:
                timestamp = (int(data['date_newspaper'])/1000)
                data['date_newspaper'] = datetime.datetime.fromtimestamp(timestamp)
            except:
                try:
                    date_str = data['date_newspaper'].rstrip('Z')
                    if '.' in date_str:
                        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
                    else:
                        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                    data['date_newspaper'] = date_obj
                except ValueError:
                    return Response({'error': 'Invalid timestamp for date_newspaper'}, status=status.HTTP_400_BAD_REQUEST)
        if data['year_of_establishment']  :
            try:
                timestamp = (int(data['year_of_establishment'])/1000)
                data['year_of_establishment'] = datetime.datetime.fromtimestamp(timestamp)
            except:
                try:
                    date_str = data['year_of_establishment'].rstrip('Z')
                    if '.' in date_str:
                        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
                    else:
                        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                    data['year_of_establishment'] = date_obj
                except ValueError:
                    return Response({'error': 'Invalid timestamp for year_of_establishment'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.CartSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            cart = serializer.save(user=user)



            for file_field in ['financial_report_thisyear', 'financial_report_lastyear', 'financial_report_yearold',
                               'audit_report_thisyear', 'audit_report_lastyear', 'audit_report_yearold',
                               'statement_thisyear', 'statement_lastyear', 'statement_yearold',
                               'alignment_6columns_thisyear', 'alignment_6columns_lastyear', 'alignment_6columns_yearold',
                               'announcement_of_changes_managers', 'announcement_of_changes_capital',
                               'bank_account_turnover', 'statutes', 'assets_and_liabilities',
                               'latest_insurance_staf', 'claims_status', 'logo']:

                if request.data.get(file_field) == None:
                    serializer.validated_data[file_field] = request.data.get(file_field)


                if file_field in request.FILES:
                    serializer.validated_data[file_field] = request.FILES[file_field]

            code = random.randint(10000, 99999)
            serializer.code = code
            serializer.save()

            response_data = serializer.data
            response_data['id'] = cart.id
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get (self,request) :
        Authorization = request.headers.get('Authorization')    
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()   
        cart = Cart.objects.filter(user=user)
        cart  =cart.order_by('-id')
        cart_serializer  =serializers.CartSerializer(cart ,  many = True)
        return Response ({'message' : True ,  'cart': cart_serializer.data} ,  status=status.HTTP_200_OK )
    

# done
class DetailCartViewset(APIView):    
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        user = fun.decryptionUser(Authorization)

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()   
        cart = Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'cart not found'}, status=status.HTTP_404_NOT_FOUND)
        cart_serializer = serializers.CartSerializer(cart)
        cart_serializer = cart_serializer.data
        cart_serializer['id'] = cart.id

    
        return Response({'message': True, 'cart': cart_serializer}, status=status.HTTP_200_OK)
    

    
    def patch(self,request, id) :
        Authorization = request.headers.get('Authorization')
        
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        user = fun.decryptionUser(Authorization)

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()  
        cart = Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'cart not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data.pop('code', None)
        if data['date_newspaper'] :

            try:
                timestamp = (int(data['date_newspaper'])/1000)
                data['date_newspaper'] = datetime.datetime.fromtimestamp(timestamp)
            except:
                try:
                    date_str = data['date_newspaper'].rstrip('Z')
                    if '.' in date_str:
                        # اگر رشته شامل میلی‌ثانیه‌ها باشد
                        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
                    else:
                        # اگر رشته شامل میلی‌ثانیه‌ها نباشد
                        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                    data['date_newspaper'] = date_obj
                except ValueError:
                    return Response({'error': 'Invalid timestamp for date_newspaper'}, status=status.HTTP_400_BAD_REQUEST)
        if data['year_of_establishment'] :
            try:
                timestamp = (int(data['year_of_establishment'])/1000)
                data['year_of_establishment'] = datetime.datetime.fromtimestamp(timestamp)
            except:
                try:
                    date_str = data['year_of_establishment'].rstrip('Z')
                    if '.' in date_str:
                        # اگر رشته شامل میلی‌ثانیه‌ها باشد
                        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
                    else:
                        # اگر رشته شامل میلی‌ثانیه‌ها نباشد
                        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                    data['year_of_establishment'] = date_obj
                except ValueError:
                    return Response({'error': 'Invalid timestamp for year_of_establishment'}, status=status.HTTP_400_BAD_REQUEST)
        cart_serializer = serializers.CartSerializer(cart, data=data, partial=True)
        if cart_serializer.is_valid():
            cart_serializer.save()
            return Response({'message': 'Cart updated successfully', 'cart': cart_serializer.data}, status=status.HTTP_200_OK)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def delete(self, request, id):
    #         Authorization = request.headers.get('Authorization')
            
    #         if not Authorization:
    #             return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

    #         user = fun.decryptionUser(Authorization)

    #         if not user:
    #             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    #         user = user.first()

    #         cart = Cart.objects.filter(id=id).first()
    #         if not cart:
    #             return Response({'error': 'cart not found'}, status=status.HTTP_404_NOT_FOUND)

    #         cart.delete()
    #         return Response({'message': 'Cart deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

# done
class CartAdmin(APIView) :
    def get(self , request) :
        Authorization = request.headers.get('Authorization')     

        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        
        admin = admin.first()
        cart = Cart.objects.all().order_by('-id')
        cart_serializer = serializers.CartSerializer(cart , many = True)
        return Response ({'message' : True ,  'cart': cart_serializer.data} ,  status=status.HTTP_200_OK )


    def patch (self , request , id) :
        Authorization = request.headers.get('Authorization')    

        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        
        admin = admin.first()

        cart = Cart.objects.filter(id=id).first()

        if not cart:
            return Response({'error': 'cart not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        for file_field in ['financial_report_thisyear', 'financial_report_lastyear', 'financial_report_yearold',
                               'audit_report_thisyear', 'audit_report_lastyear', 'audit_report_yearold',
                               'statement_thisyear', 'statement_lastyear', 'statement_yearold',
                               'alignment_6columns_thisyear', 'alignment_6columns_lastyear', 'alignment_6columns_yearold',
                               'announcement_of_changes_managers', 'announcement_of_changes_capital',
                               'bank_account_turnover', 'statutes', 'assets_and_liabilities',
                               'latest_insurance_staf', 'claims_status', 'logo']:
            if file_field in data :
                if 'null' in request.data.get(file_field) or 'undefined' in request.data.get(file_field):
                    setattr(cart, file_field, None)

            if file_field in request.FILES:
                setattr(cart, file_field, request.FILES[file_field])  
        cart.save()
        data.pop('code', None)
        if 'status' in data :
            cart.status = data['status']
            
        cart_serializer = serializers.CartSerializer(cart)
        # if cart_serializer.is_valid():
        #     cart_serializer.save()
        return Response({'message': 'Cart updated successfully', 'cart': cart_serializer.data}, status=status.HTTP_200_OK)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , id):
        Authorization = request.headers.get('Authorization')    

        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        
        admin = admin.first()

        cart = Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'cart not found'}, status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response({'message': 'Cart deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# done
class DetailCartAdminViewset(APIView):    
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        admin = fun.decryptionadmin(Authorization)

        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()   
        cart = Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'cart not found'}, status=status.HTTP_404_NOT_FOUND)
        cart_serializer = serializers.CartSerializer(cart)
    
        return Response({'message': True, 'cart': cart_serializer.data}, status=status.HTTP_200_OK)
    
# done
class MessageAdminViewSet(APIView):
    def post(self,request,id):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.MessageSerializer(data={**request.data, 'cart': cart.id})
        # اینجا پیامک باید بره
        send_sms = request.query_params.get('send_sms')
        if not serializer.is_valid():
            print(serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            message = serializer.save()  
            return Response({'status': True, 'message': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    

    def get(self , request,id) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = Cart.objects.filter(id=id).first()
        message = Message.objects.filter(cart=cart).order_by('-id').first()
        message_serializer = serializers.MessageSerializer(message)
        return Response ({'status' : True ,  'message': message_serializer.data} ,  status=status.HTTP_200_OK )


# done
class MessageUserViewSet(APIView):
    def get(self , request,id) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart = Cart.objects.filter(id=id).first()
        message = Message.objects.filter(cart=cart).order_by('-id').first()
        if not message: 
            return Response ({'status' : True ,  'message': {"message":"شما هیچ پیامی ندارید"}} ,  status=status.HTTP_200_OK )
        message_serializer = serializers.MessageSerializer(message )
        return Response ({'status' : True ,  'message': message_serializer.data} ,  status=status.HTTP_200_OK )


# done
class AddInformationViewset (APIView) :
    def post (self, request, id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart = Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        addinformation = AddInformation.objects.filter(cart=cart).first()

        if addinformation:

            if request.data.get('announcement_of_changes_managers') == None:
                addinformation.announcement_of_changes_managers = request.data.get('announcement_of_changes_managers')
            if request.data.get('announcement_of_changes_capital') == None:
                addinformation.announcement_of_changes_capital = request.data.get('announcement_of_changes_capital')
            if request.data.get('bank_account_turnover') == None:
                addinformation.bank_account_turnover = request.data.get('bank_account_turnover')
            if request.data.get('statutes') == None:
                addinformation.statutes = request.data.get('statutes')
            if request.data.get('assets_and_liabilities') == None:
                addinformation.assets_and_liabilities = request.data.get('assets_and_liabilities')
            if request.data.get('latest_insurance_staf') == None:
                addinformation.latest_insurance_staf = request.data.get('latest_insurance_staf')
            if request.data.get('claims_status') == None:
                addinformation.claims_status = request.data.get('claims_status')
            if request.data.get('product_catalog') == None:
                addinformation.product_catalog = request.data.get('product_catalog')
            if request.data.get('licenses') == None:
                addinformation.licenses = request.data.get('licenses')
            if request.data.get('auditor_representative') == None:
                addinformation.auditor_representative = request.data.get('auditor_representative')
            if request.data.get('announcing_account_number') == None:
                addinformation.announcing_account_number = request.data.get('announcing_account_number')
                

            # دریافت داده‌های ارسال شده در فایل‌ها (در صورتی که هر کدام ارسال شده باشند)
            if 'announcement_of_changes_managers' in request.FILES:
                addinformation.announcement_of_changes_managers = request.FILES.get('announcement_of_changes_managers')
            if 'announcement_of_changes_capital' in request.FILES:
                addinformation.announcement_of_changes_capital = request.FILES.get('announcement_of_changes_capital')
            if 'bank_account_turnover' in request.FILES:
                addinformation.bank_account_turnover = request.FILES.get('bank_account_turnover')
            if 'statutes' in request.FILES:
                addinformation.statutes = request.FILES.get('statutes')
            if 'assets_and_liabilities' in request.FILES:
                addinformation.assets_and_liabilities = request.FILES.get('assets_and_liabilities')
            if 'latest_insurance_staf' in request.FILES:
                addinformation.latest_insurance_staf = request.FILES.get('latest_insurance_staf')
            if 'claims_status' in request.FILES:
                addinformation.claims_status = request.FILES.get('claims_status')
            if 'product_catalog' in request.FILES:
                addinformation.product_catalog = request.FILES.get('product_catalog')
            if 'licenses' in request.FILES :
                addinformation.licenses = request.FILES.get('licenses')
            if 'auditor_representative' in request.FILES:
                addinformation.auditor_representative = request.FILES.get('auditor_representative')
            if 'announcing_account_number' in request.FILES:
                addinformation.announcing_account_number = request.FILES.get('announcing_account_number')

            # ذخیره تغییرات
            addinformation.save()
            return Response({'message': 'Information updated successfully'}, status=status.HTTP_200_OK)

        data = {
            'announcement_of_changes_managers': request.FILES.get('announcement_of_changes_managers'),
            'announcement_of_changes_capital': request.FILES.get('announcement_of_changes_capital'),
            'bank_account_turnover': request.FILES.get('bank_account_turnover'),
            'statutes': request.FILES.get('statutes'),
            'assets_and_liabilities': request.FILES.get('assets_and_liabilities'),
            'latest_insurance_staf': request.FILES.get('latest_insurance_staf'),
            'claims_status': request.FILES.get('claims_status'),
            'product_catalog': request.FILES.get('product_catalog'),
            'licenses': request.FILES.get('licenses'),
            'auditor_representative': request.FILES.get('auditor_representative'),
            'announcing_account_number': request.FILES.get('announcing_account_number'),
            'cart': cart.id
        }

        serializer = serializers.AddInformationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get (self, request, id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response ({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response ({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response ({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        addinformation = AddInformation.objects.filter(cart=cart).first()
        if not addinformation:
            return Response({'error': 'information not found for this cart'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.AddInformationSerializer(addinformation)
        return Response(serializer.data, status=status.HTTP_200_OK)


# done
class AddInfromationAdminViewset (APIView) :
    def post (self, request, id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        addinformation = AddInformation.objects.filter(cart=cart).first()
        if addinformation:

            if request.data.get('announcement_of_changes_managers') == None:
                addinformation.announcement_of_changes_managers = request.data.get('announcement_of_changes_managers')
            if request.data.get('announcement_of_changes_capital') == None:
                addinformation.announcement_of_changes_capital = request.data.get('announcement_of_changes_capital')
            if request.data.get('bank_account_turnover') == None:
                addinformation.bank_account_turnover = request.data.get('bank_account_turnover')
            if request.data.get('statutes') == None:
                addinformation.statutes = request.data.get('statutes')
            if request.data.get('assets_and_liabilities') == None:
                addinformation.assets_and_liabilities = request.data.get('assets_and_liabilities')
            if request.data.get('latest_insurance_staf') == None:
                addinformation.latest_insurance_staf = request.data.get('latest_insurance_staf')
            if request.data.get('claims_status') == None:
                addinformation.claims_status = request.data.get('claims_status')
            if request.data.get('product_catalog') == None:
                addinformation.product_catalog = request.data.get('product_catalog')
            if request.data.get('licenses') == None:
                addinformation.licenses = request.data.get('licenses')
            if request.data.get('auditor_representative') == None:
                addinformation.auditor_representative = request.data.get('auditor_representative')
            if request.data.get('announcing_account_number') == None:
                addinformation.announcing_account_number = request.data.get('announcing_account_number')


            # دریافت داده‌های ارسال شده در فایل‌ها (در صورتی که هر کدام ارسال شده باشند)

            if 'announcement_of_changes_managers' in request.FILES:
                addinformation.announcement_of_changes_managers = request.FILES.get('announcement_of_changes_managers')
            if 'announcement_of_changes_capital' in request.FILES:
                addinformation.announcement_of_changes_capital = request.FILES.get('announcement_of_changes_capital')
            if 'bank_account_turnover' in request.FILES:
                addinformation.bank_account_turnover = request.FILES.get('bank_account_turnover')
            if 'statutes' in request.FILES:
                addinformation.statutes = request.FILES.get('statutes')
            if 'assets_and_liabilities' in request.FILES:
                addinformation.assets_and_liabilities = request.FILES.get('assets_and_liabilities')
            if 'latest_insurance_staf' in request.FILES:
                addinformation.latest_insurance_staf = request.FILES.get('latest_insurance_staf')
            if 'claims_status' in request.FILES:
                addinformation.claims_status = request.FILES.get('claims_status')
            if 'product_catalog' in request.FILES:
                addinformation.product_catalog = request.FILES.get('product_catalog')
            if 'licenses' in request.FILES:
                addinformation.licenses = request.FILES.get('licenses')
            if 'auditor_representative' in request.FILES:
                addinformation.auditor_representative = request.FILES.get('auditor_representative')
            if 'announcing_account_number' in request.FILES:
                addinformation.announcing_account_number = request.FILES.get('announcing_account_number')
            
            if 'lock_announcement_of_changes_managers' in request.data.copy():
              addinformation.lock_announcement_of_changes_managers = request.data.copy()['lock_announcement_of_changes_managers'] == 'true'
            if 'lock_claims_status' in request.data.copy():
              addinformation.lock_claims_status = request.data.copy()['lock_claims_status'] == 'true'
            if 'lock_announcement_of_changes_capital' in request.data.copy():
              addinformation.lock_announcement_of_changes_capital = request.data.copy()['lock_announcement_of_changes_capital'] == 'true'
            if 'lock_bank_account_turnover' in request.data.copy():
              addinformation.lock_bank_account_turnover = request.data.copy()['lock_bank_account_turnover'] == 'true'
            if 'lock_statutes' in request.data.copy():
              addinformation.lock_statutes = request.data.copy()['lock_statutes'] == 'true'
            if 'lock_assets_and_liabilities' in request.data.copy():
              addinformation.lock_assets_and_liabilities = request.data.copy()['lock_assets_and_liabilities'] == 'true'
            if 'lock_latest_insurance_staf' in request.data.copy():
                addinformation.lock_latest_insurance_staf = request.data.copy()['lock_latest_insurance_staf'] == 'true'
            if 'lock_product_catalog' in request.data.copy():
              addinformation.lock_product_catalog = request.data.copy()['lock_product_catalog'] == 'true'
            if 'lock_licenses' in request.data.copy():
              addinformation.lock_licenses = request.data.copy()['lock_licenses'] == 'true'
            if 'lock_auditor_representative' in request.data.copy():
              addinformation.lock_auditor_representative = request.data.copy()['lock_auditor_representative'] == 'true'
            if 'lock_announcing_account_number' in request.data.copy():
              addinformation.lock_announcing_account_number = request.data.copy()['lock_announcing_account_number'] == 'true'
            # ذخیره تغییرات
            addinformation.save()
            return Response({'message': 'Information updated successfully'}, status=status.HTTP_200_OK)

        data = {
            'announcement_of_changes_managers': request.FILES.get('announcement_of_changes_managers'),
            'announcement_of_changes_capital': request.FILES.get('announcement_of_changes_capital'),
            'bank_account_turnover': request.FILES.get('bank_account_turnover'),
            'statutes': request.FILES.get('statutes'),
            'assets_and_liabilities': request.FILES.get('assets_and_liabilities'),
            'latest_insurance_staf': request.FILES.get('latest_insurance_staf'),
            'claims_status': request.FILES.get('claims_status'),
            'product_catalog': request.FILES.get('product_catalog'),
            'licenses': request.FILES.get('licenses'),
            'auditor_representative': request.FILES.get('auditor_representative'),
            'announcing_account_number': request.FILES.get('announcing_account_number'),
            'cart': cart.id
        }


        serializer = serializers.AddInformationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def get (self, request, id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response ({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        addinformation = AddInformation.objects.filter(cart=cart).first()
        if not addinformation:
            return Response({'error': 'information not found for this cart'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.AddInformationSerializer(addinformation)
        return Response(serializer.data, status=status.HTTP_200_OK)


# done
class FinishCartViewset(APIView):
    def patch (self,request,id) : 
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        finish_cart_value = request.data.get('finish_cart')
        if finish_cart_value is None:
            return Response({'error': 'finish_cart is required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.CartSerializer(cart, data={'finish_cart': finish_cart_value}, partial=True)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)