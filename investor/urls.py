from django.urls import path
from.views import RequestViewset , DetailCartViewset , CartAdmin , DetailCartAdminViewset


urlpatterns = [
    path('cart/', RequestViewset.as_view(), name='cart'),
    path('cart/', RequestViewset.as_view(), name='cart'),
    path('cart/detail/<int:id>/', DetailCartViewset.as_view(), name='cart-detail'),
    path('cart/admin/', CartAdmin.as_view(), name='cart-admin'),
    path('cart/admin/<int:id>/', CartAdmin.as_view(), name='cart-admin'),
    path('cart/detail/admin/<int:id>/', DetailCartAdminViewset.as_view(), name='cart-admin'),
]
