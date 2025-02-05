from django.urls import path
from.views import CaptchaViewset,OtpViewset,OneTimeLoginViewset,LoginViewset,OtpAdminViewset,RegisterFromSpaceViewset,UserOneViewset,LogoutViewset,AddBoursCodeUserViewset,LoginAdminViewset , InformationViewset, UserListViewset , OtpUpdateViewset, UpdateInformationViewset, RefreshTokenAdminViewset

urlpatterns = [
    path('captcha/', CaptchaViewset.as_view(), name='captcha'),
    path('otp/', OtpViewset.as_view(), name='otp'),
    path('login/', LoginViewset.as_view(), name='login'),
    path('information/', InformationViewset.as_view(), name='information'),
    path('information/user/admin/<int:id>/', UserOneViewset.as_view(), name='information-user-for-admin'),
    path('login/admin/', LoginAdminViewset.as_view(), name='login-admin'),
    path('otp/admin/', OtpAdminViewset.as_view(), name='otp-admin'),
    path('listuser/admin/', UserListViewset.as_view(), name='list-user-admin'),
    path('otp/update/', OtpUpdateViewset.as_view(), name='otp-update-profile'),
    path('update/profile/', UpdateInformationViewset.as_view(), name='update-profile'),
    path('add/bours/code/user/', AddBoursCodeUserViewset.as_view(), name='add-bours-code-user'),
    path('log/out/', LogoutViewset.as_view(), name='log-out'),
    path('refresh/token/admin/', RefreshTokenAdminViewset.as_view(), name='refresh-token-admin'),
    path('onetime/login/', OneTimeLoginViewset.as_view(), name='onetime-login'),
    path('onetime/login/<str:uuid>/', OneTimeLoginViewset.as_view(), name='onetime-login-admin'),
    path('register-from-space/', RegisterFromSpaceViewset.as_view(), name='register-from-space'),


]