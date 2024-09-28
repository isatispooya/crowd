from django.shortcuts import render
from .models import Manager ,  Resume , Validation , Shareholder , History
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from authentication import fun
from . import serializers
from investor import models
import datetime

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
        
        cart = models.Cart.objects.filter(id=id).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        for file_key, file_value in request.FILES.items():
            manager = Manager.objects.filter(national_code=file_key, cart=cart).first()
            if not manager:
                return Response({'error': 'Management not found'}, status=status.HTTP_404_NOT_FOUND)

            resume = Resume.objects.filter(manager=manager)
            if resume:
                resume.delete()

            data = {
                'file': file_value,
                'manager': manager.id,
                
            }
            serializer = serializers.ResumeSerializer(data = data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()        
        return Response({'success' : True}, status=status.HTTP_200_OK)


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
        managers_data = []

        if not request.FILES:
            return Response({'error': 'No file was uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart = models.Cart.objects.filter(id=id)
        if len(cart) == 0:
            return Response({'error': 'Not found cart'}, status=status.HTTP_400_BAD_REQUEST)
        cart = cart.first()
        lock = request.data.get('lock') == 'true'
        for file_key, file in request.FILES.items():
            manager = Manager.objects.filter(national_code=file_key, cart=cart)
            if not manager.exists():
                return Response({'error': f'Not found management for national_code {file_key}'}, status=status.HTTP_400_BAD_REQUEST)
            manager = manager.first()
            existing_resumes = Resume.objects.filter(manager=manager)
            if existing_resumes.exists():
                existing_resumes.delete()
            resume = Resume(file=file, manager=manager, lock=lock)
            resume.save()
            serializer = serializers.ResumeSerializer(resume)
            managers_data.append(serializer.data)
        return Response({'managers': managers_data }, status=status.HTTP_201_CREATED)

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
    def post(self, request, id):
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

            validation_existing = Validation.objects.filter(cart=cart, manager='1').first()

            file_manager = request.FILES.get('1')
            date_manager = request.data.copy()

            if not file_manager and not validation_existing:
                return Response({'error': 'File validation is missing'}, status=status.HTTP_400_BAD_REQUEST)

            manager_list = []

            for national_code, file in request.FILES.items():
                if national_code == '1':
                    continue

                manager = Manager.objects.filter(national_code=national_code, cart=cart).first()
                if not manager:
                    return Response({'error': f'Manager with national code {national_code} not found for this cart'}, status=status.HTTP_404_NOT_FOUND)

                existing_validation = Validation.objects.filter(manager=manager.national_code, cart=cart).first()
                if existing_validation:
                    existing_validation.file_manager.delete()
                    existing_validation.delete()
                date = int(date_manager[f'{national_code}_date'])/1000
                date = datetime.datetime.fromtimestamp(date)

                new_validation = Validation.objects.create(file_manager=file, manager=manager.national_code, cart=cart, date=date)
                new_validation.save()

                manager_list.append({
                    'national_code': manager.national_code,
                    'name': manager.name,
                    'file_manager': new_validation.file_manager.url if new_validation.file_manager else None,
                    'date' : new_validation.date
                })

            if file_manager:
                if validation_existing:
                    validation_existing.file_manager.delete()
                    validation_existing.delete()
                date = int(date_manager['1_date'])/1000
                date = datetime.datetime.fromtimestamp(date)
                validation = Validation.objects.create(file_manager=file_manager, cart=cart, manager='1',date=date)
                validation.save()

                manager_list.append({
                    'national_code': '1',
                    'name': 'شرکت',
                    'file_manager': validation.file_manager.url if validation.file_manager else None,
                    'date' : validation.date
                })
            else:
                manager_list.append({
                    'national_code': '1',
                    'name': 'شرکت',
                    'file_manager': validation_existing.file_manager.url if validation_existing and validation_existing.file_manager else None , 
                    'date' : validation.date
                })

            response_data = {
                'managers': manager_list
            }

            return Response({'data': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def get(self, request, id):
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

            managers = Manager.objects.filter(cart=cart)
            if not managers.exists():
                return Response({'error': 'No managers found for this cart'}, status=status.HTTP_404_NOT_FOUND)

            manager_list = []
            for manager in managers:
                validation = Validation.objects.filter(manager=manager.national_code, cart=cart).first()
                
                print(validation)

                if validation:
                    date = validation.date
                else:
                    date = datetime.datetime.now()

                print(date)
                

                manager_list.append({
                    'national_code': manager.national_code,
                    'name': manager.name,
                    'file_manager': validation.file_manager.url if validation and validation.file_manager else None,
                    'date' : date
                })


            company_validation = Validation.objects.filter(manager='1', cart=cart).first()

            if company_validation:
                date = company_validation.date
            else:
                date = datetime.datetime.now()

            manager_list.append({
                'national_code': '1',
                'name': 'شرکت',
                'file_manager': company_validation.file_manager.url if company_validation and company_validation.file_manager else None,
                'date' : date

            })

            response_data = {
                'managers': manager_list
            }

            return Response({'data': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            lock = request.data.get('lock') == 'true'
            validation_existing = Validation.objects.filter(cart=cart, manager='1' , lock=lock).first()

            file_manager = request.FILES.get('1')
            date_manager = request.data.copy()

            if not file_manager and not validation_existing:
                return Response({'error': 'File validation is missing'}, status=status.HTTP_400_BAD_REQUEST)

            manager_list = []

            for national_code, file in request.FILES.items():
                if national_code == '1':
                    continue

                manager = Manager.objects.filter(national_code=national_code, cart=cart).first()
                if not manager:
                    return Response({'error': f'Manager with national code {national_code} not found for this cart'}, status=status.HTTP_404_NOT_FOUND)

                existing_validation = Validation.objects.filter(manager=manager.national_code, cart=cart , lock = lock).first()
                if existing_validation:
                    existing_validation.file_manager.delete()
                    existing_validation.delete()
                date = int(date_manager[f'{national_code}_date'])/1000
                date = datetime.datetime.fromtimestamp(date)
                new_validation = Validation.objects.create(file_manager=file, manager=manager.national_code, cart=cart, date=date , lock = lock)

                new_validation.save()

                manager_list.append({
                    'national_code': manager.national_code,
                    'name': manager.name,
                    'file_manager': new_validation.file_manager.url if new_validation.file_manager else None,
                    'date' : new_validation.date,
                    'lock' : lock
                })

            if file_manager:
                if validation_existing:
                    validation_existing.file_manager.delete()
                    validation_existing.delete()
                date = int(date_manager['1_date'])/1000
                date = datetime.datetime.fromtimestamp(date)
                validation = Validation.objects.create(file_manager=file_manager, cart=cart, manager='1',date=date ,  lock=lock)
                validation.save()

                manager_list.append({
                    'national_code': '1',
                    'name': 'شرکت',
                    'file_manager': validation.file_manager.url if validation.file_manager else None,
                    'date' : validation.date,
                    'lock' : lock

                })
            else:
                manager_list.append({
                    'national_code': '1',
                    'name': 'شرکت',
                    'file_manager': validation_existing.file_manager.url if validation_existing and validation_existing.file_manager else None,
                    'date' : validation.date,
                    'lock' : lock
                })

            response_data = {
                'managers': manager_list
            }

            return Response({'data': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get (self, request, id) :
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

            managers = Manager.objects.filter(cart=cart)
            if not managers.exists():
                return Response({'error': 'No managers found for this cart'}, status=status.HTTP_404_NOT_FOUND)

            manager_list = []
            for manager in managers:
                validation = Validation.objects.filter(manager=manager.national_code, cart=cart).first()
                if validation:
                  date = validation.date
                else:
                    date = datetime.datetime.now()


                manager_list.append({
                    'national_code': manager.national_code,
                    'name': manager.name,
                    'file_manager': validation.file_manager.url if validation and validation.file_manager else None,
                    'date' : date,
                    'lock' : validation.lock if validation and validation.lock else None
                })

            company_validation = Validation.objects.filter(manager='1', cart=cart).first()
            if company_validation :
                date = company_validation.date
            else:
                date = datetime.datetime.now()
            manager_list.append({
                'national_code': '1',
                'name': 'شرکت',
                'file_manager': company_validation.file_manager.url if company_validation and company_validation.file_manager else None,
                'date' : date,
                'lock' : company_validation.lock if company_validation else None

            })

            response_data = {
                'managers': manager_list
            }

            return Response({'data': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
        date_manager = request.data.copy()
        manager_list = []

        for file_key, file_value in request.FILES.items():
            manager = Manager.objects.filter(national_code=file_key, cart=cart).first()
            if not manager:
                return Response({'error': f'Manager with national code {file_key} not found for this cart'}, status=status.HTTP_404_NOT_FOUND)
            try:
                timestamp_key = f'{manager.national_code}_date'  
                if timestamp_key not in date_manager:
                    return Response({'error': f'Date for manager with national code {manager.national_code} is missing'}, status=status.HTTP_400_BAD_REQUEST)
                
                date = int(date_manager[timestamp_key]) / 1000  
                date = datetime.datetime.fromtimestamp(date)     

                print(f"Date for manager {manager.national_code}: {date}")  
            except (KeyError, ValueError) as e:
                return Response({'error': f'Invalid date format for manager {manager.national_code}'}, status=status.HTTP_400_BAD_REQUEST)
            
            existing_history = History.objects.filter(manager=manager, cart=cart).first()
            
            if existing_history:
                existing_history.delete()  
            new_history = History.objects.create(file=file_value, manager=manager, cart=cart , date=date)

            manager_list.append({
                'national_code': manager.national_code,
                'name': manager.name,
                'file': new_history.file.url if new_history.file else None,
                'date' : new_history.date
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
            history = History.objects.filter(manager=i).first()
            
            if history:
                date = history.date 
            else:
                date = datetime.datetime.now()
                
            national_code = i.national_code
            name = i.name
            lock = False
            file = None

            
            if history:
                history = serializers.HistorySerializer(history).data
                lock = history['lock']
                file = history['file']
                date = history ['date']

   
            manager_list.append({
                'national_code': national_code,
                'lock': lock,
                'file': file,
                'name': name ,
                'date' : date 
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
        date_manager = request.data.copy()
        manager_list = []

        for i in request.FILES:
            manager = Manager.objects.filter(national_code=i, cart=cart)
            if len(manager) == 0:
                return Response({'error': f'Manager with national code {i} not found for this cart'}, status=status.HTTP_404_NOT_FOUND)
            manager = manager.first()

            try:
                timestamp_key = f'{manager.national_code}_date'  
                if timestamp_key not in date_manager:
                    return Response({'error': f'Date for manager with national code {manager.national_code} is missing'}, status=status.HTTP_400_BAD_REQUEST)
                
                date = int(date_manager[timestamp_key]) / 1000  
                date = datetime.datetime.fromtimestamp(date)     

            except (KeyError, ValueError) as e:
                return Response({'error': f'Invalid date format for manager {manager.national_code}'}, status=status.HTTP_400_BAD_REQUEST)
            
            existing_history = History.objects.create(file=request.FILES[i], manager=manager, cart=cart , date=date)
            existing_history.save()

            manager_list.append({
                'national_code': manager.national_code,
                'name': manager.name,
                'file': existing_history.file.url if existing_history.file else None,
                'date' : existing_history.date

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
            history = History.objects.filter(manager=i).first()
            if history:
                date = history.date 
            else:
                date = datetime.datetime.now()
                
            national_code = i.national_code
            name = i.name
            lock = False
            file = None

            
            if history:
                history = serializers.HistorySerializer(history).data
                lock = history['lock']
                file = history['file']
                date = history ['date']

   
            manager_list.append({
                'national_code': national_code,
                'lock': lock,
                'file': file,
                'name': name ,
                'date' : date 
            })

        return Response({'manager': manager_list}, status=status.HTTP_200_OK)




