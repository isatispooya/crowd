from django.db import models

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
    nominal_price_certificate = models.CharField(max_length=1000, null=True , blank=True) #قیمت اسمی هر گواهی 

    
    def __str__(self) :
        return self.plan_name
    

class DocumentationFiles(models.Model):
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    title = models.CharField(max_length=150 , blank=True , null=True) 
    file = models.FileField(upload_to = 'static/', null=True , blank=True)
    def __str__(self) :
        return self.title
    

    
class Appendices(models.Model):
    plan = models.ForeignKey(Plan , on_delete=models.CASCADE)
    title = models.CharField(max_length=150 , blank=True , null=True) 
    file = models.FileField(upload_to = 'static/', null=True , blank=True)
    def __str__(self) :
        return self.title
    