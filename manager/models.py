from django.db import models
from investor.models import Cart



class Manager (models.Model):
    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=100)
    national_code = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    is_legal = models.BooleanField(default=False) #حقوقی
    phone = models.CharField(max_length=14)
    is_obliged = models.BooleanField(default=False) #موظف
    representative = models.CharField(max_length=100)
    cart = models.ForeignKey(Cart,  on_delete=models.CASCADE)
    lock = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
    

    
class Resume (models.Model):
    file = models.FileField(upload_to='static/')
    manager = models.ForeignKey(Manager,  on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)
    


class Shareholder (models.Model):
    name = models.CharField(max_length=100)
    national_code = models.CharField(max_length=50, null=True, blank=True)
    national_id = models.CharField(max_length=50, null=True, blank=True)
    percent = models.CharField(max_length=4 , null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Validation (models.Model) :
    file = models.FileField(upload_to ='static/')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.manager
