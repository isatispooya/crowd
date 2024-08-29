from django.db import models
from authentication.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone




def validate_file_size(file):
    max_size = 2024288000
    if file.size > max_size:
        raise ValidationError(f"حجم فایل نباید بیشتر از {max_size / (1024 * 1024)} مگابایت باشد.")

#  کارت درخواست سرمایه پذیر
class Cart (models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length =200)
    Lock_company_name = models.BooleanField(default=False)
    
    activity_industry = models.CharField(max_length =200 , blank = True, null = True) #صنعت فعالیت
    Lock_activity_industry = models.BooleanField(default=False)

    registration_number = models.CharField(max_length = 20 , blank = True, null = True)  #شماره ثبت 
    Lock_registration_number = models.BooleanField(default=False)

    nationalid = models.CharField(max_length = 20 , blank = True, null = True)
    Lock_nationalid = models.BooleanField(default=False)

    registered_capital = models.CharField(max_length = 100,blank = True, null = True ) #سرمایه ثبتی
    Lock_registered_capital = models.BooleanField(default=False)

    personnel = models.IntegerField(blank = True, null = True)
    Lock_personnel = models.BooleanField(default=False)

    OPTION_KIND = [
        ('1', 'سهامی عام'),
        ('2', 'با مسئولیت محدود'),
        ('3', 'تضامنی'),
        ('4', 'مختلط'),
        ('5', 'نسبی'),
        ('6', 'تعاونی'),
        ('7', 'دانش بنیان'),
        ('8', 'سهامی خاص'),
    ]
    company_kind = models.CharField(max_length = 13, choices = OPTION_KIND, blank = True, null = True) #نوع شرکت
    Lock_company_kind = models.BooleanField(default=False)

    amount_of_request = models.CharField(max_length = 150 , blank = True, null = True) #منابع درخواستی
    Lock_amount_of_request = models.BooleanField(default=False)

    code = models.CharField(max_length = 5, blank = True, null = True)
    OPTION_STATUS = [
        ('1','در انتظار تایید'),
        ('2','نیاز به تکمیل'),
        ('3','تایید شده'),
    ]
    status = models.CharField(max_length = 20 , choices = OPTION_STATUS , default = 'waiting')

    email = models.EmailField(blank = True, null = True)
    Lock_email = models.BooleanField(default=False)
    
    address = models.CharField (max_length=500 , blank = True, null = True)
    Lock_address = models.BooleanField(default=False)

    financial_report_thisyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_financial_report_thisyear = models.BooleanField(default=False)

    financial_report_lastyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_financial_report_lastyear = models.BooleanField(default=False)
    financial_report_yearold = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_financial_report_yearold = models.BooleanField(default=False)

    audit_report_thisyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_audit_report_thisyear = models.BooleanField(default=False)

    audit_report_lastyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_audit_report_lastyear = models.BooleanField(default=False)

    audit_report_yearold = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_audit_report_yearold= models.BooleanField(default=False)

    statement_thisyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_statement_thisyear = models.BooleanField(default=False)

    statement_lastyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_statement_lastyear = models.BooleanField(default=False)

    statement_yearold = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_statement_yearold = models.BooleanField(default=False)

    alignment_6columns_thisyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_alignment_6columns_thisyear = models.BooleanField(default=False)

    alignment_6columns_lastyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_alignment_6columns_lastyear = models.BooleanField(default=False)

    alignment_6columns_yearold = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    Lock_alignment_6columns_yearold = models.BooleanField(default=False)
    creat = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.company_name
    

class Message(models.Model):
    cart  = models.ForeignKey(Cart , on_delete=models.CASCADE)
    message = models.CharField(max_length=512 )
    def __str__(self):
        return self.cart