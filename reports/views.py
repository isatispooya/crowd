from django.shortcuts import render
from plan.models import Plan , ProgressReport , AuditReport
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from authentication import fun
from . import serializers
from plan import serializers
from plan.CrowdfundingAPIService import CrowdfundingAPI 


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
