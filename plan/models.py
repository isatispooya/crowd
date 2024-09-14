from django.db import models

class Plan(models.Model):
    plan_name = models.CharField(max_length=100 )
    company_name = models.CharField(max_length=150)
    funded_amount = models.IntegerField()
    profit = models.FloatField()
    total_time = models.IntegerField()
    buoyancy = models.IntegerField()
    payment_period = models.IntegerField()
    picture = models.FileField(upload_to = 'static/')
    description = models.CharField(max_length=10000)
    status_option = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    ]
    plan_status = models.CharField(max_length=50 , choices=status_option)
    activity_field = models.CharField(max_length=150)
    remaining_days = models.IntegerField()
    marketer  = models.CharField(max_length=150)
    symbol = models.CharField(max_length=100 )
    farabours_link = models.CharField(max_length=500)
    applicant_funding_percentage = models.FloatField() #درصد تامین متقاضی
    nominal_price_certificate = models.CharField(max_length=1000) #قیمت اسمی هر گواهی 

    
    def __str__(self) :
        return self.plan_name
    