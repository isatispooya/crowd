from django.shortcuts import render
from investor import models
from manager import models
from .models import SignatureCompany
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication import fun
from investor import serializers



# انتخاب مدیران شرکت برای حق امضا توسط ادمین
class SignatureViewset (APIView):
    def post (self,request,id):
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
        signature, created = SignatureCompany.objects.get_or_create(cart=cart)
        data = request.data
        signature_serializer = serializers.SignatureCompanySerializer(instance=signature, data=data)
        if signature_serializer.is_valid():
            signature_serializer.save()
            return Response(signature_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(signature_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SetSignatureViewset(APIView) :
# فعال کردن وضعیت حق امضای مدیران مشتری توسط ادمین
    def post (self,request,id):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = models.Cart.objects.filter(id=id).first()
        data = request.data.copy()
        manager_ids = data.get('ids', [])
        if not manager_ids or not isinstance(manager_ids, list):
            return Response({'error': 'Manager IDs must be provided as a list'}, status=status.HTTP_400_BAD_REQUEST)
        managers = models.Manager.objects.filter(cart=cart, id__in=manager_ids)
        if not managers.exists():
            return Response({'error': 'No matching managers found'}, status=status.HTTP_404_NOT_FOUND)
        managers.update(signature= True)  
        return Response ({'success': True}, status=status.HTTP_200_OK)
    



# وارد کردن اطلاعات قرارداد عاملیت توسط ادمین
class SetCartAdminViewset(APIView) :
    def post (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = models.Cart.objects.filter(id=id).first()

        data = request.data.copy()

        
        update_fields = [
            'otc_fee', 'publication_fee', 'dervice_fee', 'design_cost',
            'percentage_total_amount', 'payback_period', 'swimming_percentage',
            'partnership_interest', 'guarantee'
        ]

        for i in update_fields:
            if i in data:
                setattr(cart, i, data.get(i))
        cart.save()
        serializer = serializers.CartSerializer(cart)
        return Response ({'success': True , 'cart' : serializer.data}, status=status.HTTP_200_OK)


# وارد کردن اطلاعات قرارداد عاملیت توسط مشتری
class SetCartUserViewset(APIView) :
    def post (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart = models.Cart.objects.filter(id=id).first()

        data = request.data.copy()

        
        update_fields = [
            'otc_fee', 'publication_fee', 'dervice_fee', 'design_cost',
            'percentage_total_amount', 'payback_period', 'swimming_percentage',
            'partnership_interest', 'guarantee'
        ]

        for i in update_fields:
            if i in data:
                setattr(cart, i, data.get(i))
        cart.save()
        serializer = serializers.CartSerializer(cart)
        return Response ({'success': True , 'cart' : serializer.data}, status=status.HTTP_200_OK)

