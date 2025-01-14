from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

# Create your views here.
class AgendamentoList(generics.ListCreateAPIView): # api/agendamentos/
   queryset = Agendamento.objects.all()
   serializer_class = AgendamentoSerializer
   
   
   def get_queryset(self):
      # Recupera o parâmetro 'cancelado' da requisição
      cancelado = self.request.query_params.get("cancelado", None)
      if cancelado is not None:
         # Filtra os agendamentos com base no parâmetro 'cancelado'
         if cancelado.lower() == "true":
               return Agendamento.objects.filter(is_canceled=True)
         else:
               return Agendamento.objects.filter(is_canceled=False)
      return super().get_queryset()



class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView): #api/agendamentos/<pk>/
   queryset = Agendamento.objects.all()
   serializer_class = AgendamentoSerializer
   
        
   def post(self, request, *args, **kwargs):
      obj = self.get_object()  # Usa o get_object para buscar o agendamento
      if obj.is_canceled:
         return JsonResponse({"detail": "Agendamento já foi cancelado."}, status=400) # Evita recancelamento
      obj.is_canceled = True
      obj.save()
      return Response({"detail": "Agendamento cancelado com secesso."}, status=200)#No Content
   
   


#f094