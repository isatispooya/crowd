from django.urls import path
from.views import RequestViewset , DetailCartViewset , CartAdmin , DetailCartAdminViewset , MessageAdminViewSet , MessageUserViewSet , SetStatusViesset , SetStatusAdminViesset, AddInformationViewset , AddInfromationAdminViewset, PdfViewset
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cart/', RequestViewset.as_view(), name='cart'),
    path('cart/', RequestViewset.as_view(), name='cart'),
    path('cart/detail/<int:id>/', DetailCartViewset.as_view(), name='cart-detail'),
    path('cart/admin/', CartAdmin.as_view(), name='cart-admin'),
    path('cart/admin/<int:id>/', CartAdmin.as_view(), name='cart-admin'),
    path('cart/detail/admin/<int:id>/', DetailCartAdminViewset.as_view(), name='cart-admin'),
    path('message/admin/<int:id>/', MessageAdminViewSet.as_view(), name='message-admin'),
    path('message/<int:id>/', MessageUserViewSet.as_view(), name='message-user'),
    path('setstatus/<int:id>/', SetStatusViesset.as_view(), name='set-status'),
    path('setstatus/admin/<int:id>/', SetStatusAdminViesset.as_view(), name='set-status-admin'),
    path('setstatus/admin/', SetStatusAdminViesset.as_view(), name='set-status-admin'),
    path('addinformation/<int:id>/', AddInformationViewset.as_view(), name='add-information'),
    path('addinformation/admin/<int:id>/', AddInfromationAdminViewset.as_view(), name='add-information-admin'),
    path('pdf/<int:id>/', PdfViewset.as_view(), name='pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
