from django.shortcuts import render
import datetime
from . import serializers
from . import models
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication import fun


class RequestViewset(APIView):
    def post (self,request):
        Authorization = request.headers.get('Authorization')
        
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        user = fun.decryptionUser(Authorization)

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart_serializer = serializers.CartSerializer(data=request.data)
        if cart_serializer.is_valid():
            cart_serializer.save()
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)