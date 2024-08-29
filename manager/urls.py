from django.urls import path
from.views import ManagerViewset , ManagerAdminViewset


urlpatterns = [
    path('manager/<int:id>/', ManagerViewset.as_view(), name='manager'),
    path('manager/', ManagerViewset.as_view(), name='manager-list'),
    path('manager/admin/', ManagerAdminViewset.as_view(), name='manager-list-admin'),
    path('manager/admin/<int:id>/', ManagerAdminViewset.as_view(), name='manager-update-admin'),
]