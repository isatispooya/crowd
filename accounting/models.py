from django.db import models
from authentication.models import User


class Wallet (models.Model):
    remaining = models.IntegerField(null=True , blank=True) #مانده
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    def __str__(self):
        return self.user.uniqueIdentifier
    

class Transaction (models.Model):
    wallet = models.ForeignKey(Wallet , on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(null=True, blank=True) # تاریخ تراکنش
    method_option = [
        ('1','درگاه انلاین'),
        ('2','فیش'),
    ]
    method = models.CharField(max_length=20 , choices=method_option , null=True , blank=True ) #روش 
    credit_amount = models.IntegerField(null=True, blank=True) # مقدار بستانکاری
    debt_amount = models.IntegerField (null=True, blank=True) # مقدار بدهکاری
    status = models.BooleanField(default=False)
    description_transaction = models.CharField(max_length=250 , null=True , blank= True) #شرح تراکنش
    image_receipt = models.FileField(upload_to = 'static/', null=True , blank=True) #تصویر فیش
    document_number = models.CharField(max_length=100 , null=True , blank= True) #شماره سند

    def __str__(self):
        return self.method