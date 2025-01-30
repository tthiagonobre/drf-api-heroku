from django.urls import path
from agenda.views import AgendamentoDetail, AgendamentoList, PrestadorList, get_horarios, healthcheck

urlpatterns = [
   path('agendamentos/', AgendamentoList.as_view()),
   path('agendamentos/<int:pk>/', AgendamentoDetail.as_view(), name='agendamento_detail'),
   path('horarios/', get_horarios),
   path('prestadores/', PrestadorList.as_view()),
   path('', healthcheck),
]
