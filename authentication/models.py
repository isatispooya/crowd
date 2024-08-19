from django.db import models

class User(models.Model):
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    fatherName = models.CharField(max_length=32)
    mobile = models.CharField(max_length=11)
    uniqueIdentifier = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=150)
    sheba = models.CharField(max_length=150)
    city_name = models.CharField(max_length=150)
    country_name = models.CharField(max_length=150)
    postalCode = models.CharField(max_length=150)
    email = models.EmailField()
    province_name = models.CharField(max_length=150)
    remnantAddress = models.CharField(max_length=150)
    assetsValue = models.CharField(max_length=150)
    inComingAverage = models.CharField(max_length=150)
    birthDate = models.DateTimeField()
    gender = models.CharField(max_length=150)
    placeOfBirth = models.CharField(max_length=150)
    placeOfIssue = models.CharField(max_length=150)
    shNumber = models.CharField(max_length=150)
    type = models.CharField(max_length=150)

    def __str__(self):
        uniqueIdentifier = self.uniqueIdentifier if self.uniqueIdentifier else "uniqueIdentifier"
        return f'{uniqueIdentifier}'
    
class Otp(models.Model):
    code = models.CharField(max_length=4)
    mobile = models.CharField(max_length=11)
    date = models.DateTimeField(auto_now_add=True)

class Admin(models.Model):
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    mobile = models.CharField(max_length=11)
    uniqueIdentifier = models.CharField(max_length=10)











