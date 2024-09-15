from django.db import models
from authentication.models import User


class Wallet (models.Model):
    remaining = models.IntegerField(null=True , blank=True)
    adjustment_balance = models.IntegerField(null=True , blank=True)
    credit =  models.IntegerField(null=True , blank=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    def __str__(self):
        return self.user.uniqueIdentifier
    

class Transaction (models.Model):
    wallet = models.ForeignKey(Wallet , on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(null=True, blank=True)
    method_option = [
        ('1','درگاه'),
        ('2','فیش'),
        ('3','شرکت در طرح'),
        ('4','برداشت وجه'),
    ]
    method = models.CharField(max_length=20 , choices=method_option , null=True , blank=True )
    credit_amount = models.IntegerField(null=True, blank=True)
    debt_amount = models.IntegerField (null=True, blank=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.method