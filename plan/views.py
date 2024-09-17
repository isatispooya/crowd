from django.shortcuts import render
from .models import Plan , DocumentationFiles ,Appendices ,Participant
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from authentication import fun
from . import serializers
from accounting.models import Wallet
class PlanAdminViewset(APIView):
    def post(self, request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        serializer = serializers.PlanSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        serializer.save()
        return Response({'success': True,'data': serializer.data}, status=status.HTTP_201_CREATED)
    


    def get (self,request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.all()
        serializer = serializers.PlanSerializer(plan, many=True)     
        return Response({'success': True,'data': serializer.data}, status=status.HTTP_200_OK)



class PlanAdmin2Viewset(APIView):

    def patch (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.get(id=id)
        serializer = serializers.PlanSerializer(plan, data=request.data, partial=True)
        
        if not serializer.is_valid():
            print(serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'success': True,'data': serializer.data}, status=status.HTTP_201_CREATED)


    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(id=id).first()
        if not plan:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.PlanSerializer(plan)

        return Response({'success': True,'data': serializer.data}, status=status.HTTP_200_OK)



    def delete (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(id=id).first()
        if not plan:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        plan.delete()
        return Response({'success': 'plan deleted'}, status=status.HTTP_200_OK)



class PlanViewset(APIView):
    def get (self, request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        plan = Plan.objects.all()
        serializer = serializers.PlanSerializer(plan, many=True)     
        return Response({'success': True,'data': serializer.data}, status=status.HTTP_200_OK)
    

class Plan2Viewset(APIView):

    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        plan = Plan.objects.filter(id=id).first()
        if not plan:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.PlanSerializer(plan)

        return Response({'success': True,'data': serializer.data}, status=status.HTTP_200_OK)




class DocumentationAdminViewset(APIView) :
    def post (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(id=id).first()
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        ducumentation = DocumentationFiles.objects.filter(plan = plan).first()
        serializer = serializers.DocumentationSerializer(ducumentation,data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'file' in request.FILES:
            serializer.uploaded_file = request.FILES['file']
        serializer.save()
        return Response ({'data' : serializer.data} , status=status.HTTP_200_OK)
    

    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(id=id).first()
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        ducumentation = DocumentationFiles.objects.filter(plan=plan).first()
        serializer = serializers.DocumentationSerializer(ducumentation)
        return Response({'data' :serializer.data} , status=status.HTTP_200_OK)

class DocumentationViewset(APIView):
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        plan = Plan.objects.filter(id=id).first()
        documentation = DocumentationFiles.objects.filter(plan=plan)
        serializer = serializers.DocumentationSerializer(documentation , many = True)
        return Response({'data' :serializer.data} , status=status.HTTP_200_OK)
    
    
class AppendicesAdminViewset(APIView) :
    def post (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(id=id).first()
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        appendices = Appendices.objects.filter(plan = plan).first()
        if not appendices :
            return Response({'error': 'Appendices not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.AppendicesSerializer(appendices,data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'file' in request.FILES:
            serializer.uploaded_file = request.FILES['file']
        serializer.save()
        return Response ({'data' : serializer.data} , status=status.HTTP_200_OK)
    

    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(id=id).first()
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        appendices = Appendices.objects.filter(plan=plan).first()
        if not appendices :
            return Response({'error': 'Appendices not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.AppendicesSerializer(appendices)
        return Response({'data' :serializer.data} , status=status.HTTP_200_OK)



class AppendicesViewset(APIView):
    def get (self,request,id):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        plan = Plan.objects.filter(id=id).first()
        appendices = Appendices.objects.filter(plan=plan)
        serializer = serializers.AppendicesSerializer(appendices , many = True)
        return Response({'data' :serializer.data} , status=status.HTTP_200_OK)
    


class ParticipantViewset(APIView):
    def post(self,request,id):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()      
        plan = Plan.objects.filter(id=id).first()
        amount = request.data.get('amount')
        try:
            amount = int(amount)  
        except ValueError:
            return Response({'error': 'Invalid amount value, it should be an integer'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            nominal_price = plan.nominal_price_certificate
            total_amount = amount * int(nominal_price)
            print(total_amount)
        except AttributeError:
            return Response({'error': 'Plan does not have nominal_price_certificate'}, status=status.HTTP_400_BAD_REQUEST)
        participant = Participant.objects.filter(plan=plan, participant=user).first()
        if not participant:
            participant = Participant.objects.create(plan=plan, participant=user, amount=amount, total_amount=total_amount)
        serializer_data = {
            'amount': amount,
            'total_amount': total_amount,
            'plan':plan
        }
        serializer = serializers.ParticipantSerializer(participant, data=serializer_data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        wallet = Wallet.objects.filter(user=user).first()
        if not wallet :
            return Response({'error': 'Wallet does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if  total_amount >= wallet.remaining :
            return Response({'error' : 'کیف پول شما شارژ نیست'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    


    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()      
        plan = Plan.objects.filter(id=id).first()
        participants = Participant.objects.filter(plan=plan)
        serializer = serializers.ParticipantSerializer(participants , many = True)
        return Response ({'data' :serializer.data} , status=status.HTTP_200_OK)
    


class ParticipantAdminViewset(APIView):
    
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()     
        plan = Plan.objects.filter(id=id).first()
        participants = Participant.objects.filter(plan=plan)
        serializer = serializers.ParticipantSerializer(participants , many = True)
        return Response ({'data' :serializer.data} , status=status.HTTP_200_OK)
    