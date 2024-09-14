from django.urls import path
from.views import PlanAdminViewset , PlanAdmin2Viewset , PlanViewset , Plan2Viewset


urlpatterns = [
    path('plan/admin/', PlanAdminViewset.as_view(), name='plan-admin'),
    path('plan/admin/<int:id>/', PlanAdmin2Viewset.as_view(), name='plan-admin'),
    path('plan/', PlanViewset.as_view(), name='plan-user'),
    path('plan/<int:id>/', Plan2Viewset.as_view(), name='plan-user'),
]