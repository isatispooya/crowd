from django.urls import path
from.views import RequestViewset , DetailCartViewset


urlpatterns = [
    path('cart/', RequestViewset.as_view(), name='cart'),
    path('cart/', RequestViewset.as_view(), name='cart'),
    path('cart/detail/<int:id>/', DetailCartViewset.as_view(), name='cart-detail'),
]