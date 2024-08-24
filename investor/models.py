from django.db import models
from authentication.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone




def validate_file_size(file):
    max_size = 20242880  
    if file.size > max_size:
        raise ValidationError(f"حجم فایل نباید بیشتر از {max_size / (1024 * 1024)} مگابایت باشد.")

#  کارت درخواست سرمایه پذیر
class Cart (models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length =200)
    activity_industry = models.CharField(max_length =200 , blank = True, null = True) #صنعت فعالیت
    registration_number = models.CharField(max_length = 20 )  #شماره ثبت 
    nationalid = models.CharField(max_length = 20 , blank = True, null = True)
    registered_capital = models.CharField(max_length = 100,blank = True, null = True ) #سرمایه ثبتی
    personnel = models.IntegerField(blank = True, null = True)
    OPTION_KIND = [
        ('special stock', 'سهامی خاص'),
        ('common stock', 'سهامی عام'),
    ]
    company_kind = models.CharField(max_length = 13, choices = OPTION_KIND, blank = True, null = True) #نوع شرکت
    amount_of_request = models.CharField(max_length = 150 , blank = True, null = True) #منابع درخواستی
    code = models.CharField(max_length = 5, blank = True, null = True)
    OPTION_STATUS = [
        ('waiting','در انتظار تایید'),
        ('editing','نیاز به تکمیل'),
        ('okay','تایید شده'),
    ]
    status = models.CharField(max_length = 20 , choices = OPTION_STATUS , default = 'waiting')
    email = models.EmailField(blank = True, null = True)
    address = models.CharField (max_length=500 , blank = True, null = True)
    financial_report_thisyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    financial_report_lastyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    financial_report_yearold = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    audit_report_thisyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    audit_report_lastyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    audit_report_yearold = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    statement_thisyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    statement_lastyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    statement_yearold = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    alignment_6columns_thisyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    alignment_6columns_lastyear = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    alignment_6columns_yearold = models.FileField(upload_to='static/' ,  blank = True, null = True,validators=[validate_file_size])
    creat = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.company_name