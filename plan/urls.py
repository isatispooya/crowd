from django.urls import path
from.views import PlansViewset, PlanViewset, DocumentationViewset, AppendicesViewset ,PaymentDocument, CommentAdminViewset , CommentViewset ,InformationPlanViewset,DocumationRecieveViewset   ,SendpicturePlanViewset , ParticipantViewset


urlpatterns = [

    path('plans/', PlansViewset.as_view(), name='plans'),
    path('plan/<str:trace_code>/', PlanViewset.as_view(), name='plan'),
    path('appendices/<str:trace_code>/', AppendicesViewset.as_view(), name='appendices-admin'),
    path('send/picture/<str:trace_code>/', SendpicturePlanViewset.as_view(), name='send-picture-admin'),
    path('documentation/<str:trace_code>/', DocumentationViewset.as_view(), name='documentation-admin'),
    path('comment/user/<str:trace_code>/', CommentViewset.as_view(), name='comment-user'),
    path('comment/admin/<str:trace_code>/', CommentAdminViewset.as_view(), name='comment-admin'),
    path('payment/document/<str:trace_code>/', PaymentDocument.as_view(), name='comment-admin'),
    path('participant/user/<str:trace_code>/', ParticipantViewset.as_view(), name='participant-user'),
    path('documation/recieve/admin/<int:id>/', DocumationRecieveViewset.as_view(), name='documation-recieve-admin'),
    path('information/plan/admin/<str:trace_code>/', InformationPlanViewset.as_view(), name='add-information-plan-admin'),

]