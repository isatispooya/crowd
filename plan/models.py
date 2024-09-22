from django.db import models
from authentication.models import User
from accounting.models import Wallet

class Plan(models.Model):
    plan_name = models.CharField(max_length=100 , null=True , blank=True )
    company_name = models.CharField(max_length=150, null=True , blank=True)
    funded_amount = models.IntegerField(null=True , blank=True) #مبلغ بودجه
    profit = models.FloatField(null=True , blank=True) #سود
    total_time = models.IntegerField(null=True , blank=True) #مدت زمان طرح
    buoyancy = models.IntegerField(null=True , blank=True) #شناوری
    payment_period = models.IntegerField(null=True , blank=True) #دوره پرداخت
    picture = models.FileField(upload_to = 'static/', null=True , blank=True)
    description = models.CharField(max_length=10000, null=True , blank=True)
    status_option = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    ]
    plan_status = models.CharField(max_length=50 , choices=status_option, null=True , blank=True)
    activity_field = models.CharField(max_length=150, null=True , blank=True) 
    remaining_days = models.IntegerField(null=True , blank=True) #روزهای باقی مانده
    marketer  = models.CharField(max_length=150, null=True , blank=True) # بازارگردان
    symbol = models.CharField(max_length=100 , null=True , blank=True)
    farabours_link = models.CharField(max_length=500, null=True , blank=True)
    applicant_funding_percentage = models.FloatField(null=True , blank=True) #درصد تامین متقاضی
    nominal_price_certificate = models.IntegerField( null=True , blank=True) #قیمت اسمی هر گواهی 

    
    def __str__(self) :
        return self.plan_name
    

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
    participant = models.ForeignKey(User , on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    amount = models.BigIntegerField( null=True, blank=True)
    total_amount = models.BigIntegerField( null=True , blank=True)
    def __str__(self) :
            return self.participant.uniqueIdentifier
        



class DocumentationRecieve (models.Model):
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    type = models.CharField(max_length=20 , blank=True , null= True , choices =[('1','اصل پول') , ('2','سود')])
    amount = models.BigIntegerField( null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
            return self.plan.plan_name
        
