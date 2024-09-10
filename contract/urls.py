from django.urls import path
from.views import SignatureViewset , SetSignatureViewset , SetCartAdminViewset , SetCartUserViewset
from django.conf import settings
urlpatterns = [
    path('signature/<int:id>/', SignatureViewset.as_view(), name='signature-company'),
    path('setsignature/admin/<int:id>/', SetSignatureViewset.as_view(), name='set-signature-admin'),
    path('setcart/admin/<int:id>/', SetCartAdminViewset.as_view(), name='set-cart-admin'),
    path('setcart/<int:id>/', SetCartUserViewset.as_view(), name='set-cart-user'),

]