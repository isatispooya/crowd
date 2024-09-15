from django.shortcuts import render
import datetime
from . import serializers
from .models import Wallet , Transaction 
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication import fun
from django.http import HttpResponse, HttpResponseNotAllowed


class WalletAdminViewset(APIView):
    def get (self,request):
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()

        wallet = Wallet.objects.all()
        if not wallet :
            return Response({'error': 'wallet not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.WalletSerializer(wallet , many = True)
        if serializer:
            return Response({'wallet': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WalletAdmin2Viewset(APIView):
    def patch (self,request,id) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()

        wallet =  Wallet.objects.filter(id=id).first()
        if not wallet :
            return Response({'error': 'wallet not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        serializer = serializers.WalletSerializer(wallet , data = data , partial = True) 
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'wallet updated successfully', 'wallet': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()

        wallet = Wallet.objects.filter(id=id).first()
        if not wallet :
            return Response({'error': 'wallet not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.WalletSerializer(wallet)
        if serializer :
            return Response({'wallet': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 



class WalletViewset(APIView) :
    def get (self,request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()   
        wallet = Wallet.objects.filter(user=user).first()
        serializer = serializers.WalletSerializer(wallet)
        if serializer :
            return Response({'wallet': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class TransactionAdminViewset(APIView):
    def get(self,request) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()

        transaction = Transaction.objects.all()
        if not transaction :
            return Response({'error': 'transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.TransactionSerializer(transaction , many = True)
        if serializer:
            return Response({'transaction': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class TransactionAdmin2Viewset(APIView):
    def get(self,request,id) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()

        transaction = Transaction.objects.filter(id=id).first()
        if not transaction :
            return Response({'error': 'transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.TransactionSerializer(transaction )
        if serializer:
            return Response({'transaction': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  



    def patch (self,request,id) :
        Authorization = request.headers.get('Authorization')     
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()

        transaction =  Transaction.objects.filter(id=id).first()
        if not transaction :
            return Response({'error': 'transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        serializer = serializers.TransactionSerializer(transaction , data = data , partial = True) 
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'transaction updated successfully', 'transaction': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    







class TransactionViewset(APIView) :
    def get (self,request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        wallet = Wallet.objects.filter(user=user).first()
        transaction = Transaction.objects.filter(wallet=wallet)
        serializer = serializers.TransactionSerializer(transaction , many=True)
        if serializer :
            return Response({'transaction': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Transaction2Viewset(APIView):
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()  
        wallet = Wallet.objects.filter(user=user).first()
        transaction = Transaction.objects.filter(id=id , wallet=wallet).first()
        if transaction is None :
            return Response({'error': 'Transaction not found for this user'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.TransactionSerializer(transaction)
        if serializer :
            return Response({'transaction': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

