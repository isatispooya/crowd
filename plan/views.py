from .models import Plan , DocumentationFiles ,Appendices ,Comment  , Plans ,ListOfProjectBoardMembers,ProjectOwnerCompan , PaymentGateway ,PicturePlan , InformationPlan , EndOfFundraising ,ListOfProjectBigShareHolders
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from authentication import fun
from . import serializers
from accounting.models import Wallet
from investor.models import Cart
from authentication.models import privatePerson , User , accounts , LegalPerson , tradingCodes
import datetime
from persiantools.jdatetime import JalaliDate
from dateutil.relativedelta import relativedelta
import pandas as pd
from .CrowdfundingAPIService import CrowdfundingAPI , ProjectFinancingProvider
from dateutil.relativedelta import relativedelta
from datetime import timedelta




def get_name (uniqueIdentifier) :
    user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
    
    privateperson = privatePerson.objects.filter(user=user).first()
    if privateperson :
        first_name = privateperson.firstName
        last_name = privateperson.lastName
        full_name = first_name + ' ' + last_name
    else :
        legalperson = LegalPerson.objects.filter(user=user).first()
        full_name = legalperson.companyName

    return full_name
        

def get_fname (uniqueIdentifier) :
    user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
    privateperson = privatePerson.objects.filter(user=user).first()
    first_name = privateperson.firstName
    return first_name


def get_lname (uniqueIdentifier) :
    user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
    privateperson = privatePerson.objects.filter(user=user).first()
    last_name = privateperson.lastName
    return last_name


def get_economi_code (uniqueIdentifier) :
    user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
    economi_code = tradingCodes.objects.filter(user=user).first()
    economi_code = economi_code.code
    return economi_code


def get_account_number(uniqueIdentifier) :
    user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
    user_account = accounts.objects.filter(user=user).first()
    sheba = user_account.sheba
    return sheba


def get_mobile_number(uniqueIdentifier) :
    user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
    mobile = user.mobile
    if mobile[:2] == '98':
      mobile = '0'+ mobile[2:]
    return mobile


def check_legal_person(uniqueIdentifier) :
    user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
    legal_person = LegalPerson.objects.filter(user=user).first()
    if legal_person:
        return True
    return False

# done
# detial + information
class PlanViewset(APIView):
    def get(self, request, trace_code):
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan:
            return Response({'message': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        plan_serializer = serializers.PlanSerializer(plan)
        
        board_members = ListOfProjectBoardMembers.objects.filter(plan=plan)
        if board_members.exists():
            board_members_serializer = serializers.ListOfProjectBoardMembersSerializer(board_members, many=True)
        shareholder = ListOfProjectBigShareHolders.objects.filter(plan=plan)
        if shareholder.exists():
            shareholder_serializer = serializers.ListOfProjectBigShareHoldersSerializer(shareholder, many=True)
        response_data = {
            'plan': plan_serializer.data ,
            'board_member' : board_members_serializer.data , 
            'shareholder' : shareholder_serializer.data

        }
        information = InformationPlan.objects.filter(plan=plan).first()
        if information:
            information_serializer = serializers.InformationPlanSerializer(information)
            response_data['information_complete'] = information_serializer.data
        
        return Response(response_data, status=status.HTTP_200_OK)
        

# done
# list + information
# update
class PlansViewset(APIView):
    def get(self, request):
        plans = Plan.objects.all()
        result = []

        for plan in plans:
            information = InformationPlan.objects.filter(plan=plan).first()
            board_members = ListOfProjectBoardMembers.objects.filter(plan=plan)  
            shareholder = ListOfProjectBigShareHolders.objects.filter(plan=plan)  
            plan_serializer = serializers.PlanSerializer(plan)
            board_members_serializer = serializers.ListOfProjectBoardMembersSerializer(board_members, many=True)
            shareholder_serializer = serializers.ListOfProjectBigShareHoldersSerializer(shareholder, many=True)
            data = {
                'plan': plan_serializer.data,
                'board_members': board_members_serializer.data , 
                'shareholder': shareholder_serializer.data  
            }
            if information:
                information_serializer =serializers.InformationPlanSerializer(information)
                data['information_complete'] = information_serializer.data
            result.append(data)

        return Response(result, status=status.HTTP_200_OK)
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

            if len(plan_detail.get('List Of Project Big Share Holders', [])) > 0:
                for j in plan_detail['List Of Project Big Share Holders']:
                    List_of_project_big_shareholder, _ = ListOfProjectBigShareHolders.objects.update_or_create(
                        plan=plan,
                        national_id=j.get('National ID', None),
                        defaults={
                            'shareholder_type': j.get('Shareholder Type', None),
                            'first_name': j.get('First Name / Company Name', None),
                            'last_name': j.get('Last Name / CEO Name', None),
                            'share_percent': j.get('Share Percent', None),
                            
                        }
                    )



            if len(plan_detail.get('List Of Project Board Members', [])) > 0:
                for j in plan_detail['List Of Project Board Members']:
                    List_of_project_board_members, _ = ListOfProjectBoardMembers.objects.update_or_create(
                        plan=plan,
                        national_id=j.get('National ID', None),
                        defaults={
                            'mobile_number': j.get('mobile_number', None),
                            'email_address': j.get('email_address', None),
                            'organization_post_id': j.get('Organization Post ID', None),
                            'is_agent_from_company': j.get('Is Agent from a Company', None),
                            'first_name': j.get('First Name', None),
                            'last_name': j.get('Last Name', None),
                            'company_national_id': j.get('Company National ID', None),
                            'company_name': j.get('Company Name', None),
                            'mobile_number': j.get('Mobile Number', None),
                            'email_address': j.get('Email Address', None),
                            'organization_post_description': j.get('Organization Post Description', None),
                            
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
        if not plan:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(plan=plan)
        for comment in comments:
            if comment.answer is None or comment.answer == '':
                comment.answer = 'منتظر پاسخ'
                comment.save()  

        serializer = serializers.CommenttSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
        data = request.data
        data['answer'] = data.get('answer', 'منتظر پاسخ') or 'منتظر پاسخ'
        serializer = serializers.CommenttSerializer(comment, data=data, partial=True)
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
        data = request.data
        comment = Comment.objects.create(plan=plan , user=user)
        if not comment:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        if not data.get('answer'):
            data['answer'] = 'منتظر پاسخ'
        serializer = serializers.CommenttSerializer(comment , data=data)
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
            df = pd.DataFrame(response.data)
            if len(df)==0:
                return Response([], status=status.HTTP_200_OK)
            df['fulname'] = [get_name(x) for x in df['user']]
            df = df.to_dict('records')
            return Response(df, status=status.HTTP_200_OK)
        
        if user:
            user = user.first()
            payments = PaymentGateway.objects.filter(user=user, plan=plan)
            response = serializers.PaymentGatewaySerializer(payments,many=True)
            df = pd.DataFrame(response.data)
            if len(df)==0:
                return Response([], status=status.HTTP_200_OK)
            df['fulname'] = [get_name(x) for x in df['user']]
            df = df.to_dict('records')
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
        payment_id = request.data.get('id')
        payments = PaymentGateway.objects.filter(plan=plan,id = payment_id).first()
        if not payments :
            return Response({'error': 'payments not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data

        serializer = serializers.PaymentGatewaySerializer(payments, data = request.data , partial = True)
        if serializer.is_valid () :
            serializer.save()
        payment = PaymentGateway.objects.filter(plan=plan ,id = payment_id)
        value = 0
        for i in payment : 
            if i.status == True:
               value += i.value
        information = InformationPlan.objects.filter(plan=plan ).first()
        information.amount_collected_now = value
        information.save()
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
        status_second = request.data.get('status_second')
        status_show = request.data.get('status_show')
        if status_second not in ['1' , '2','3' , '4' , '5'] :
            status_second = '1'
        information , _ = InformationPlan.objects.update_or_create(plan=plan ,defaults={'rate_of_return' : rate_of_return , 'status_second': status_second, 'status_show' :status_show } )
        serializer = serializers.InformationPlanSerializer(information)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self,request,trace_code) : 
        plan = Plan.objects.filter(trace_code=trace_code).first()
        if not plan :
            return Response({'error': 'Invalid plan status'}, status=status.HTTP_400_BAD_REQUEST)
        information = InformationPlan.objects.filter(plan=plan).first()
        serializer = serializers.InformationPlanSerializer(information)
        return Response(serializer.data, status=status.HTTP_200_OK)



#done
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
        all_end_fundraising = []
        end_fundraising = EndOfFundraising.objects.filter(plan=plan)
        if not end_fundraising :
            return Response({'error': 'end of fundraising not found'}, status=status.HTTP_404_NOT_FOUND)
        EndOfFundraising.objects.filter(plan=plan).delete()
        data = request.data 
        for item in data:
            fundraising_id = item.get('id')

            if fundraising_id is None:
                return Response({'error': 'ID is required for each fundraising item'}, status=status.HTTP_400_BAD_REQUEST)

            EndOfFundraising.objects.create(
                id=fundraising_id,
                amount=item.get('amount', 0),  
                type=item.get('type', ''),
                date=item.get('date', None),
                date_capitalization=item.get('date_capitalization', None),
                plan=plan
            )

        all_end_fundraising = EndOfFundraising.objects.filter(plan=plan)
        serializer = serializers.EndOfFundraisingSerializer(all_end_fundraising, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    






    def get(self,request,trace_code) : 
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
        end_fundraising = EndOfFundraising.objects.filter(plan=plan)
        if end_fundraising.exists():
            serializer = serializers.EndOfFundraisingSerializer(end_fundraising , many = True).data
            return Response(serializer, status=status.HTTP_200_OK)
        if not end_fundraising.exists():
            all_end_fundraising = []
            amount_fundraising = plan.sum_of_funding_provided
            if amount_fundraising:
                amount_fundraising = amount_fundraising / 4
            else:
                amount_fundraising = 0

            date = plan.project_start_date
            if isinstance(date, str):
                date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

            for i in range(4):
                format_date = date.strftime('%Y-%m-%d')
                date_capitalization = (date - timedelta(days=5)).date()

                end_fundraising = EndOfFundraising.objects.create(
                    plan=plan,
                    date=format_date,
                    amount=amount_fundraising,
                    type=2,
                    date_capitalization=date_capitalization
                )
                date = date + relativedelta(months=3)
                all_end_fundraising.append(end_fundraising)

            date_end = plan.project_end_date
            date_end = datetime.datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%S')
            date_capitalization_end = (date_end - timedelta(days=5)).date()

            end_fundraising_total = EndOfFundraising.objects.create(
                plan=plan,
                date=date_end.strftime('%Y-%m-%d'),
                amount=plan.sum_of_funding_provided,
                type=1,
                date_capitalization=date_capitalization_end
            )
            
            all_end_fundraising.append(end_fundraising_total)
            serializer = serializers.EndOfFundraisingSerializer(all_end_fundraising, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# done
class SendPaymentToFarabours(APIView) :
    def post (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first() 
        data = request.data
        financing_provider = ProjectFinancingProvider(
            projectID=data.get('projectID'),
            nationalID=data.get('nationalID'),
            isLegal=data.get('isLegal'),
            firstName=data.get('firstName'),
            lastNameOrCompanyName=data.get('lastNameOrCompanyName'),
            providedFinancePrice=data.get('providedFinancePrice'),
            bourseCode=data.get('bourseCode'),
            paymentDate=data.get('paymentDate'),
            shebaBankAccountNumber=data.get('shebaBankAccountNumber'),
            mobileNumber=data.get('mobileNumber'),
            bankTrackingNumber=data.get('bankTrackingNumber'),
        )
        return Response (status=status.HTTP_200_OK)




# done
class SendParticipationCertificateToFaraboursViewset(APIView):
    def post(self, request, trace_code):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        plan = Plan.objects.filter(trace_code = trace_code).first()
        if not plan :
            return Response({'error': 'plan not found '}, status=status.HTTP_400_BAD_REQUEST)
        payment = PaymentGateway.objects.filter(plan=plan , status = True , send_farabours = False)
        if not payment :
            return Response({'error': 'payment not found'}, status=status.HTTP_400_BAD_REQUEST)

        payment_serializer = serializers.PaymentGatewaySerializer(payment , many = True)
        payment_serializer = payment_serializer.data
        api_farabours = CrowdfundingAPI()
        for i in payment_serializer :
            uniqueIdentifier = i['user']
            user_obj = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
            print('-'*55)
            print(get_account_number (uniqueIdentifier))
            print('+'*55)
            if user_obj is not None:
                user_fname = get_fname(uniqueIdentifier)
                user_lname = get_lname(uniqueIdentifier)
                account_number = get_account_number (uniqueIdentifier)
                mobile = get_mobile_number (uniqueIdentifier)
                bourse_code = get_economi_code (uniqueIdentifier)
                is_legal = check_legal_person (uniqueIdentifier)
            provided_finance_price = i['value']
            payment_date = i['create_date']
            bank_tracking_number = i['payment_id']

            project_finance = ProjectFinancingProvider(
                projectID = trace_code,
                nationalID = uniqueIdentifier ,
                isLegal = is_legal,
                firstName = user_fname ,
                lastNameOrCompanyName = user_lname,
                providedFinancePrice = provided_finance_price,
                bourseCode = bourse_code,
                paymentDate = payment_date,
                shebaBankAccountNumber = account_number,
                mobileNumber = mobile,
                bankTrackingNumber = bank_tracking_number,
            )
            # api = api_farabours.register_financing(project_finance)
        for j in payment :
            j.send_farabours = True
            j.save()
            
            
        return Response(True, status=status.HTTP_200_OK)




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









