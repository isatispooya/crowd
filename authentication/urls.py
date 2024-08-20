from django.urls import path
from.views import CaptchaViewset,OtpViewset,LoginViewset,OtpAdminViewset,LoginAdminViewset,SignUpViewset

urlpatterns = [
    path('captcha/', CaptchaViewset.as_view(), name='captcha'),
    path('otp/', OtpViewset.as_view(), name='otp'),
    path('login/', LoginViewset.as_view(), name='login'),
    path('signup/', SignUpViewset.as_view(), name='signup'),
    path('login/admin/', LoginAdminViewset.as_view(), name='login-admin'),
    path('otp/admin/', OtpAdminViewset.as_view(), name='otp-admin'),
]