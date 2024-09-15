from django.urls import path
from .views import WalletAdminViewset , WalletAdmin2Viewset , WalletViewset , Wallet2ViewSet


urlpatterns = [
    path('wallet/admin/', WalletAdminViewset.as_view(), name='wallet-admin'),
    path('wallet/admin/<int:id>/', WalletAdmin2Viewset.as_view(), name='wallet-admin'),
    path('wallet/' , WalletViewset.as_view() , name='wallet-user'),
    path('wallet/<int:id>/' , Wallet2ViewSet.as_view() , name='wallet-user'),
]
