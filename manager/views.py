from django.shortcuts import render
from .models import Manager ,  Resume , Validation , Shareholder
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from authentication import fun
from . import serializers
from investor import models

class ManagerViewset(APIView) :
    def post (self , request , id ):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        managers_data = request.data.get('managers', [])
        
        for manager_data in managers_data:
            serializer = serializers.ManagerSerializer(data={**manager_data, 'cart': cart.id})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(cart=cart)
        serializer = serializers.CartWithManagersSerializer(cart)
        return Response({'message': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    

    def get (self,request , id):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        managers = Manager.objects.filter(cart=cart)
        serializer = serializers.ManagerSerializer(managers, many=True)
        return Response({'message': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    


    def patch (self,request , id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        if id is None:
            return Response({'error': 'Manager ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            manager = Manager.objects.get(id=id)
        except Manager.DoesNotExist:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        manager.delete()
        request.data['id'] = id
        serializer = serializers.ManagerSerializer(data=request.data)
 
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'message': 'Manager updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


class ManagerAdminViewset(APIView):
    def get (self,request,id):
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
        
        managers = Manager.objects.filter(cart=cart)
        serializer = serializers.ManagerSerializer(managers, many=True)
        return Response({'message': True ,  'data': serializer.data }, status=status.HTTP_200_OK)

    def patch (self,request , id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        if id is None:
            return Response({'error': 'Manager ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            manager = Manager.objects.get(id=id)
        except Manager.DoesNotExist:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        manager.delete()
        request.data['id'] = id
        serializer = serializers.ManagerSerializer(data=request.data)
 
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'message': 'Manager updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)



class ResumeViewset(APIView):
    def post (self,request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        
        if not request.FILES:
            return Response({'error': 'No file was uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        national_code = list(request.FILES.keys())[0]
        resume_file = request.FILES[national_code]
        manager = Manager.objects.filter(national_code=national_code).first()
        if not manager:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)

        resume = Resume(file=resume_file, manager=manager)
        resume.save()
        return Response({'message': True }, status=status.HTTP_200_OK)
    


    def get (self,request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        national_code = request.query_params.get('national_code')

        if not national_code:
            return Response({'error': 'National code is missing'}, status=status.HTTP_400_BAD_REQUEST)
        manager = Manager.objects.filter(national_code=national_code).first()

        if not manager:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        resumes = Resume.objects.filter(manager=manager)

        if not resumes.exists():
            return Response({'error': 'No resumes found for this manager'}, status=status.HTTP_404_NOT_FOUND)
        resume_files = [{'file': resume.file.url} for resume in resumes]

        return Response({'manager': manager.national_code, 'resumes': resume_files}, status=status.HTTP_200_OK)


    def patch (self,request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        national_code = request.query_params.get('national_code')
        if not national_code:
            return Response({'error': 'National code is missing'}, status=status.HTTP_400_BAD_REQUEST)
        manager = Manager.objects.filter(national_code=national_code).first()
        if not manager:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)

        resume = Resume.objects.filter(manager=manager).first()     
        if resume:
            resume.delete()   

        if not request.FILES:
            return Response({'error': 'No file was uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        national_code = list(request.FILES.keys())[0]
        resume_file = request.FILES[national_code]
        manager = Manager.objects.filter(national_code=national_code).first()
        if not manager:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)

        resume = Resume(file=resume_file, manager=manager)
        resume.save()
        print(resume)
        return Response({'message': True }, status=status.HTTP_200_OK)




class ResumeAdminViewset(APIView) :
    def get(self, request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        national_code = request.query_params.get('national_code')

        if not national_code:
            return Response({'error': 'National code is missing'}, status=status.HTTP_400_BAD_REQUEST)
        manager = Manager.objects.filter(national_code=national_code).first()

        if not manager:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        resumes = Resume.objects.filter(manager=manager)

        if not resumes.exists():
            return Response({'error': 'No resumes found for this manager'}, status=status.HTTP_404_NOT_FOUND)
        resume_files = [{'file': resume.file.url} for resume in resumes]

        return Response({'manager': manager.national_code, 'resumes': resume_files}, status=status.HTTP_200_OK)


    def patch(self,request) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first() 
        national_code = request.query_params.get('national_code')
        if not national_code:
            return Response({'error': 'National code is missing'}, status=status.HTTP_400_BAD_REQUEST)
        manager = Manager.objects.filter(national_code=national_code).first()
        if not manager:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)

        resume = Resume.objects.filter(manager=manager).first()     
        if resume:
            resume.delete()   

        if not request.FILES:
            return Response({'error': 'No file was uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        national_code = list(request.FILES.keys())[0]
        resume_file = request.FILES[national_code]
        manager = Manager.objects.filter(national_code=national_code).first()
        if not manager:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)

        resume = Resume(file=resume_file, manager=manager)
        resume.save()
        print(resume)
        return Response({'message': True }, status=status.HTTP_200_OK)

