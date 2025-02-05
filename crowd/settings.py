
from pathlib import Path
import dj_database_url
import os
from dotenv import load_dotenv

# بارگذاری فایل .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640   # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 15728640   # 50 MB
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = ['apicrowd.isatispooya.com'] if not DEBUG else ['*']
APPEND_SLASH = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CORS_ALLOW_CREDENTIALS = True    
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    '*'
]

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        "https://admincrowd.isatispooya.com",
        "https://mycrowd.isatispooya.com",
        "https://crowd.isatispooya.com",
        "https://app.isatiscrowd.ir",
        "https://isatiscrowd.ir",
        "https://admin.isatiscrowd.ir",

    ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'investor',
    'rest_framework',
    'corsheaders',
    'manager',
    'contract',
    'dbbackup',
    'plan', 
    'accounting', 
    'reports',


]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.security.SecurityMiddleware',
    # 'middleware.XSSCleanMiddleware.XSSCleanMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crowd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'crowd.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

DATABASES['default']['OPTIONS'] = {
    'timeout': 90  
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'crowd',
#         'USER': 'postgres',
#         'PASSWORD': 'isatis-1403',
#         'HOST':'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
# DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'backups')}

#SMTP SERVER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('MAIL_HOST')
EMAIL_PORT = os.getenv('MAIL_PORT')
EMAIL_HOST_USER = os.getenv('MAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('MAIL_PASSWORD')
EMAIL_USE_TLS = True  # Use TLS encryption
EMAIL_FROM_ADDRESS = os.getenv('MAIL_FROM_ADDRESS')
DEFAULT_FROM_EMAIL = os.getenv('MAIL_FROM_ADDRESS')
EMAIL_USE_SSL = False

#SMS SERVICE
SMS_NUMBER = os.getenv('SMS_NUMBER')
SMS_USERNAME = os.getenv('SMS_USERNAME')
SMS_PASSWORD = os.getenv('SMS_PASSWORD')


RATE_LIMIT = {
    'GET': {
        'rate': '50/m',
        'method': ['GET'],
        'key': 'ip',
        'block': True
    },
    'POST': {
        'rate': '30/m',
        'method': ['POST'],
        'key': 'ip',
        'block': True
    },
    'PATCH': {
        'rate': '20/m',
        'method': ['PATCH'],
        'key': 'ip',
        'block': True
    },
    'DELETE': {
        'rate': '10/m',
        'method': ['DELETE'],
        'key': 'ip',
        'block': True
    }
}

