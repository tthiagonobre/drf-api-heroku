from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

# Create your views here.
@api_view(http_method_names=["GET", "PATCH", "POST"]) #api que retorna objs de JSON
def agendamento_detail(request, id):
   obj = get_object_or_404(Agendamento, id=id)
   if request.method == "GET":
      serializer = AgendamentoSerializer(obj)
      return JsonResponse(serializer.data) 
   
   if request.method == "PATCH":

      serializer = AgendamentoSerializer(obj, data=request.data, partial=True)#partial=True -> Aceita updates parciais
      if serializer.is_valid():
         serializer.save()    
         return JsonResponse(serializer.data, status=200)#success
      return JsonResponse(serializer.errors, status=400)#bad request
   
   if request.method == "POST":
      
      if obj.is_canceled:
         return JsonResponse({"detail": "Agendamento já foi cancelado"}, status=400) # Evita recancelamento
      obj.is_canceled = True
      obj.save()
      return Response({"detail": "Agendamento cancelado com secesso."}, status=200)#No Content
         

@api_view(http_method_names=["GET", "POST"])
def agendamento_list(request):
   if request.method == "GET":
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

   if request.method == "POST":
      data = request.data
      serializer = AgendamentoSerializer(data=data)
      if serializer.is_valid():
         serializer.save()
         return JsonResponse(serializer.data, status=201)
      return JsonResponse(serializer.errors, status=400)

   
      
#f089