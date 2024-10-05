from django.urls import path
from.views import PlansViewset, PlanViewset, DocumentationViewset, AppendicesViewset,PaymentDocument,EndOfFundraisingViewset, CommentAdminViewset , CommentViewset ,InformationPlanViewset   ,SendpicturePlanViewset , ParticipantViewset , SendPaymentToFarabours


urlpatterns = [

    path('plans/', PlansViewset.as_view(), name='plans'),
    path('plan/<str:trace_code>/', PlanViewset.as_view(), name='plan'),
    path('appendices/<str:trace_code>/', AppendicesViewset.as_view(), name='appendices-admin'),
    path('send/picture/<str:trace_code>/', SendpicturePlanViewset.as_view(), name='send-picture-admin'),
    path('documentation/<str:trace_code>/', DocumentationViewset.as_view(), name='documentation-admin'),
    path('comment/user/<str:trace_code>/', CommentViewset.as_view(), name='comment-user'),
    path('comment/admin/<str:trace_code>/', CommentAdminViewset.as_view(), name='comment-admin'),
    path('payment/document/<str:trace_code>/', PaymentDocument.as_view(), name='payment-admin'),
    path('participant/user/<str:trace_code>/', ParticipantViewset.as_view(), name='participant-user'),
    path('information/plan/admin/<str:trace_code>/', InformationPlanViewset.as_view(), name='add-information-plan-admin'),
    path('end/fundraising/admin/<str:trace_code>/', EndOfFundraisingViewset.as_view(), name='end-fundraising-plan-admin'),
    path('send/payment/farabours/admin/<str:trace_code>/', SendPaymentToFarabours.as_view(), name='send-payment-faravours-admin'),

]