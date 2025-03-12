from datetime import datetime
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer

from agenda.utils import get_horarios_disponiveis


class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        username = request.query_params.get("username", None)
        if request.user.username == username:
            return True
        return False
    
    
class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False


class AgendamentoList(generics.ListCreateAPIView):  # api/agendamentos/
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def get_queryset(self):
        # Recupera os parâmetros 'username' e 'deletado' da requisição
        username = self.request.query_params.get("username", None)
        deletado = self.request.query_params.get("deletado", None)
        renderer_classes = [JSONRenderer]  # Adicionando a renderização em JSON

        # Começa com todos os objetos
        queryset = Agendamento.objects.all()

        # Aplica o filtro por 'username', se fornecido
        if username is not None:
            queryset = queryset.filter(prestador__username=username)

        # Aplica o filtro por 'deletado', se fornecido
        if deletado is not None:
            if deletado.lower() == "true":
                queryset = queryset.filter(deletado=True)
            elif deletado.lower() == "false":
                queryset = queryset.filter(deletado=False)

        return queryset


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPrestador]
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def delete(self, request, *args, **kwargs):
        # Obtém o objeto de agendamento
        agendamento = self.get_object()
        
        # Marca o agendamento como deletado
        agendamento.deletado = True
        agendamento.save()
        
        return Response({"detail": "Agendamento deletado com sucesso."}, 204)
    
#adicionar permissao nessa view q apenas o admin tenha acesso
class PrestadorList(generics.ListAPIView): # api/agendamentos/
    serializer_class = PrestadorSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    
    
@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
        
    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)    
    
    
@api_view(http_method_names=["GET"])
def healthcheck(request):
    return Response({
        "status": "ok",
        "message": "Deploy feito!"        
     }, status=200)