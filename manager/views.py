from django.shortcuts import render
from .models import Manager ,  Resume , Validation , Shareholder , History
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
        manager = Manager.objects.filter(cart=cart)
        if manager :
            manager.delete()
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

    def post (self , request , id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        if id is None:
            return Response({'error': 'Manager ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
        cart =  models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        manager = Manager.objects.filter(cart=cart)
        if manager :
            manager.delete()
        managers_data = request.data.get('managers', [])
        for manager_data in managers_data:
            serializer = serializers.ManagerSerializer(data={**manager_data, 'cart': cart.id})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(cart=cart)
        serializer = serializers.CartWithManagersSerializer(cart)
        return Response({'message': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    





class ResumeViewset(APIView):
    def post (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        
        if not request.FILES:
            return Response({'error': 'No file was uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        cart = models.Cart.objects.filter(id=id)
        if len(cart) == 0:
            return Response({'error': 'not found cart'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart = cart.first()

        for i in request.FILES:
            manager = Manager.objects.filter(national_code=i,cart=cart)
            if len(manager)==0:
                return Response({'error': 'not found managment'}, status=status.HTTP_400_BAD_REQUEST)
            manager = manager.first()
            resume = Resume(file=request.FILES[i],manager=manager)
            resume.save()
        return Response({'message': True }, status=status.HTTP_200_OK)
    


    def get (self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart = models.Cart.objects.filter(user=user,id=id)
        if not cart.exists():
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        cart = cart.first()
        manager = Manager.objects.filter(cart=cart)
        if not manager.exists():
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        resume_list = []
        for i in manager:
            resume = Resume.objects.filter(manager=i)
            national_code = i.national_code
            name = i.name
            lock = False
            file = None
            if resume.exists():
              resume = resume.first()
              resume = serializers.ResumeSerializer(resume).data
              lock = resume['lock']
              file = resume['file']
              
              
            resume_list.append({'national_code': national_code,'lock': lock,'file': file,'name':name})

        return Response({'manager': resume_list}, status=status.HTTP_200_OK)


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
        return Response({'message': True }, status=status.HTTP_200_OK)




class ResumeAdminViewset(APIView) :
    def get(self, request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = models.Cart.objects.filter(id=id)
        if not cart.exists():
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        cart = cart.first()
        manager = Manager.objects.filter(cart=cart)
        if not manager.exists():
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        resume_list = []
        for i in manager:
            resume = Resume.objects.filter(manager=i)
            national_code = i.national_code
            name = i.name
            lock = False
            file = None
            if resume.exists():
              resume = resume.first()
              resume = serializers.ResumeSerializer(resume).data
              lock = resume['lock']
              file = resume['file']
              
              
            resume_list.append({'national_code': national_code,'lock': lock,'file': file,'name':name})

        return Response({'manager': resume_list}, status=status.HTTP_200_OK)

    def post(self, request, id):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()

        if not request.FILES:
            return Response({'error': 'No file was uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart = models.Cart.objects.filter(id=id)
        if len(cart) == 0:
            return Response({'error': 'Not found cart'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart = cart.first()

        for i in request.FILES:
            manager = Manager.objects.filter(national_code=i, cart=cart)
            if len(manager) == 0:
                return Response({'error': 'Not found management'}, status=status.HTTP_400_BAD_REQUEST)
            
            manager = manager.first()

            existing_resumes = Resume.objects.filter(manager=manager)
            if existing_resumes.exists():
                existing_resumes.delete()

            resume = Resume(file=request.FILES[i], manager=manager)
            resume.save()

        return Response({'message': True}, status=status.HTTP_200_OK)
class ShareholderViewset(APIView):
    def post(self, request,id):
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
        shareholder = Shareholder.objects.filter(cart=cart)
        if shareholder :
            shareholder.delete()

        shareholder  = request.data.get('shareholder', [])
        all_serialized = [] 

        for shareholder in shareholder:
            serializer = serializers.ShareholderSerializer(data={**shareholder, 'cart': cart.id})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(cart=cart)
            all_serialized.append(serializer.data)  # اضافه کردن داده‌های سریالایز شده به لیست

        return Response({'message': True, 'data': all_serialized}, status=status.HTTP_200_OK)




    def get (self, request , id) :
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
        
        shareholder = Shareholder.objects.filter(cart=cart)
        serializer = serializers.ShareholderSerializer(shareholder, many=True)
        return Response({'message': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    

class ShareholderAdminViewset(APIView) :
    def get (self, request, id) :
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
        
        shareholder = Shareholder.objects.filter(cart=cart)
        serializer = serializers.ShareholderSerializer(shareholder, many=True)
        return Response({'message': True ,  'data': serializer.data }, status=status.HTTP_200_OK)

    
    def post(self,request,id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        if id is None:
            return Response({'error': 'Manager ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        shareholder = Shareholder.objects.filter(cart=cart)
        if shareholder :
            shareholder.delete()

        shareholder  = request.data.get('shareholder', [])
        all_serialized = [] 

        for shareholder in shareholder:
            serializer = serializers.ShareholderSerializer(data={**shareholder, 'cart': cart.id})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(cart=cart)
            all_serialized.append(serializer.data)   
        return Response({'message': True, 'data': all_serialized}, status=status.HTTP_200_OK)

        



class ValidationViewset (APIView) :
    def post (self, request, id) :
        try:
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
            if not request.FILES:
                return Response({'error': 'No files were uploaded'}, status=status.HTTP_400_BAD_REQUEST)
            file_validation = request.FILES.get('file_validation')
            if not file_validation:
                return Response({'error': 'File validation is missing'}, status=status.HTTP_400_BAD_REQUEST)
            
            manager_list = []

            for i in request.FILES:
                if i == 'file_validation':   
                    continue
                manager = Manager.objects.filter(national_code=i, cart=cart )
                if len(manager) == 0:
                    return Response({'error': f'Manager with national code {i} not found for this cart'}, status=status.HTTP_404_NOT_FOUND)

                manager = manager.first()

                existing_validation = Validation.objects.create(file_manager=request.FILES[i], manager=manager, cart=cart)
                existing_validation.save()

                manager_list.append({
                    'national_code': manager.national_code,
                    'name': manager.name,
                    'file_manager': existing_validation.file_manager.url if existing_validation.file_manager else None,
                })
            validation = Validation.objects.create(file_validation=file_validation, cart=cart , manager = manager)

            print(validation)

            validation.save()
            response_data = {
                'file_validation': validation.file_validation.url if validation.file_validation else None,
                'managers': manager_list
            }



            return Response({'data': response_data}, status=status.HTTP_200_OK)
        except Exception as e:
                print(f"An error occurred: {e}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request, id):
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
        
        manager = Manager.objects.filter(cart=cart)
        if not manager.exists():
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        
        manager_list = []
        
        validation = Validation.objects.filter(cart=cart).first()
        file_validation = None
        if validation:
            file_validation = validation.file_validation.url if validation.file_validation else None

        for i in manager:
            validation_manager = Validation.objects.filter(manager=i)
            national_code = i.national_code
            name = i.name
            file_manager = None

            if validation_manager.exists():
                validation_instance = validation_manager.first()
                file_manager = validation_instance.file_manager.url if validation_instance.file_manager else None

            manager_list.append({
                'national_code': national_code,
                'file_manager': file_manager,
                'name': name
            })

        return Response({
            'file_validation': file_validation,
            'managers': manager_list
        }, status=status.HTTP_200_OK)


class ValidationAdminViewset (APIView) :
    def post (self, request, id) :
        try :
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
            if not request.FILES:
                return Response({'error': 'No files were uploaded'}, status=status.HTTP_400_BAD_REQUEST)
            file_validation = request.FILES.get('file_validation')
            if not file_validation:
                return Response({'error': 'File validation is missing'}, status=status.HTTP_400_BAD_REQUEST)
            
            manager_list = []

            for i in request.FILES:
                if i == 'file_validation':   
                    continue
                manager = Manager.objects.filter(national_code=i, cart=cart )
                if len(manager) == 0:
                    return Response({'error': f'Manager with national code {i} not found for this cart'}, status=status.HTTP_404_NOT_FOUND)

                manager = manager.first()

                existing_validation = Validation.objects.create(file_manager=request.FILES[i], manager=manager, cart=cart)
                existing_validation.save()

                manager_list.append({
                    'national_code': manager.national_code,
                    'name': manager.name,
                    'file_manager': existing_validation.file_manager.url if existing_validation.file_manager else None,
                })
            validation = Validation.objects.create(file_validation=file_validation, cart=cart , manager = manager)

            print(validation)

            validation.save()
            response_data = {
                'file_validation': validation.file_validation.url if validation.file_validation else None,
                'managers': manager_list
            }
            return Response({'data': response_data}, status=status.HTTP_200_OK)
        except Exception as e:
                print(f"An error occurred: {e}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get (self, request, id) :
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
        
        manager = Manager.objects.filter(cart=cart)
        if not manager.exists():
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        
        manager_list = []
        
        validation = Validation.objects.filter(cart=cart).first()
        file_validation = None
        if validation:
            file_validation = validation.file_validation.url if validation.file_validation else None

        for i in manager:
            validation_manager = Validation.objects.filter(manager=i)
            national_code = i.national_code
            name = i.name
            file_manager = None

            if validation_manager.exists():
                validation_instance = validation_manager.first()
                file_manager = validation_instance.file_manager.url if validation_instance.file_manager else None

            manager_list.append({
                'national_code': national_code,
                'file_manager': file_manager,
                'name': name
            })

        return Response({
            'file_validation': file_validation,
            'managers': manager_list
        }, status=status.HTTP_200_OK)


class HistoryViewset (APIView) :
    def post (self, request, id) :
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
        if not request.FILES:
            return Response({'error': 'No files were uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        if not request.FILES:
            return Response({'error': 'No files were uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        manager_list = []

        for i in request.FILES:
            manager = Manager.objects.filter(national_code=i, cart=cart)
            if len(manager) == 0:
                return Response({'error': f'Manager with national code {i} not found for this cart'}, status=status.HTTP_404_NOT_FOUND)

            manager = manager.first()

            existing_history = History.objects.create(file=request.FILES[i], manager=manager, cart=cart)
            existing_history.save()

            manager_list.append({
                'national_code': manager.national_code,
                'name': manager.name,
                'file': existing_history.file.url if existing_history.file else None,
            })

        return Response({'managers': manager_list}, status=status.HTTP_200_OK)



    def get (self, request, id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response ({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response ({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = user.first()
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response ({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        manager = Manager.objects.filter(cart=cart)
        if not manager.exists():
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        manager_list = []
        for i in manager:
            history = History.objects.filter(manager=i)
            national_code = i.national_code
            name = i.name
            lock = False
            file = None
            
            if history.exists():
                history = history.first()
                history = serializers.HistorySerializer(history).data
                lock = history['lock']
                file = history['file']
            
            manager_list.append({
                'national_code': national_code,
                'lock': lock,
                'file': file,
                'name': name
            })

        return Response({'manager': manager_list}, status=status.HTTP_200_OK)






class HistoryAdminViewset (APIView) :
    def post (self, request, id) :
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
        if not request.FILES:
            return Response({'error': 'No files were uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        manager_list = []

        for i in request.FILES:
            manager = Manager.objects.filter(national_code=i, cart=cart)
            if len(manager) == 0:
                return Response({'error': f'Manager with national code {i} not found for this cart'}, status=status.HTTP_404_NOT_FOUND)

            manager = manager.first()

            existing_history = History.objects.create(file=request.FILES[i], manager=manager, cart=cart)
            existing_history.save()

            manager_list.append({
                'national_code': manager.national_code,
                'name': manager.name,
                'file': existing_history.file.url if existing_history.file else None,
            })

        return Response({'managers': manager_list}, status=status.HTTP_200_OK)





    def get (self, request, id) :
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response ({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        manager = Manager.objects.filter(cart=cart)
        if not manager.exists():
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
        manager_list = []
        for i in manager:
            history = History.objects.filter(manager=i)
            national_code = i.national_code
            name = i.name
            lock = False
            file = None
            
            if history.exists():
                history = history.first()
                history = serializers.HistorySerializer(history).data
                lock = history['lock']
                file = history['file']
            
            manager_list.append({
                'national_code': national_code,
                'lock': lock,
                'file': file,
                'name': name
            })

        return Response({'manager': manager_list}, status=status.HTTP_200_OK)




class SetSignatureViewset(APIView) :
    def post (self,request,id):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        admin = fun.decryptionadmin(Authorization)
        if not admin:
            return Response({'error': 'admin not found'}, status=status.HTTP_404_NOT_FOUND)
        admin = admin.first()
        cart = models.Cart.objects.filter(id=id).first()
        print(cart)
        manager = Manager.objects.filter(cart=cart)

        return Response ({'success': True}, status=status.HTTP_200_OK)
    

