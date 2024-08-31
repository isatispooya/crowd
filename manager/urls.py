from django.urls import path
from.views import ManagerViewset , ManagerAdminViewset , ResumeViewset , ResumeAdminViewset , ShareholderViewset , ShareholderAdminViewset


urlpatterns = [
    path('manager/<int:id>/', ManagerViewset.as_view(), name='manager'),
    path('manager/', ManagerViewset.as_view(), name='manager-list'),
    path('manager/admin/', ManagerAdminViewset.as_view(), name='manager-list-admin'),
    path('manager/admin/<int:id>/', ManagerAdminViewset.as_view(), name='manager-update-admin'),
    path('resume/<int:id>/', ResumeViewset.as_view(), name='resume'),
    path('resume/admin/', ResumeAdminViewset.as_view(), name='resume-admin'),
    path('shareholder/<int:id>/', ShareholderViewset.as_view(), name='shareholder'),
    path('shareholder/admin/<int:id>/', ShareholderAdminViewset.as_view(), name='shareholder-admin'),
]