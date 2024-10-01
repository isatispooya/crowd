from django.shortcuts import render
from .models import Plan , DocumentationFiles ,Appendices ,Comment , DocumentationRecieve , Plans ,ProjectOwnerCompan , PaymentGateway ,PicturePlan , InformationPlan , EndOfFundraising
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from authentication import fun
from . import serializers
from accounting.models import Wallet
from investor.models import Cart
from authentication.models import privatePerson , User
import datetime
from persiantools.jdatetime import JalaliDate
from dateutil.relativedelta import relativedelta
import pandas as pd
from .CrowdfundingAPIService import CrowdfundingAPI
from dateutil.relativedelta import relativedelta




def get_name (uniqueIdentifier) :
    user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
    privateperson = privatePerson.objects.filter(user=user).first()
    first_name = privateperson.firstName
    last_name = privateperson.lastName
    full_name = first_name + ' ' + last_name

    return full_name


# done
class PlanViewset(APIView):
    def get(self, request, trace_code):
        plan = Plan.objects.filter(trace_code=trace_code)
        if not plan.exists ():
            return Response({'message':'not found plan'}, status=status.HTTP_404_NOT_FOUND)
        plan = plan.first()
        response = serializers.PlanSerializer(plan)
        return Response(response.data, status=status.HTTP_200_OK)
# done
class PlansViewset(APIView):
    def get(self, request):
        plan = Plan.objects.filter()
        response =serializers.PlanSerializer(plan, many=True)
        return Response(response.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        crowd_founding_api = CrowdfundingAPI()
        plan_list = crowd_founding_api.get_company_projects()
        for i in plan_list : 
            if not Plans.objects.filter(plan_id = i).exists () :
                plan = Plans.objects.create(plan_id=i)
        for i in plan_list:    
            plan_detail = crowd_founding_api.get_project_info(i)

        
            plan, created = Plan.objects.update_or_create(
                trace_code=i,
                defaults={
                    'creation_date': plan_detail.get('Creation Date', None),
                    'persian_name': plan_detail.get('Persian Name', None),
                    'persian_suggested_symbol': plan_detail.get('Persian Suggested Symbol', None),
                    'persoan_approved_symbol': plan_detail.get('Persoan Approved Symbol', None),
                    'english_name': plan_detail.get('English Name', None),
                    'english_suggested_symbol': plan_detail.get('English Suggested Symbol', None),
                    'english_approved_symbol': plan_detail.get('English Approved Symbol', None),
                    'industry_group_id': plan_detail.get('Industry Group ID', None),
                    'industry_group_description': plan_detail.get('Industry Group Description', None),
                    'sub_industry_group_id': plan_detail.get('Sub Industry Group ID', None),
                    'sub_industry_group_description': plan_detail.get('Sub Industry Group Description', None),
                    'persian_subject': plan_detail.get('Persian Subject', None),
                    'english_subject': plan_detail.get('English Subject', None),
                    'unit_price': plan_detail.get('Unit Price', None),
                    'total_units': plan_detail.get('Total Units', None),
                    'company_unit_counts': plan_detail.get('Company Unit Counts', None),
                    'total_price': plan_detail.get('Total Price', None),
                    'crowd_funding_type_id': plan_detail.get('Crowd Funding Type ID', None),
                    'crowd_funding_type_description': plan_detail.get('Crowd Funding Type Description', None),
                    'float_crowd_funding_type_description': plan_detail.get('Float Crowd Funding Type Description', None),
                    'minimum_required_price': plan_detail.get('Minimum Required Price', None),
                    'real_person_minimum_availabe_price': plan_detail.get('Real Person Minimum Availabe Price', None),
                    'real_person_maximum_available_price': plan_detail.get('Real Person Maximum Available Price', None),
                    'legal_person_minimum_availabe_price': plan_detail.get('Legal Person Minimum Availabe Price', None),
                    'legal_person_maximum_availabe_price': plan_detail.get('Legal Person Maximum Available Price', None),
                    'underwriting_duration': plan_detail.get('Underwriting Duration', None),
                    'suggested_underwriting_start_date': plan_detail.get('Suggested Underwriting Start Date', None),
                    'suggested_underwriting_end_date': plan_detail.get('Suggested Underwriting End Date', None),
                    'approved_underwriting_start_date': plan_detail.get('Approved Underwriting Start Date', None),
                    'approved_underwriting_end_date': plan_detail.get('Approved Underwriting End Date', None),
                    'project_start_date': plan_detail.get('Project Start Date', None),
                    'project_end_date': plan_detail.get('Project End Date', None),
                    'settlement_description': plan_detail.get('Settlement Description', None),
                    'project_status_description': plan_detail.get('Project Status Description', None),
                    'project_status_id': plan_detail.get('Project Status ID', None),
                    'persian_suggested_underwiring_start_date': plan_detail.get('Persian Suggested Underwiring Start Date', None),
                    'persian_suggested_underwriting_end_date': plan_detail.get('Persian Suggested Underwriting End Date', None),
                    'persian_approved_underwriting_start_date': plan_detail.get('Persian Approved Underwriting Start Date', None),
                    'persian_approved_underwriting_end_date': plan_detail.get('Persian Approved Underwriting End Date', None),
                    'persian_project_start_date': plan_detail.get('Persian Project Start Date', None),
                    'persian_project_end_date': plan_detail.get('Persian Project End Date', None),
                    'persian_creation_date': plan_detail.get('Persian Creation Date', None),
                    'number_of_finance_provider': plan_detail.get('Number of Finance Provider', None),
                    'sum_of_funding_provided': plan_detail.get('SumOfFundingProvided', None)
                }
            )
            if len(plan_detail.get('Project Owner Company', [])) > 0:
                for j in plan_detail['Project Owner Company']:
                    project_owner_company, _ = ProjectOwnerCompan.objects.update_or_create(
                        plan=plan,
                        national_id=j.get('National ID', None),
                        defaults={
                            'name': j.get('Name', None),
                            'compnay_type_id': j.get('Company Type ID', None),
                            'company_type_description': j.get('Company Type Description', None),
                            'registration_date': j.get('Registration Date', None),
                            'registration_number': j.get('Registration Number', None),
                            'economic_id': j.get('Economic ID', None),
                            'address': j.get('Address', None),
                            'postal_code': j.get('Postal Code', None),
                            'phone_number': j.get('Phone Number', None),
                            'fax_number': j.get('Fax Number', None),
                            'email_address': j.get('Email Address', None)
                        }
                    )
        return Response({'message':'بروزرسانی از فرابورس انجام شد'}, status=status.HTTP_200_OK)
# done
class AppendicesViewset(APIView) :
    def post (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        serializer = serializers.AppendicesSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'file' in request.FILES:
            serializer.uploaded_file = request.FILES['file']
        serializer.save(plan=plan)
        return Response (serializer.data, status=status.HTTP_200_OK)
    

    def get (self,request,trace_code) :
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        appendices = Appendices.objects.filter(plan=plan)
        if not appendices.exists() :
            return Response({'error': 'Appendices not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.AppendicesSerializer(appendices, many= True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def delete(self,request,trace_code):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        appendices = Appendices.objects.filter(id=int(trace_code))
        if not appendices.exists() :
            return Response({'error': 'Appendices not found'}, status=status.HTTP_404_NOT_FOUND)
        appendices.delete()
        return Response({'message':'succes'} , status=status.HTTP_200_OK)
    
# done
class DocumentationViewset(APIView) :
    def post (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        serializer = serializers.DocumentationSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'file' in request.FILES:
            serializer.uploaded_file = request.FILES['file']
        serializer.save(plan=plan)
        return Response ({'data' : serializer.data} , status=status.HTTP_200_OK)

    def get (self,request,trace_code) :

        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        ducumentation = DocumentationFiles.objects.filter(plan=plan)
        serializer = serializers.DocumentationSerializer(ducumentation, many= True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def delete(self,request,trace_code):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        appendices = DocumentationFiles.objects.filter(id=int(trace_code))
        if not appendices.exists() :
            return Response({'error': 'Appendices not found'}, status=status.HTTP_404_NOT_FOUND)
        appendices.delete()
        return Response({'message':'succses'} , status=status.HTTP_200_OK)
# done
class CommentAdminViewset (APIView) :

    def get (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()     
        plan = Plan.objects.filter(trace_code=trace_code).first()
        comment = Comment.objects.filter(plan=plan)
        if not comment:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommenttSerializer(comment , many=True)
        return Response ({'data' :serializer.data} , status=status.HTTP_200_OK)
    
    def patch (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()     
        comment = Comment.objects.filter(id=trace_code).first()
        if not comment:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommenttSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
   # done 
class CommentViewset (APIView):
    def post (self,request,trace_code):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()      
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        comment = Comment.objects.create(plan=plan , user=user)
        if not comment:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommenttSerializer(comment , data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



    def get (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_400_BAD_REQUEST)

        private_person = privatePerson.objects.filter(user=user).first()
        if not private_person:
            return Response({'error': 'privatePerson not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(plan=plan, status=True)
        if not comments.exists():
            return Response({'error': 'Comments not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommenttSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    




    def post(self, request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        data = request.data.copy()

        if 'remaining_date_to' in data : 
            try : 
                timestamp = abs(int(data['remaining_date_to'])/1000)
                print(timestamp)
                data['remaining_date_to'] = datetime.datetime.fromtimestamp(timestamp)
            except (ValueError, TypeError):
                return Response({'error': 'Invalid timestamp for remaining_date_to'}, status=status.HTTP_400_BAD_REQUEST)

        if 'remaining_from_to' in data : 
            try : 
                timestamp = abs(int(data['remaining_from_to'])/1000)
                data['remaining_from_to'] = datetime.datetime.fromtimestamp(timestamp)
            except (ValueError, TypeError):
                return Response({'error': 'Invalid timestamp for remaining_from_to'}, status=status.HTTP_400_BAD_REQUEST)


        serializer = serializers.PlanSerializer(data=data)
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

#done
class SendpicturePlanViewset(APIView) :

    def post (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        if 'picture' not in request.FILES:
            return Response({'error': 'No picture file was uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        picture = PicturePlan.objects.filter(plan=plan).first()
        if picture :
            picture.delete()
        picture = PicturePlan.objects.create(plan=plan , picture = request.FILES['picture'])
        picture.save()
        return Response({'success': True, 'message': 'Picture updated successfully'}, status=status.HTTP_200_OK)



    def get (self,request,trace_code) :
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        picture = PicturePlan.objects.filter(plan=plan).first()
        serializer = serializers.PicturePlanSerializer(picture)
        return Response(serializer.data, status=status.HTTP_200_OK)


# done
class PaymentDocument(APIView):
    def post(self,request,trace_code):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        if not request.data.get('amount'):
            return Response({'error': 'amount not found'}, status=status.HTTP_404_NOT_FOUND)
        amount = int(request.data.get('amount'))
        value = plan.unit_price * amount
        if not request.data.get('payment_id'):
            return Response({'error': 'payment_id not found'}, status=status.HTTP_404_NOT_FOUND)
        payment_id = request.data.get('payment_id')
        description = request.data.get('description',None)
        if not request.data.get('risk_statement'):
            return Response({'error': 'risk_statement not found'}, status=status.HTTP_404_NOT_FOUND)
        payment_id = request.data.get('risk_statement') == 'true'
        if not payment_id:
            return Response({'error': 'risk_statement not true'}, status=status.HTTP_404_NOT_FOUND)
        if not request.data.get('name_status'):
            return Response({'error': 'name_status not found'}, status=status.HTTP_404_NOT_FOUND)
        name_status = request.data.get('name_status') == 'true'
        if not request.FILES.get('picture'):
            return Response({'error': 'picture not found'}, status=status.HTTP_404_NOT_FOUND)
        picture = request.FILES.get('picture')
        payment = PaymentGateway(
            plan = plan,
            user = user,
            amount = amount,
            value = value,
            payment_id = payment_id,
            description = description,
            name_status = name_status,
            picture = picture
        )
        payment.save()
        return Response('success')
    

    def get(self,request,trace_code):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)

        admin = fun.decryptionadmin(Authorization)


        if not admin and not user:
            return Response({'error': 'Authorization not found'}, status=status.HTTP_401_UNAUTHORIZED)
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        


        if admin:
            admin = admin.first()
            payments = PaymentGateway.objects.filter(plan=plan)
            response = serializers.PaymentGatewaySerializer(payments,many=True)
            return Response(response.data, status=status.HTTP_200_OK)

        if user:
            user = user.first()
            payments = PaymentGateway.objects.filter(user=user, plan=plan)
            response = serializers.PaymentGatewaySerializer(payments,many=True)
            return Response(response.data, status=status.HTTP_200_OK)

        
    def patch (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        payments = PaymentGateway.objects.filter(plan=plan).first()
        if not payments :
            return Response({'error': 'payments not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.PaymentGatewaySerializer(payments, data = request.data , partial = True)
        if serializer.is_valid () :
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
# done
class ParticipantViewset(APIView) :
    def get(self, request,trace_code):
        Authorization = request.headers.get('Authorization')
        if  Authorization:
            admin = fun.decryptionadmin(Authorization)
            if not admin:
                return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
            admin = admin.first()
        else :
            admin= False
        plan = Plan.objects.filter(trace_code = trace_code).first()
        if not plan :
            return Response ({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        participant = PaymentGateway.objects.filter(plan=plan , status= True)
        if not participant :
            return Response ({'error': 'participant not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.PaymentGatewaySerializer(participant , many= True)
        names = []

        df = pd.DataFrame(serializer.data)
        df = df.drop(['picture', 'risk_statement', 'cart_number', 'code', 'description' , 'cart_hashpan'] , axis=1)
        for index, row in df.iterrows():
            
            if row['name_status'] == True or admin:
                name = get_name(row['user'])
            else : 
                name = 'نامشخص'
            names.append(name)
        df['name'] = names
        df= df.sort_values(by='user')
        df = df.to_dict('records')
              
        return Response (df, status=status.HTTP_200_OK)
    
# done
class InformationPlanViewset(APIView) :
    def post (self,request,trace_code):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first() 
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan :
            return Response({'error': 'Invalid plan status'}, status=status.HTTP_400_BAD_REQUEST)
        rate_of_return = request.data.get('rate_of_return')
        information , _ = InformationPlan.objects.update_or_create(plan=plan ,defaults={'rate_of_return' : rate_of_return} )
        serializer = serializers.InformationPlanSerializer(information)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self,request,trace_code) : 
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan :
            return Response({'error': 'Invalid plan status'}, status=status.HTTP_400_BAD_REQUEST)
        information = InformationPlan.objects.filter(plan=plan).first()
        serializer = serializers.InformationPlanSerializer(information)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EndOfFundraisingViewset(APIView) :
    def post (self,request,trace_code):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first() 
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan :
            return Response({'error': 'Invalid plan status'}, status=status.HTTP_400_BAD_REQUEST)
        amount_fundraising = plan.sum_of_funding_provided
        if amount_fundraising : 
            amount_fundraising = amount_fundraising / 4
        else:
            amount_fundraising = 0
        date = plan.project_start_date
        if isinstance(date, str):
            date =datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        for i in range (4) :
            format_date = date.strftime('%Y-%m-%d')           
            end_fundraising , _ = EndOfFundraising.objects.update_or_create(plan=plan,date=format_date,defaults={'amount': amount_fundraising,'type': 2})
            date = date + relativedelta(months=3)
            
        end_fundraising_total ,_ = EndOfFundraising.objects.update_or_create(plan=plan , date=date.strftime('%Y-%m-%d') , defaults={'amount': plan.sum_of_funding_provided,'type': 1})
        return Response ({'success': 'edn_fundraising'}, status=status.HTTP_200_OK)




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
        timestamp = request.data.get('timestamp', None)
        if not timestamp:
            return Response({'error': 'Timestamp is required'}, status=status.HTTP_400_BAD_REQUEST)
        timestamp = int(timestamp)/1000
        try:
            # تبدیل timestamp به datetime
            start_date = datetime.datetime.fromtimestamp(int(timestamp))
        except ValueError:
            return Response({'error': 'Invalid timestamp format'}, status=status.HTTP_400_BAD_REQUEST)



        # تعداد چک 
        number = int(plan.total_time / plan.payment_period)
        # مبلغ چک اصل پول
        amount_of_payment = plan.funded_amount
        # مبلغ هر چک سود 
        amount_of_profit  = (plan.funded_amount * int(plan.profit)) / number


        list = []
        
        # محاسبه تاریخ اولین چک سود: start_date + دوره پرداخت
        first_profit_date = start_date + relativedelta(months=plan.payment_period)

        # ایجاد چک‌های سود
        for i in range(number):
            # محاسبه تاریخ هر چک سود
            check_date = first_profit_date + relativedelta(months=i * plan.payment_period)
            
            # ایجاد شیء DocumentationRecieve برای چک سود
            documation = DocumentationRecieve.objects.create(plan=plan, type='2', amount=amount_of_profit) 
            
            # تبدیل تاریخ به جلالی برای نمایش
            jalali_date = JalaliDate(check_date)
            list.append({
                'type': documation.type,
                'amount': amount_of_profit,
                'date': str(jalali_date),
                'plan': documation.plan.id
            })

        # اضافه کردن یک چک برای اصل پول: start_date + total_time
        final_check_date = start_date + relativedelta(months=plan.total_time)  # آخرین چک
        documation = DocumentationRecieve.objects.create(plan=plan, type='1', amount=amount_of_payment)
        jalali_date = JalaliDate(final_check_date)
        list.append({
            'type': documation.type,
            'amount': amount_of_payment,
            'date': str(jalali_date),
            'plan': documation.plan.id
        })

        return Response({
            'message': f'{number+1} DocumentationRecieve created',
            'list': list
        }, status=status.HTTP_200_OK)
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


class RoadMapViewset(APIView) :
    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart = Cart.objects.filter(user=user).first()
        if not cart :
            return Response ({'error': 'Cart not found'}, status=status.HTTP_400_BAD_REQUEST)
        plan = Plan.objects.filter(id=id).first()
        if not plan :
            return Response ({'error': 'plan not found'}, status=status.HTTP_400_BAD_REQUEST)
        date_cart = cart.creat
        date_plan = None
        date_end_plan = None
        date_contract = None
        list = {
            'date_cart' : date_cart,
            'date_plan' : '2024-09-24T08:44:41.701688Z',
            'date_end_plan' : '2024-09-24T08:44:41.701688Z',
            'date_contract' : '2024-09-24T08:44:41.701688Z'
        }
            
        

        return Response({'data': list}, status=status.HTTP_200_OK)










