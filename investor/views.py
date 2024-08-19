from django.shortcuts import render
import datetime
from . import serializers
from .models import Cart
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
        cart_data = request.data.copy()
        cart_data['user'] = user.id  
        cart_serializer = serializers.CartSerializer(data=cart_data)
        if cart_serializer.is_valid():
            cart_instance = cart_serializer.save()
            code = random.randint(10000,99999)
            cart_instance.code= code
            cart_instance.save()
            return Response({'message' :True , 'cart' : cart_serializer.data } , status=status.HTTP_201_CREATED)
        return Response({'error' :cart_serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
    


    def get (self,request) :
        Authorization = request.headers.get('Authorization')
        
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        user = fun.decryptionUser(Authorization)

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()   
        cart = Cart.objects.filter(user=user)
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
