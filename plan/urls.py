from django.urls import path
from.views import PlanAdminViewset , PlanAdmin2Viewset , PlanViewset , Plan2Viewset ,DocumentationAdminViewset , AppendicesAdminViewset ,DocumentationViewset , AppendicesViewset


urlpatterns = [
    path('plan/admin/', PlanAdminViewset.as_view(), name='plan-admin'),
    path('plan/admin/<int:id>/', PlanAdmin2Viewset.as_view(), name='plan-admin'),
    path('plan/', PlanViewset.as_view(), name='plan-user'),
    path('plan/<int:id>/', Plan2Viewset.as_view(), name='plan-user'),
    path('documentation/admin/<int:id>/', DocumentationAdminViewset.as_view(), name='documentation-admin'),
    path('appendices/admin/<int:id>/', AppendicesAdminViewset.as_view(), name='appendices-admin'),
    path('documentation/<int:id>/', DocumentationViewset.as_view(), name='documentation-user'),
    path('appendices/<int:id>/', AppendicesViewset.as_view(), name='appendices-user'),
]