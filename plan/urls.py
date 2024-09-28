from django.urls import path
from.views import PlanAdminViewset , PlanAdmin2Viewset , PlanViewset , Plan2Viewset ,DocumentationAdminViewset , AppendicesAdminViewset ,DocumentationViewset , AppendicesViewset , ParticipantViewset , ParticipantAdminViewset , CommentAdminViewset , CommentViewset , DocumationRecieveViewset , CertificateViewset ,RoadMapViewset, SetFileParticipantViewSet


urlpatterns = [
    path('plan/admin/', PlanAdminViewset.as_view(), name='plan-admin'),
    path('plan/admin/<int:id>/', PlanAdmin2Viewset.as_view(), name='plan-admin'),
    path('plan/', PlanViewset.as_view(), name='plan-user'),
    path('plan/<int:id>/', Plan2Viewset.as_view(), name='plan-user'),
    path('documentation/admin/<int:id>/', DocumentationAdminViewset.as_view(), name='documentation-admin'),
    path('appendices/admin/<int:id>/', AppendicesAdminViewset.as_view(), name='appendices-admin'),
    path('documentation/<int:id>/', DocumentationViewset.as_view(), name='documentation-user'),
    path('appendices/<int:id>/', AppendicesViewset.as_view(), name='appendices-user'),
    path('participant/<int:id>/', ParticipantViewset.as_view(), name='participant-user'),
    path('participant/admin/<int:id>/', ParticipantAdminViewset.as_view(), name='participant-admin'),
    path('comment/admin/<int:id>/', CommentAdminViewset.as_view(), name='comment-admin'),
    path('documation/recieve/admin/<int:id>/', DocumationRecieveViewset.as_view(), name='documation-recieve-admin'),
    path('comment/<int:id>/', CommentViewset.as_view(), name='comment-user'),
    path('certificate/', CertificateViewset.as_view(), name='certificate-user'),
    path('roadmap/<int:id>/', RoadMapViewset.as_view(), name='roadmap-user'),
    path('set/participant/<int:id>/', SetFileParticipantViewSet.as_view(), name='set-file-participant-user'),
]