from django.db import models
from authentication.models import User

#  کارت درخواست سرمایه پذیر
class Cart (models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    activity_industry = models.CharField(max_length=200)
    registration_number = models.CharField(max_length= 20 , unique=True)
    nationalid = models.CharField(max_length= 20 , unique=True)
    registered_capital = models.CharField(max_length= 100 )
    personnel = models.IntegerField()
    OPTION_KIND = [
        ('special stock', 'سهامی خاص'),
        ('common stock', 'سهامی عام'),
    ]
    company_kind = models.CharField(max_length=13, choices=OPTION_KIND)
    amount_of_request = models.CharField(max_length= 150)


    def __str__(self):
        return self.company_name