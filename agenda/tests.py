from datetime import datetime
import json
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer


class TestListagemAgendamento(APITestCase):
    def setUp(self):
        # Criação do prestador para os testes
        self.prestador = User.objects.create_user(username="test_user", password="password123")

    def test_listagem_vazia(self):
        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_de_agendamentos_criados(self):
        data = {
            "data_horario": "2026-01-10T14:30:00Z",
            "nome_cliente": "João Silva",
            "email_cliente": "joao.silva@email.com",
            "telefone_cliente": "+5511987654321",
            "prestador": "test_user",
            "deletado": False,
        }

        response_post = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response_post.status_code, 201)

        response_get = self.client.get("/api/agendamentos/")
        self.assertEqual(response_get.status_code, 200)

        agendamento_serializado = AgendamentoSerializer(Agendamento.objects.first()).data
        self.assertDictEqual(response_get.data[0], agendamento_serializado)

    def test_listagem_de_agendamentos_deletados(self):
        data = {
            "data_horario": "2026-01-12T14:30:00Z",
            "nome_cliente": "Pedro",
            "email_cliente": "pedro@email.com",
            "telefone_cliente": "+554781518965",  # Certifique-se de que o formato é aceito
            "prestador": "test_user",  # Prestador deve ser criado no `setUp`
            "deletado": False,  # Inicialmente False, pois a deleção será testada
        }

        # Criação via POST
        response_post = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response_post.status_code, 201, response_post.json())  # Debugging extra para detalhes da falha

        # Recupera o ID do agendamento criado
        agendamento_id = response_post.data["id"]

        # Realiza a deleção lógica via DELETE
        response_delete = self.client.delete(f"/api/agendamentos/{agendamento_id}/")
        self.assertEqual(response_delete.status_code, 204)

        # Verifica se o agendamento aparece como deletado
        agendamento = Agendamento.objects.get(id=agendamento_id)
        self.assertTrue(agendamento.deletado)



class TestCriacaoAgendamento(APITestCase):
    def setUp(self):
        self.prestador = User.objects.create_user(username="test_user", password="password123")

    def test_cria_agendamento(self):
        data = {
            "data_horario": "2026-01-11T14:30:00Z",
            "nome_cliente": "João Silva",
            "email_cliente": "joao.silva@email.com",
            "telefone_cliente": "+5511987654321",
            "prestador": "test_user",
            "deletado": False,
        }
        response = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_cria_agendamento_outra_forma(self):
        data = {
            "data_horario": "2026-01-11T14:30:00Z",
            "nome_cliente": "Neymar",
            "email_cliente": "ney@email.com",
            "telefone_cliente": "+55154652187",
            "prestador": "test_user",
            "deletado": False,
        }
        response = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data["data_horario"], data["data_horario"])
        self.assertEqual(response_data["nome_cliente"], data["nome_cliente"])

    def test_quando_request_e_invalido_retorna_400(self):
        data = {
            "data_horario": "2025-01-11T14:30:00Z",
            "nome_cliente": "João",
            "email_cliente": "joao.silva@email.com.br",
            "telefone_cliente": "+5511987654321",
            "prestador": "test_user",
            "deletado": False,
        }

        response = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response.status_code, 400)


class TestAgendamentoDetail(APITestCase):
    def setUp(self):
        self.prestador = User.objects.create_user(username="test_user", password="password123")

    def test_detalhar_agendamento(self):
        data = {
            "data_horario": "2026-01-12T14:30:00Z",
            "nome_cliente": "Pedro",
            "email_cliente": "pedro@email.com",
            "telefone_cliente": "+554781518965",
            "prestador": "test_user",
            "deletado": False,
        }

        response = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response.status_code, 201)

        agendamento_id = response.data["id"]
        response_get = self.client.get(f"/api/agendamentos/{agendamento_id}/")
        self.assertEqual(response_get.status_code, 200)

    def test_editar_agendamento(self):
        data = {
            "data_horario": "2026-01-12T15:30:00Z",
            "nome_cliente": "Luiz",
            "email_cliente": "luiz@email.com",
            "telefone_cliente": "+554865486546",
            "prestador": "test_user",
            "deletado": False,
        }
        response = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response.status_code, 201)

        patch_data = {"data_horario": "2026-01-13T10:00:00Z"}
        agendamento_id = response.data["id"]
        response_patch = self.client.patch(f"/api/agendamentos/{agendamento_id}/", patch_data, format="json")
        self.assertEqual(response_patch.status_code, 200)

        response_get = self.client.get(f"/api/agendamentos/{agendamento_id}/")
        self.assertEqual(response_get.status_code, 200)

        response_data = response_get.json()
        self.assertEqual(response_data["data_horario"], "2026-01-13T10:00:00Z")
        self.assertEqual(response_data["nome_cliente"], "Luiz")

    def test_deletar_agendamento(self):
        data = {
            "data_horario": "2026-01-12T14:30:00Z",
            "nome_cliente": "Pedro",
            "email_cliente": "pedro@email.com",
            "telefone_cliente": "+554781518965",
            "prestador": "test_user",
            "deletado": False,
        }

        response_post = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response_post.status_code, 201)

        agendamento_id = response_post.data["id"]
        response_delete = self.client.delete(f"/api/agendamentos/{agendamento_id}/")
        self.assertEqual(response_delete.status_code, 204)

        agendamento = Agendamento.objects.get(id=agendamento_id)
        self.assertTrue(agendamento.deletado)
