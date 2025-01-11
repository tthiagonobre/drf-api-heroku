from datetime import datetime, timezone
import json
from rest_framework.test import APITestCase

from agenda.models import Agendamento

# Create your tests here.
class TestListagemAgendamento(APITestCase):
   def test_listagem_vazia(self):
      response = self.client.get("/api/agendamentos/")
      data = json.loads(response.content)
      self.assertEqual(data, [])


   def test_listagem_de_agendamentos_criados(self):
      #criar um agendamento e verficar que a resposta seja uma resposta esperada
      Agendamento.objects.create(
         data_horario=datetime(2025, 1, 10, 14, 30, tzinfo=timezone.utc),
         nome_cliente="João Silva",
         email_cliente="joao.silva@email.com",
         telefone_cliente="11987654321",
      )

      agendamento_serializado = {
         "id": 1,
         "data_horario": "2025-01-10T14:30:00Z",
         "nome_cliente": "João Silva",
         "email_cliente": "joao.silva@email.com",
         "telefone_cliente": "11987654321"
      }
      response = self.client.get("/api/agendamentos/")
      data = json.loads(response.content)
      self.assertDictEqual(data[0], agendamento_serializado)


class TestCriacaoAgendamento(APITestCase):
   def test_cria_agendamento(self):
      agendamento_request_data = {
         "data_horario": "2025-01-11T14:30:00Z",
         "nome_cliente": "João Silva",
         "email_cliente": "joao.silva@email.com",
         "telefone_cliente": "11987654321"
      }

      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")

      agendamento_criado = Agendamento.objects.get()
      self.assertEqual(response.status_code, 201)

      agendamento_data_horario = datetime(2025, 1, 11, 14, 30, tzinfo=timezone.utc)
      self.assertEqual(agendamento_criado.data_horario, agendamento_data_horario)
      self.assertEqual(agendamento_criado.nome_cliente, "João Silva")
      self.assertEqual(agendamento_criado.email_cliente, "joao.silva@email.com")
      self.assertEqual(agendamento_criado.telefone_cliente, "11987654321")


   def test_cria_agendamento_outra_forma(self):
      agendamento_request_data = {
         "data_horario": "2025-01-11T14:30:00Z",
         "nome_cliente": "Neymar",
         "email_cliente": "Ney@email.com",
         "telefone_cliente": "154652187"
      }

      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
      response_get = self.client.get("/api/agendamentos/")
      self.assertEqual(response_get.status_code, 200)
      
      # Dados da resposta POST
      response_data = response.json()
      
      self.assertEqual(response_data["data_horario"], agendamento_request_data["data_horario"])
      self.assertEqual(response_data["nome_cliente"], agendamento_request_data["nome_cliente"])
      

   def test_quando_request_e_invalido_retorna_400(self):
      """
         agendamento_request_data = {
         "data_horario": "2025-01-11T14:30:00Z",
         "nome_cliente": "Neymar",
         "email_cliente": "Ney@email.com",
         "telefone_cliente": "154652187"
      }
      Alterar essa req de alguma maneira que ela seja inválida
      não vai criar obj no banco
      e o statuscode vai ser 400
      """
      agendamento_request_data = {
         "data_horario": "2025-01-11T14:30:00Z",
         "nome_cliente": "jão",
         "email_cliente": "joao.silva@email.com.br",
         "telefone_cliente": "+11987654321"
      }

      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")

      self.assertEqual(response.status_code, 400)