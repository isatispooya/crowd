
from . import serializers
from cryptography.fernet import Fernet
import base64
from . import models
from ast import literal_eval
import requests

from django.core.mail import EmailMessage
from django.conf import settings

def encryptionUser(user):
    user = serializers.UserSerializer(user).data
    user = str(user)
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()
    fernet = Fernet(key)
    token = fernet.encrypt(user.encode())
    token = base64.urlsafe_b64encode(token).decode()
    return token

def decryptionUser(Bearer):
    try:
        token = Bearer.split('Bearer ')[1]
        with open('secret.key', 'rb') as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(token.encode())
        user = fernet.decrypt(encrypted_bytes).decode()
        user = literal_eval(user)
        user = models.User.objects.filter(id=user['id'])
        return user
    except:
        return None


def encryptionadmin(admin):
    admin = serializers.AdminSerializer(admin).data
    admin = str(admin)
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()
    fernet = Fernet(key)
    token = fernet.encrypt(admin.encode())
    token = base64.urlsafe_b64encode(token).decode()
    return token

def decryptionadmin(Bearer):
    try:
        token = Bearer.split('Bearer ')[1]
        with open('secret.key', 'rb') as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(token.encode())
        admin = fernet.decrypt(encrypted_bytes).decode()
        admin = literal_eval(admin)
        admin = models.Admin.objects.filter(id=admin['id'])
        return admin
    except:
        return None





def SendOtpEmail(code,email):
    subject = 'کد تایید ایساتیس کراد'
    message = f'ّکد تایید ورود به ایساتیس کراد شما {code} میباشد'
    recipient_list = [email]
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_FROM_ADDRESS,
        recipient_list,
        headers={"x-liara-tag": "test-tag"} 
    )

    
    email.send(fail_silently=False)



def SendSms(snd,txt):
    txt = f'به ایساتیس کراد خوش آمدید \n کد تایید :{txt}'
    resp = requests.get(url=f'http://tsms.ir/url/tsmshttp.php?from={settings.SMS_NUMBER}&to={snd}&username={settings.SMS_USERNAME}&password={settings.SMS_PASSWORD}&message={txt}').json()
    print(txt)
    return resp