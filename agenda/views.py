from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

# Create your views here.
class AgendamentoDetail(APIView):
   def get(self, request, id):
      obj = get_object_or_404(Agendamento, id=id)
      serializer = AgendamentoSerializer(obj)
      return JsonResponse(serializer.data) 
   
   
   def patch(self, request, id):
      obj = get_object_or_404(Agendamento, id=id)
      serializer = AgendamentoSerializer(obj, data=request.data, partial=True)#partial=True -> Aceita updates parciais
      if serializer.is_valid():
         serializer.save()    
         return JsonResponse(serializer.data, status=200)#success
      return JsonResponse(serializer.errors, status=400)#bad request
   
   
   def post(self, request, id):
      obj = get_object_or_404(Agendamento, id=id)
      if obj.is_canceled:
         return JsonResponse({"detail": "Agendamento já foi cancelado."}, status=400) # Evita recancelamento
      obj.is_canceled = True
      obj.save()
      return Response({"detail": "Agendamento cancelado com secesso."}, status=200)#No Content
   
   
class AgendamentoList(APIView):
   def get(self, request):
      cancelado = request.query_params.get("cancelado", None)
      if cancelado is not None:
         # Filtra os agendamentos com base no parâmetro 'cancelado'
         if cancelado.lower() == "true":
               qs = Agendamento.objects.filter(is_canceled=True)
         else:
               qs = Agendamento.objects.filter(is_canceled=False)
      else:
         # Retorna todos os agendamentos
         qs = Agendamento.objects.all()
      # Serializa os agendamentos
      serializer = AgendamentoSerializer(qs, many=True)
      return JsonResponse(serializer.data, safe=False)
   
   
   def post(self, request):
      data = request.data
      serializer = AgendamentoSerializer(data=data)
      if serializer.is_valid():
         serializer.save()
         return JsonResponse(serializer.data, status=201)
      return JsonResponse(serializer.errors, status=400)


#f090