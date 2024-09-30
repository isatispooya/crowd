from django.db import models
from authentication.models import User
from accounting.models import Wallet
from django.utils import timezone

# class Plan(models.Model):
#     plan_name = models.CharField(max_length=100 , null=True , blank=True )
#     company_name = models.CharField(max_length=150, null=True , blank=True)
#     funded_amount = models.IntegerField(null=True , blank=True) #مبلغ بودجه
#     profit = models.FloatField(null=True , blank=True) #سود
#     total_time = models.IntegerField(null=True , blank=True) #مدت زمان طرح
#     buoyancy = models.IntegerField(null=True , blank=True) #شناوری
#     payment_period = models.IntegerField(null=True , blank=True) #دوره پرداخت
#     picture = models.FileField(upload_to = 'static/', null=True , blank=True)
#     description = models.CharField(max_length=10000, null=True , blank=True)
#     status_option = [
#         ('1','1'),
#         ('2','2'),
#         ('3','3'),
#         ('4','4'),
#         ('5','5'),
#     ]
#     plan_status = models.CharField(max_length=50 , choices=status_option, null=True , blank=True)
#     activity_field = models.CharField(max_length=150, null=True , blank=True) 
#     remaining_from_to = models.DateTimeField(null=True, blank=True) #روزهای باقی مانده از
#     remaining_date_to = models.DateTimeField(null=True, blank=True) #روزهای باقی مانده تا 
#     marketer  = models.CharField(max_length=150, null=True , blank=True) # بازارگردان
#     symbol = models.CharField(max_length=100 , null=True , blank=True)
#     farabours_link = models.CharField(max_length=500, null=True , blank=True)
#     applicant_funding_percentage = models.FloatField(null=True , blank=True) #درصد تامین متقاضی
#     nominal_price_certificate = models.IntegerField( null=True , blank=True) #قیمت اسمی هر گواهی 
#     amount_of_shareholders = models.IntegerField( null=True , blank=True) #تعداد سرمایه گذران


#     def __str__(self) :
#         return self.plan_name
    


class Plan (models.Model) : 
    trace_code = models.CharField(max_length=500, null=True , blank=True)
    creation_date = models.CharField(max_length=500, null=True , blank=True)
    persian_name =  models.CharField(max_length=500, null=True , blank=True)
    persian_suggested_symbol = models.CharField(max_length=500, null=True , blank=True)
    persoan_approved_symbol = models.CharField(max_length=500, null=True , blank=True)
    english_name = models.CharField(max_length=500, null=True , blank=True)
    english_suggested_symbol = models.CharField(max_length=500, null=True , blank=True)
    english_approved_symbol = models.CharField(max_length=500, null=True , blank=True)
    industry_group_id =  models.IntegerField( null=True , blank=True)
    industry_group_description =  models.CharField(max_length=500, null=True , blank=True)
    sub_industry_group_id =  models.CharField(max_length=500, null=True , blank=True)
    sub_industry_group_description =  models.CharField(max_length=500, null=True , blank=True)
    persian_subject =  models.CharField(max_length=500, null=True , blank=True)
    english_subject = models.CharField(max_length=500, null=True , blank=True)
    unit_price = models.IntegerField( null=True , blank=True)
    total_units =  models.IntegerField( null=True , blank=True)
    company_unit_counts =  models.IntegerField( null=True , blank=True)
    total_price =  models.BigIntegerField( null=True, blank=True)
    crowd_funding_type_id  =  models.IntegerField( null=True , blank=True)
    crowd_funding_type_description =  models.CharField(max_length=500, null=True , blank=True)
    float_crowd_funding_type_description = models.CharField(max_length=500, null=True , blank=True)
    minimum_required_price =  models.BigIntegerField( null=True, blank=True)
    real_person_minimum_availabe_price =  models.BigIntegerField( null=True, blank=True)
    real_person_maximum_available_price = models.BigIntegerField( null=True, blank=True)
    legal_person_minimum_availabe_price =  models.BigIntegerField( null=True, blank=True)
    legal_person_maximum_availabe_price =  models.BigIntegerField( null=True, blank=True)
    underwriting_duration =   models.IntegerField( null=True , blank=True)
    suggested_underwriting_start_date =  models.CharField(max_length=500, null=True , blank=True)
    suggested_underwriting_end_date = models.CharField(max_length=500, null=True , blank=True)
    approved_underwriting_start_date = models.CharField(max_length=500, null=True , blank=True)
    approved_underwriting_end_date = models.CharField(max_length=500, null=True , blank=True)
    project_start_date =   models.CharField(max_length=500, null=True , blank=True)
    project_end_date =  models.CharField(max_length=500, null=True , blank=True)
    settlement_description =  models.CharField(max_length=500, null=True , blank=True)
    project_status_description =  models.CharField(max_length=500, null=True , blank=True)
    project_status_id =   models.IntegerField( null=True , blank=True)
    persian_suggested_underwiring_start_date =  models.CharField(max_length=500, null=True , blank=True)
    persian_suggested_underwriting_end_date =  models.CharField(max_length=500, null=True , blank=True)
    persian_approved_underwriting_start_date =  models.CharField(max_length=500, null=True , blank=True)
    persian_approved_underwriting_end_date =  models.CharField(max_length=500, null=True , blank=True)
    persian_project_start_date =  models.CharField(max_length=500, null=True , blank=True)
    persian_project_end_date = models.CharField(max_length=500, null=True , blank=True)
    persian_creation_date =  models.CharField(max_length=500, null=True , blank=True)
    number_of_finance_provider =  models.IntegerField( null=True , blank=True)
    sum_of_funding_provided =   models.IntegerField( null=True , blank=True)
    
class ProjectOwnerCompan(models.Model):
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    national_id = models.BigIntegerField( null=True, blank=True)
    name = models.CharField(max_length=500, null=True , blank=True)
    compnay_type_id = models.IntegerField( null=True , blank=True)
    company_type_description = models.CharField(max_length=500, null=True , blank=True)
    registration_date = models.CharField(max_length=500, null=True , blank=True)
    registration_number = models.CharField(max_length=500, null=True , blank=True)
    economic_id = models.CharField(max_length=500, null=True , blank=True)
    address = models.CharField(max_length=500, null=True , blank=True)
    postal_code = models.CharField(max_length=500, null=True , blank=True)
    phone_number = models.CharField(max_length=500, null=True , blank=True)
    fax_number = models.CharField(max_length=500, null=True , blank=True)
    email_address = models.CharField(max_length=500, null=True , blank=True)

class ListOfProjectBigShareHolders(models.Model):
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    national_id = models.BigIntegerField( null=True, blank=True)
    shareholder_type = models.IntegerField( null=True , blank=True)
    first_name =models.CharField(max_length=500, null=True , blank=True)
    last_name = models.CharField(max_length=500, null=True , blank=True)
    share_percent = models.FloatField( null=True , blank=True)


class ListOfProjectBoardMembers(models.Model):
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    national_id = models.BigIntegerField( null=True, blank=True)
    mobile_number = models.CharField(max_length=500, null=True , blank=True)
    email_address = models.CharField(max_length=500, null=True , blank=True)
    organization_post_id = models.IntegerField( null=True , blank=True)
    is_agent_from_company = models.BooleanField(null=True , blank=True)
    first_name =models.CharField(max_length=500, null=True , blank=True)
    last_name = models.CharField(max_length=500, null=True , blank=True)
    company_national_id = models.BigIntegerField( null=True, blank=True)
    company_name = models.CharField(max_length=500, null=True , blank=True)




    
class DocumentationFiles(models.Model): #فایل های مستندات
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    title = models.CharField(max_length=150 , blank=True , null=True) 
    file = models.FileField(upload_to = 'static/', null=True , blank=True)
    def __str__(self) :
        return self.title
    

    
class Appendices(models.Model): #تضامین 
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    title = models.CharField(max_length=150 , blank=True , null=True) 
    file = models.FileField(upload_to = 'static/', null=True , blank=True)
    def __str__(self) :
        return self.title
    


class Comment(models.Model):
    comment = models.CharField(max_length=2000 , null= True, blank = True) 
    status = models.BooleanField(default=False)
    known =  models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    def __str__(self) :
        return self.user.uniqueIdentifier
    


class PaymentGateway(models.Model) :
    wallet = models.ForeignKey(Wallet , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=30 , null=True, blank=True)
    amount = models.CharField(max_length=100 , null=True, blank=True)
    description = models.CharField(max_length=2500 , null=True, blank=True)
    code = models.CharField(max_length=2500 , null=True, blank=True)
    cart_number =  models.CharField(max_length=50 , null=True, blank=True)
    cart_hashpan =  models.CharField(max_length=50 , null=True, blank=True)

    def __str__(self) :
            return self.user.uniqueIdentifier
        

class Participant (models.Model):
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    amount = models.BigIntegerField( null=True, blank=True)
    total_amount = models.BigIntegerField( null=True , blank=True)
    name_status = models.BooleanField (default=False)
    create_date =  models.DateTimeField(null=True, blank=True, default=timezone.now) # تاریخ ایجاد مشارکت 
    risk_statement = models.BooleanField(default=True) # بیانیه ریسک
    agreement = models.BooleanField(default=True) # موافقت نامه
    status = models.BooleanField(default=True) # وضعیت تایید سفارش 
    participant_new = models.CharField(max_length=20 , blank= True , null= True)
    def __str__(self) :
            return self.participant_new
        



class DocumentationRecieve (models.Model):
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    type = models.CharField(max_length=20 , blank=True , null= True , choices =[('1','اصل پول') , ('2','سود')])
    amount = models.BigIntegerField( null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    doing = models.BooleanField(default=False)
    def __str__(self) :
            return self.plan.plan_name
        

class Plans (models.Model):
    plan_id = models.CharField(max_length=250)

    def __str__(self) :
         return self.plan_id
    