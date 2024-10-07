from django.shortcuts import render
from plan.models import Plan , PaymentGateway ,InformationPlan ,EndOfFundraising
from authentication.models import User , accounts , privatePerson
from investor.models import Cart
from .models import ProgressReport , AuditReport
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from authentication import fun
from . import serializers
from plan import serializers
from plan.CrowdfundingAPIService import CrowdfundingAPI 
from django.utils import timezone
from django.db.models import Sum
import pandas as pd
from authentication.serializers import accountsSerializer , privatePersonSerializer

# گزارش پیشرفت پروژه
# done
class ProgressReportViewset(APIView) :
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
        serializer = serializers.ProgressReportSerializer(data=data)
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
        progres_report = ProgressReport.objects.filter(plan=plan)
        if not progres_report.exists() :
            return Response({'error': 'progres report not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ProgressReportSerializer(progres_report, many= True)
        return Response(serializer.data , status=status.HTTP_200_OK)



    def delete (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        progres_report = ProgressReport.objects.filter(id=int(trace_code))
        if not progres_report.exists() :
            return Response({'error': 'progres report not found'}, status=status.HTTP_404_NOT_FOUND)
        progres_report.delete()
        return Response({'message':'succes'} , status=status.HTTP_200_OK)


# گزارش حسابررسی
# done
class AuditReportViewset(APIView) :
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
        serializer = serializers.AuditReportSerializer(data=data)
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
        audit_report = AuditReport.objects.filter(plan=plan)
        if not audit_report.exists() :
            return Response({'error': 'audit report not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.AuditReportSerializer(audit_report, many= True)
        return Response(serializer.data , status=status.HTTP_200_OK)



    def delete (self,request,trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        audit_report = AuditReport.objects.filter(id=int(trace_code))
        if not audit_report.exists() :
            return Response({'error': 'audit report not found'}, status=status.HTTP_404_NOT_FOUND)
        audit_report.delete()
        return Response({'message':'succes'} , status=status.HTTP_200_OK)


# گزارش مشارکت کننده ها
# done
class ParticipationReportViewset(APIView) :
    def get (self , request, trace_code) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        plan = Plan.objects.filter(trace_code=trace_code).first()
        national_id =   user.uniqueIdentifier
        crowd_api = CrowdfundingAPI()
        participation = crowd_api.get_project_participation_report(plan.id , national_id)
        return Response (participation, status=status.HTTP_200_OK)


# داشبورد ادمین 
# done
class DashBoardAdminViewset (APIView) : 
    def get (self , request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()

        plan_all = Plan.objects.all().count()
        now = timezone.now()
        expire_plan = Plan.objects.filter(suggested_underwriting_end_date__lt=now).count()
        current_date = timezone.now().date()
        active_plan = Plan.objects.filter( suggested_underwriting_start_date__lte=current_date,suggested_underwriting_end_date__gte=current_date).count()
        cart_all = Cart.objects.all().count()
        expire_cart = Cart.objects.filter(finish_cart = True).count()
        active_cart = Cart.objects.filter(finish_cart = False).count()
        return Response ({'all plan':plan_all ,'expire plan' : expire_plan , 'active plan' : active_plan , 'all cart' : cart_all, 'expire cart' : expire_cart , 'active cart' : active_cart} , status=status.HTTP_200_OK)
   


# داشبورد مشتری 
# done
class DashBoardUserViewset(APIView) :
    def get (self,request) : 
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        plan_all = Plan.objects.all().count()
        current_date = timezone.now().date()
        active_plan = Plan.objects.filter( suggested_underwriting_start_date__lte=current_date,suggested_underwriting_end_date__gte=current_date).count()
        payments = PaymentGateway.objects.filter(user=user).values('plan').distinct()
        payments_count = payments.count()
        total_value = PaymentGateway.objects.filter(user=user).aggregate(total_value_sum=Sum('value'))['total_value_sum']
        if total_value is None:
            total_value = 0

        total_rate_of_return = InformationPlan.objects.filter(plan__in=payments).aggregate(total_rate_sum=Sum('rate_of_return'))['total_rate_sum']        
        if total_rate_of_return is None:
            total_rate_of_return = 0
        return Response ({'all plan' :plan_all , 'active plan' : active_plan , 'participant plan' :payments_count , 'total value' : total_value , 'all rate of return' :  total_rate_of_return }, status=status.HTTP_200_OK)
    
# گزارش سود دهی ادمین
class ProfitabilityReportViewSet(APIView) :
    def get(self,request,trace_code):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        if not trace_code:
            return Response({'error': 'trace_code not found'}, status=status.HTTP_400_BAD_REQUEST)
        plan =Plan.objects.filter(trace_code=trace_code)
        if not plan.exists():
            return Response({'error': 'plan not found'}, status=status.HTTP_404_NOT_FOUND)
        plan =plan.first()
        end_plan = EndOfFundraising.objects.filter(plan=plan)
        if not end_plan.exists():
            return Response({'error': 'plan not end'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        end_plan = serializers.EndOfFundraisingSerializer(end_plan,many=True)
        user_peyment = PaymentGateway.objects.filter(plan=plan,status=True)
        if not user_peyment.exists():
            return Response({'error': 'payment not fund'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        user_peyment = serializers.PaymentGatewaySerializer(user_peyment,many=True)

        user = user_peyment.data[0]['user']
        user = User.objects.filter(uniqueIdentifier = user).first()
        if user is None:
            return Response({'error': 'user not fund'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user_account = accounts.objects.filter(user=user).first()
        if user_account is None:
            return Response({'error': 'user account not found'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        user_account_serializer = accountsSerializer(user_account)
        account_number = user_account_serializer.data.get('accountNumber')

        user_privetperson = privatePerson.objects.filter(user=user).first()
        user_privetperson_serializer = privatePersonSerializer(user_privetperson)
        user_fname = user_privetperson_serializer.data.get('firstName')
        user_lname = user_privetperson_serializer.data.get('lastName')
        user_name = user_fname + '' + user_lname

        information = InformationPlan.objects.filter(plan=plan)
        if not information.exists():
            return Response({'error': 'information not fund'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        information_serializer = serializers.InformationPlanSerializer(information.first())

        rate_of_return = ((information_serializer.data['rate_of_return'])/100) /365
        df = pd.DataFrame(user_peyment.data)[['user','amount','value']].groupby(by=['user']).sum().reset_index()
        df ['account_number'] = account_number
        df ['user_name'] = user_name

        pey_df = pd.DataFrame(end_plan.data).sort_values('date')
        start_project = plan.project_start_date
        pey_df['date'] = pd.to_datetime(pey_df['date'])
        pey_df['date_diff'] = (pey_df['date'] - pd.to_datetime(start_project))
        pey_df['date_diff'] = [x.days for x in  pey_df['date_diff']]
        pey_df['profit'] = pey_df['date_diff'] * rate_of_return 
        pey_df = pey_df.sort_values('date_diff')
        qest = 1
        for i in pey_df.index : 
            if pey_df['type'][i] == '2' :
                df[f'profit{qest}'] = pey_df['profit'][i]
                df[f'value{qest}'] = pey_df['profit'][i] * df['value']
                df[f'date{qest}'] = pey_df['date'][i]
                qest += 1
            else :
                df['date_base'] = pey_df['date']
        
        print(df)
        df = df.to_dict('records')
        return Response(df, status=status.HTTP_200_OK)