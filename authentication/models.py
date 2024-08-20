from django.db import models


class bank (models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 150)

class branchCity (models.Model) :
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 150)

class accounts (models.Model) :
    accountNumber = models.CharField(max_length=200)
    bank = models.ForeignKey( bank, on_delete = models.CASCADE)
    branchCity = models.ForeignKey(branchCity, on_delete = models.CASCADE)
    branchCode = models.CharField(max_length=20)
    branchName = models.CharField(max_length=200)
    isDefault = models.DateTimeField (default=False)
    modifiedDate = models.DateTimeField()
    type = models.CharField(max_length= 200)
    sheba = models.CharField(max_length= 200)


class city (models.Model):
    name = models.CharField(max_length=200)
    id = models.IntegerField (primary_key=True)

class country (models.Model):
    name = models.CharField(max_length=200)
    id = models.IntegerField (primary_key=True)

class province (models.Model):
    name = models.CharField(max_length=200)
    id = models.IntegerField (primary_key=True)

class section (models.Model):
    name = models.CharField(max_length=200)
    id = models.IntegerField (primary_key=True)

class addresses (models.Model):
    alley = models.CharField(max_length=1000 ,  blank=True , null= True)
    city = models.ForeignKey( city, on_delete = models.CASCADE)
    cityPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    country =models.ForeignKey( country, on_delete = models.CASCADE)
    countryPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    email = models.EmailField ()
    emergencyTel =  models.CharField(max_length=1000 ,  blank=True , null= True) 
    emergencyTelCityPrefix =  models.CharField(max_length=1000 ,  blank=True , null= True)
    emergencyTelCountryPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    fax = models.CharField(max_length=1000 ,  blank=True , null= True)
    faxPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    mobile = models.CharField(max_length=1000 ,  blank=True , null= True)
    plaque = models.CharField(max_length=1000 ,  blank=True , null= True)
    postalCode = models.CharField(max_length=1000 ,  blank=True , null= True)
    province = models.ForeignKey( province, on_delete = models.CASCADE)
    remnantAddress = models.CharField(max_length=1000 ,  blank=True , null= True)
    section =models.ForeignKey( section, on_delete = models.CASCADE)
    tel =  models.CharField(max_length=1000 ,  blank=True , null= True)
    website = models.CharField(max_length=1000 ,  blank=True , null= True)




class financialInfo (models.Model) :
    assetsValue = models.CharField(max_length=1000 ,  blank=True , null= True)
    cExchangeTransaction = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyPurpose = models.CharField(max_length=1000 ,  blank=True , null= True)
    financialBrokers = models.CharField(max_length=1000 ,  blank=True , null= True)
    inComingAverage = models.CharField(max_length=1000 ,  blank=True , null= True)
    outExchangeTransaction = models.CharField(max_length=1000 ,  blank=True , null= True)
    rate = models.CharField(max_length=1000 ,  blank=True , null= True)
    rateDate = models.CharField(max_length=1000 ,  blank=True , null= True)
    referenceRateCompany = models.CharField(max_length=1000 ,  blank=True , null= True)
    sExchangeTransaction = models.CharField(max_length=1000 ,  blank=True , null= True)
    tradingKnowledgeLevel = models.CharField(max_length=1000 ,  blank=True , null= True)
    transactionLevel = models.CharField(max_length=1000 ,  blank=True , null= True)



class job (models.Model) :
    id = models.IntegerField (primary_key=True)
    title = models.CharField(max_length=200 ,  blank=True , null= True)

class jobInfo (models.Model) :
    companyAddress = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyCityPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyEmail = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyFax =  models.CharField(max_length=1000 ,  blank=True , null= True)
    companyFaxPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyName = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyPhone = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyPostalCode = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyWebSite = models.CharField(max_length=1000 ,  blank=True , null= True)
    employmentDate = models.CharField(max_length=1000 ,  blank=True , null= True)
    job = models.ForeignKey( job, on_delete = models.CASCADE)
    jobDescription = models.CharField(max_length=1000 ,  blank=True , null= True)
    position = models.CharField(max_length=1000 ,  blank=True , null= True)

class privatePerson (models.Model) :
    birthDate = models.DateField()
    fatherName = models.CharField(max_length=200)
    firstName = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    placeOfBirth = models.CharField(max_length=200)
    placeOfIssue = models.CharField(max_length=200)
    seriSh = models.CharField(max_length=200)
    seriShChar = models.CharField(max_length=200)
    serial = models.CharField(max_length=200)
    shNumber = models.CharField(max_length=200)
    signatureFile = models.FileField(upload_to='signatures/', null=True, blank=True) 


class tradingCodes (models.Model) :
    code = models.CharField(max_length=200)
    firstPart =  models.CharField(max_length=200)
    secondPart  = models.CharField(max_length=200)
    thirdPart = models.CharField(max_length=200)
    type = models.CharField(max_length=200)



class User(models.Model):
    accounts = models.ForeignKey( accounts, on_delete = models.CASCADE)
    addresses = models.ForeignKey( addresses, on_delete = models.CASCADE)
    agent = models.CharField(max_length= 200 , null=True, blank=True )
    email = models.EmailField( null=True, blank=True)
    financialInfo = models.ForeignKey( financialInfo, on_delete = models.CASCADE)
    jobInfo =models.ForeignKey( jobInfo, on_delete = models.CASCADE)
    legalPerson = models.CharField(max_length=150 ,null=True, blank=True )
    legalPersonShareholders = models.CharField(max_length=150 ,null=True, blank=True )
    legalPersonStakeholders = models.CharField(max_length=150 ,null=True, blank=True )
    mobile = models.CharField(max_length=11)
    privatePerson = models.ForeignKey( privatePerson, on_delete = models.CASCADE)
    status = models.CharField(max_length=150 , null=True, blank=True)
    tradingCodes = models.ForeignKey( tradingCodes, on_delete = models.CASCADE)
    type = models.CharField(max_length=200)
    uniqueIdentifier = models.CharField(max_length=150 , unique=True)


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











