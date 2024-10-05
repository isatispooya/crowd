from django.shortcuts import render
from plan.models import Plan , PaymentGateway ,InformationPlan ,EndOfFundraising
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
    def get(self,request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        now = timezone.now()
        expire_plan = Plan.objects.filter(suggested_underwriting_end_date__lt=now)
        end_fundraising = EndOfFundraising.objects.filter(plan__in = expire_plan)
        if not end_fundraising :
            return Response({'error': 'this plan has not end of fundraising'}, status=status.HTTP_400_BAD_REQUEST)
        # df = pd.DataFrame(columns=['نام کاربر', 'کدملی', 'موبایل', 'طرح', 'جمع کل سرمایه گذاری', 
        #                            'مبلغ قسط 1', 'مبلغ قسط 2', 'مبلغ قسط 3', 'مبلغ قسط 4',
        #                            'تاریخ پرداخت قسط 1', 'تاریخ پرداخت قسط 2', 'تاریخ پرداخت قسط 3', 'تاریخ پرداخت قسط 4', 
        #                            'تاریخ واریز سود', 'تاریخ پرداخت اصل پول', 'پرداخت اصل پول'])
        # data_list = [] 
        # for entry in end_fundraising:
        #     plan_name = entry.plan.persian_name  
        #     data_list.append({
        #         'نام کاربر': 'نام کاربر نمونه',  # باید از مدل مرتبط گرفته شود
        #         'کدملی': '1234567890',  # باید از مدل مرتبط گرفته شود
        #         'موبایل': '09123456789',  # باید از مدل مرتبط گرفته شود
        #         'طرح': plan_name,  # نام طرح از مدل Plan
        #         'جمع کل سرمایه گذاری': 'مقدار نمونه',  # باید از مدل مرتبط گرفته شود
        #         'مبلغ قسط 1': 'مقدار نمونه',  # باید از مدل مرتبط گرفته شود
        #         'مبلغ قسط 2': 'مقدار نمونه',  # باید از مدل مرتبط گرفته شود
        #         'مبلغ قسط 3': 'مقدار نمونه',  # باید از مدل مرتبط گرفته شود
        #         'مبلغ قسط 4': 'مقدار نمونه',  # باید از مدل مرتبط گرفته شود
        #         'تاریخ پرداخت قسط 1': 'تاریخ نمونه',  # باید از مدل مرتبط گرفته شود
        #         'تاریخ پرداخت قسط 2': 'تاریخ نمونه',  # باید از مدل مرتبط گرفته شود
        #         'تاریخ پرداخت قسط 3': 'تاریخ نمونه',  # باید از مدل مرتبط گرفته شود
        #         'تاریخ پرداخت قسط 4': 'تاریخ نمونه',  # باید از مدل مرتبط گرفته شود
        #         'تاریخ واریز سود': 'تاریخ نمونه',  # باید از مدل مرتبط گرفته شود
        #         'تاریخ پرداخت اصل پول': 'تاریخ نمونه',  # باید از مدل مرتبط گرفته شود
        #         'پرداخت اصل پول': 'وضعیت نمونه'  # باید از مدل مرتبط گرفته شود
        #     }, ignore_index=True)
        # df = pd.concat([df, pd.DataFrame(data_list)], ignore_index=True)
        # print(df)
        return Response({'success':True}, status=status.HTTP_200_OK)
    
