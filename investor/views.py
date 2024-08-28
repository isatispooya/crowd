from django.shortcuts import render
import datetime
from . import serializers
from .models import Cart , Message
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
        print(data)

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
        cart  =cart.order_by('creat')
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
        cart = Cart.objects.all()
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
    

class MessageViewSet(APIView):
    def post(self, request):
        Authorization = request.headers.get('Authorization')

        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()

        serializer = serializers.MessageSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            message = serializer.save()  
            return Response({'status': True, 'cart': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def get(self , request) :
        Authorization = request.headers.get('Authorization')     

        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        
        admin = admin.first()
        message = Message.objects.all()
        message_serializer = serializers.MessageSerializer(message , many = True)
        return Response ({'message' : True ,  'cart': message_serializer.data} ,  status=status.HTTP_200_OK )



