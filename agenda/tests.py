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
      Agendamento.objects.create(
         data_horario=datetime(2026, 1, 10, 14, 30, tzinfo=timezone.utc),
         nome_cliente="João Silva",
         email_cliente="joao.silva@email.com",
         telefone_cliente="11987654321",
      )

      agendamento_serializado = {
         "id": 1,
         "data_horario": "2026-01-10T14:30:00Z",
         "nome_cliente": "João Silva",
         "email_cliente": "joao.silva@email.com",
         "telefone_cliente": "11987654321"
      }
      response = self.client.get("/api/agendamentos/")
      data = json.loads(response.content)
      self.assertDictEqual(data[0], agendamento_serializado)
      
   
   def test_listagem_de_agendamentos_nao_cancelados(self):
      #Criar agendamento
      data = {
         "data_horario": "2026-01-12T15:30:00Z",
         "nome_cliente": "Léo",
         "email_cliente": "Leo@email.com",
         "telefone_cliente": "65481654877"
      }
      response = self.client.post("/api/agendamentos/", data, format="json")
      self.assertEqual(response.status_code, 201)
      #Listar agendamentos não cancelados
      response_get = self.client.get("/api/agendamentos/?cancelado=False")
      self.assertEqual(response_get.status_code, 200)
      
      
   def test_listagem_de_agendamentos_cancelados(self):
      #Criar agendamento
      data = {
         "data_horario": "2026-01-12T15:30:00Z",
         "nome_cliente": "Bruno",
         "email_cliente": "bruno@email.com",
         "telefone_cliente": "46358842555"
      }
      response = self.client.post("/api/agendamentos/", data, format="json")
      self.assertEqual(response.status_code, 201)
      #Listar agendamentos cancelados
      response_get = self.client.get("/api/agendamentos/?cancelado=True")
      self.assertEqual(response_get.status_code, 200)


class TestCriacaoAgendamento(APITestCase):
   def test_cria_agendamento(self):
      agendamento_request_data = {
         "data_horario": "2026-01-11T14:30:00Z",
         "nome_cliente": "João Silva",
         "email_cliente": "joao.silva@email.com",
         "telefone_cliente": "11987654321"
      }
      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")

      agendamento_criado = Agendamento.objects.get()
      self.assertEqual(response.status_code, 201)

      agendamento_data_horario = datetime(2026, 1, 11, 14, 30, tzinfo=timezone.utc)
      self.assertEqual(agendamento_criado.data_horario, agendamento_data_horario)
      self.assertEqual(agendamento_criado.nome_cliente, "João Silva")
      self.assertEqual(agendamento_criado.email_cliente, "joao.silva@email.com")
      self.assertEqual(agendamento_criado.telefone_cliente, "11987654321")


   def test_cria_agendamento_outra_forma(self):
      agendamento_request_data = {
         "data_horario": "2026-01-11T14:30:00Z",
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
      agendamento_request_data = {
         "data_horario": "2025-01-11T14:30:00Z",
         "nome_cliente": "jão",
         "email_cliente": "joao.silva@email.com.br",
         "telefone_cliente": "+11987654321"
      }

      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")

      self.assertEqual(response.status_code, 400)
      

class TestAgendamentoDetail(APITestCase):
   def test_detalhar_agendamento(self):
      data = {
         "data_horario": "2026-01-12T14:30:00Z",
         "nome_cliente": "Pedro",
         "email_cliente": "Pedro@email.com",
         "telefone_cliente": "47815189665"
      }

      response = self.client.post("/api/agendamentos/", data, format="json")
      self.assertEqual(response.status_code, 201)
      response_get = self.client.get("/api/agendamentos/1/")
      self.assertEqual(response_get.status_code, 200)
      
      
   def test_editar_agendamento(self):
      #Criar agendamento
      data = {
         "data_horario": "2026-01-12T15:30:00Z",
         "nome_cliente": "Luiz",
         "email_cliente": "Luiz@email.com",
         "telefone_cliente": "846548465464"
      }
      response = self.client.post("/api/agendamentos/", data, format="json")
      self.assertEqual(response.status_code, 201)
      # Editar agendamento
      patch_data = {"data_horario": "2026-01-13T10:00:00Z"}
      response_patch = self.client.patch("/api/agendamentos/1/", patch_data)
      self.assertEqual(response_patch.status_code, 200)
      #Detalhar agendamento
      response_get = self.client.get("/api/agendamentos/1/")
      self.assertEqual(response_get.status_code, 200)
      # Verificar se os dados foram editados
      response_data = response_get.json()
      self.assertEqual(response_data["data_horario"], "2026-01-13T10:00:00Z")
      self.assertEqual(response_data["nome_cliente"], "Luiz")
      
      
   def test_cancelar_agendamento(self):
      #Criar agendamento
      data = {
         "data_horario": "2026-01-12T18:30:00Z",
         "nome_cliente": "Alex",
         "email_cliente": "Alex@email.com",
         "telefone_cliente": "45321658784"
      }
      response = self.client.post("/api/agendamentos/", data, format="json")
      self.assertEqual(response.status_code, 201)
      #Cancelar agendamento
      response_post = self.client.post("/api/agendamentos/1/")
      self.assertEqual(response_post.status_code, 200)
      self.assertEqual(response_post.json()["detail"], "Agendamento cancelado com secesso.")
      #Verificar recancelamento
      response_recancel = self.client.post("/api/agendamentos/1/")
      self.assertEqual(response_recancel.status_code, 400)
      self.assertEqual(response_recancel.json()["detail"], "Agendamento já foi cancelado.")
      