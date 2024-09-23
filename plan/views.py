from django.shortcuts import render
from .models import Plan , DocumentationFiles ,Appendices ,Participant ,Comment , DocumentationRecieve
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from authentication import fun
from . import serializers
from accounting.models import Wallet
from authentication.models import privatePerson
import datetime
from persiantools.jdatetime import JalaliDate

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

# ارسال عکس برای پلن 
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
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        if 'picture' not in request.FILES:
            return Response({'error': 'No picture file was uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        picture = request.FILES['picture']
        plan.picture = picture
        plan.save()
        return Response({'success': True, 'message': 'Picture updated successfully'}, status=status.HTTP_200_OK)



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
        if ducumentation :
            ducumentation.delete()
        serializer = serializers.DocumentationSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'file' in request.FILES:
            serializer.uploaded_file = request.FILES['file']
        serializer.save(plan=plan)
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
        appendices = Appendices.objects.filter(plan = plan).first()
        if appendices :
            appendices.delete()
        data = request.data.copy()
        serializer = serializers.AppendicesSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'file' in request.FILES:
            serializer.uploaded_file = request.FILES['file']
        serializer.save(plan=plan)
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
        serializer = serializers.ParticipantSerializer(participants, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


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
    

class CommentAdminViewset (APIView) :
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()     
        plan = Plan.objects.filter(id=id).first()
        comment = Comment.objects.filter(plan=plan)
        if not comment:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommenttSerializer(comment , many=True)
        return Response ({'data' :serializer.data} , status=status.HTTP_200_OK)
    

    def patch (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()     
        comment = Comment.objects.filter(id=id).first()
        if not comment:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommenttSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    


class CommentViewset (APIView):
    def post (self,request,id):
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
        comment = Comment.objects.filter(plan=plan , user=user).first()
        if not comment:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommenttSerializer(comment , data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)



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
            return Response({'error': 'Plan not found'}, status=status.HTTP_400_BAD_REQUEST)

        private_person = privatePerson.objects.filter(user=user).first()
        if not private_person:
            return Response({'error': 'privatePerson not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(plan=plan, status=True)
        if not comments.exists():
            return Response({'error': 'Comments not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommenttSerializer(comments, many=True)

        response_data = {
            'comments': serializer.data, 
        }
        return Response({'data': response_data}, status=status.HTTP_200_OK)
    



class DocumationRecieveViewset(APIView) :
    def post (self, request, id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first() 
        plan = Plan.objects.filter(id=id).first()
        if plan.plan_status != '5' :
            return Response({'error': 'Invalid plan status'}, status=status.HTTP_400_BAD_REQUEST)
        


        # تعداد چک 
        number = int(plan.total_time / plan.payment_period)
        # تاریخ اتمام چک

        # مبلغ چک اصل پول
        amount_of_payment = plan.funded_amount
        # مبلغ هر چک سود 
        amount_of_profit  = (plan.funded_amount * int(plan.profit)) / number


        list = []
        for _ in range(number):
            documation = DocumentationRecieve.objects.create(plan=plan, type='2', amount=amount_of_profit) 
            date = JalaliDate(documation.date)
            list.append({
                'type': documation.type,
                'amount': documation.amount,
                'date': str(date),
                'plan' :documation.plan.id
                })
        documation = DocumentationRecieve.objects.create(plan=plan, type='1', amount= amount_of_payment) 
        date = JalaliDate(documation.date)
        list.append({
            'type': documation.type,
            'amount': documation.amount,
            'date': str(date),
            'plan' :documation.plan.id
        })
        return Response ({'message': '5 DocumentationRecieve created','list': list }, status=status.HTTP_200_OK)        
    
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
    
        documation = DocumentationRecieve.objects.filter(plan=plan)
        if not documation:
            return Response({'error': 'documation not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = []
        for doc in documation:
            jalali_date = str(JalaliDate(doc.date))  
            serialized_doc = serializers.DocumationRecieveSerializer(doc).data  
            serialized_doc['date_jalali'] = jalali_date   
            serializer.append(serialized_doc)
        return Response ({'data': serializer},status=status.HTTP_200_OK)
    
    # این متود کامل نیست
    def patch (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first() 

        plan = Plan.objects.filter(id=id).first()
        if plan.plan_status != '5' :
            return Response({'error': 'Invalid plan status'}, status=status.HTTP_400_BAD_REQUEST)    
        
        data_list = request.data  
        if not isinstance(data_list, list):
            return Response({'error': 'Invalid input data format'}, status=status.HTTP_400_BAD_REQUEST)

        updated_list = []
        documation = DocumentationRecieve.objects.filter(plan=plan)
        if len(data_list) != documation.count():
            return Response({'error': 'Number of records does not match with the input data'}, status=status.HTTP_400_BAD_REQUEST)
        
        for documation, doc_data in zip(documation, data_list):
            documation.type = doc_data.get('type', documation.type)
            documation.amount = doc_data.get('amount', documation.amount)
            documation.save()
            date_jalali = JalaliDate(documation.date)
            updated_list.append({
                'type': documation.type,
                'amount': documation.amount,
                'date': str(date_jalali),
                'plan': documation.plan.id
            })

        return Response({
            'message': f'{len(updated_list)} DocumentationRecieve records updated','list': updated_list}, status=status.HTTP_200_OK)

# گواهی مشارکت 
class CertificateViewset (APIView) :
    def get (self, request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        participant = Participant.objects.filter (participant = user)
        if not participant:
            return Response({'error': 'participant not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ParticipantSerializer(participant , many = True)
        data = serializer.data
        for i in data :
            i ['link'] = 'www.isatispooya.com'

        return Response({'data': data}, status=status.HTTP_200_OK)
    



