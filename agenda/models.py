from django.db import models

class Agendamento(models.Model):
    prestador = models.ForeignKey("auth.User", related_name="agendamentos", on_delete=models.CASCADE)
    data_horario = models.DateTimeField()
    nome_cliente = models.CharField(max_length=200)
    email_cliente = models.EmailField()
    telefone_cliente = models.CharField(max_length=20)
    deletado = models.BooleanField(default=False) 
