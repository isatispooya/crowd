from django.shortcuts import render
import datetime
from . import serializers
from .models import Cart , Message , SetStatus
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication import fun
from django.http import HttpResponse, HttpResponseNotAllowed
import random

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

        serializer = serializers.CartSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)  # چاپ خطاها برای بررسی
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():

            cart = serializer.save(user=user)
            
            if 'financial_report_thisyear' in request.FILES:
                serializer.uploaded_file1 = request.FILES['financial_report_thisyear']
            if 'financial_report_lastyear' in request.FILES:
                serializer.uploaded_file2 = request.FILES['financial_report_lastyear']
            if 'financial_report_yearold' in request.FILES:
                serializer.uploaded_file3 = request.FILES['financial_report_yearold']
                

            if 'audit_report_thisyear' in request.FILES:
                serializer.uploaded_file3 = request.FILES['audit_report_thisyear']
            if 'audit_report_lastyear' in request.FILES:
                serializer.uploaded_file3 = request.FILES['audit_report_lastyear']
            if 'audit_report_yearold' in request.FILES:
                serializer.uploaded_file3 = request.FILES['audit_report_yearold']
            

            if 'statement_thisyear' in request.FILES:
                serializer.uploaded_file3 = request.FILES['statement_thisyear']
            if 'statement_lastyear' in request.FILES:
                serializer.uploaded_file3 = request.FILES['statement_lastyear']
            if 'statement_yearold' in request.FILES:
                serializer.uploaded_file3 = request.FILES['statement_yearold']


            if 'alignment_6columns_thisyear' in request.FILES:
                serializer.uploaded_file3 = request.FILES['alignment_6columns_thisyear']
            if 'alignment_6columns_lastyear' in request.FILES:
                serializer.uploaded_file3 = request.FILES['alignment_6columns_lastyear']
            if 'alignment_6columns_yearold' in request.FILES:
                serializer.uploaded_file3 = request.FILES['alignment_6columns_yearold']


            if 'announcement_of_changes_managers' in request.FILES:
                serializer.uploaded_file3 = request.FILES['announcement_of_changes_managers']

            if 'announcement_of_changes_capital' in request.FILES:
                serializer.uploaded_file3 = request.FILES['announcement_of_changes_capital']

            if 'bank_account_turnover' in request.FILES:
                serializer.uploaded_file3 = request.FILES['bank_account_turnover']

            if 'statutes' in request.FILES:
                serializer.uploaded_file3 = request.FILES['statutes']

            if 'assets_and_liabilities' in request.FILES:
                serializer.uploaded_file3 = request.FILES['assets_and_liabilities']

            if 'latest_insurance_staf' in request.FILES:
                serializer.uploaded_file3 = request.FILES['latest_insurance_staf']

            if 'claims_status' in request.FILES:
                serializer.uploaded_file3 = request.FILES['claims_status']

            code = random.randint(10000,99999)
            serializer.code= code
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
    
        return Response({'message': True, 'cart': cart_serializer.data}, status=status.HTTP_200_OK)
    

    
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
        cart_serializer = serializers.CartSerializer(cart, data=data, partial=True)
        if cart_serializer.is_valid():
            cart_serializer.save()
            return Response({'message': 'Cart updated successfully', 'cart': cart_serializer.data}, status=status.HTTP_200_OK)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
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

            cart.delete()
            return Response({'message': 'Cart deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    


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
        data.pop('code', None)
        if 'status' in data :
            cart.status = data['status']
            
        cart_serializer = serializers.CartSerializer(cart, data = data , partial=True)
        if cart_serializer.is_valid():
            cart_serializer.save()
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



class SetStatusViesset(APIView) :
    def post(self , request, id) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        data = request.data.copy()
        cart = Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'cart not found'}, status=status.HTTP_404_NOT_FOUND)
        print(cart)
        set_status = SetStatus.objects.filter(cart=cart).first()
        print(set_status)
        if set_status :
            set_status.delete()
        data['cart'] = cart.id   
        serializer = serializers.SetStatusSerializer(data=data)
        if serializer.is_valid():
            set_status = serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self , request, id) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)
        user = user.first()
        cart = Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'cart not found'}, status=status.HTTP_400_BAD_REQUEST)
        set_status = SetStatus.objects.filter(cart=cart).first()
        if not set_status:
            return Response({'error' : 'status not found'}, status=status.HTTP_400_BAD_REQUEST)
        print(set_status)
        serializer = serializers.SetStatusSerializer(set_status)
        return Response({'message' : serializer.data}, status=status.HTTP_200_OK)
    


class SetStatusAdminViesset(APIView) :
    def post(self , request, id) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        data = request.data.copy()
        cart = Cart.objects.filter(id=id).first()
        print(cart)
        set_status = SetStatus.objects.filter(cart=cart).first()
        print(set_status)
        if set_status :
            set_status.delete()
        data['cart'] = cart.id   
        serializer = serializers.SetStatusSerializer(data=data)
        if serializer.is_valid():
            set_status = serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self,request) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()  
        carts = Cart.objects.all()
        if not carts:
            return Response({'error': 'cart not found'}, status=status.HTTP_400_BAD_REQUEST)
        response_data = []
        for cart in carts:
            set_status = SetStatus.objects.filter(cart=cart).first()
            status_serializer = serializers.SetStatusSerializer(set_status)
            cart_data = {
                'status': status_serializer.data if set_status else None
            }
            response_data.append(cart_data)

        return Response({'carts': response_data}, status=status.HTTP_200_OK)
        


    