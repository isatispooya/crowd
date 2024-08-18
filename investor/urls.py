from django.urls import path
from.views import RequestViewset , DetailViewset


urlpatterns = [
    path('cart/', RequestViewset.as_view(), name='cart'),
    path('cart/list/', RequestViewset.as_view(), name='cart_list'),
    path('cart/detail/<int:id>', DetailViewset.as_view(), name='cart_detail'),
]