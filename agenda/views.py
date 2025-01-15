from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer


class AgendamentoList(generics.ListCreateAPIView):  # api/agendamentos/
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        # Recupera os parâmetros 'username' e 'deletado' da requisição
        username = self.request.query_params.get("username", None)
        deletado = self.request.query_params.get("deletado", None)

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
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def delete(self, request, *args, **kwargs):
        # Obtém o objeto de agendamento
        agendamento = self.get_object()
        
        # Marca o agendamento como deletado (deleção lógica)
        agendamento.deletado = True
        agendamento.save()
        
        return Response({"detail": "Agendamento deletado com sucesso."}, 204)

#f097