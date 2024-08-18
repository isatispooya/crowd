from django.urls import path
from.views import RequestViewset


urlpatterns = [
    path('cart/', RequestViewset.as_view(), name='cart'),
]