from django.conf import settings
import requests
from django.core.mail import EmailMessage


class Message():
    def __init__(self):
        pass
    def otpSMS(self,otp,mobile):
        txt = f'به ایساتیس کراد خوش آمدید \n کد تایید :{otp}'
        resp = requests.get(url=f'http://tsms.ir/url/tsmshttp.php?from={settings.SMS_NUMBER}&to={mobile}&username={settings.SMS_USERNAME}&password={settings.SMS_PASSWORD}&message={txt}').json()
        print(txt)

    def otpEmail(otp,email):
        subject = 'کد تایید ایساتیس کراد'
        message = f'ّکد تایید ورود به ایساتیس کراد شما {otp} میباشد'
        recipient_list = [email]
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_FROM_ADDRESS,
            recipient_list,
            headers={"x-liara-tag": "test-tag"} 
        )
        email.send(fail_silently=False)