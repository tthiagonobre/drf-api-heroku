from datetime import datetime, timezone
import json
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer


class TestListagemAgendamento(APITestCase):
    def setUp(self):
        # Criação do prestador para os testes
        self.prestador = User.objects.create_user(username="test_user", password="password123")
        self.outro_prestador = User.objects.create_user(username="other_user", password="123password")

    def test_listagem_vazia(self):
        # Autenticar o client com o prestador criado
        self.client.login(username="test_user", password="password123")
        
        response = self.client.get("/api/agendamentos/", {"username": "test_user"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, [])
      

    def test_listagem_de_agendamentos_criados(self): 
        # Autenticar o client com o prestador criado
        self.client.login(username="test_user", password="password123")
        
        data = {
            "data_horario": "2026-01-10T14:30:00Z",
            "nome_cliente": "João Silva",
            "email_cliente": "joao.silva@email.com",
            "telefone_cliente": "+5511987654321",
            "prestador": "test_user",
            "deletado": False,
        }
        # Criar o agendamento (POST)
        response_post = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response_post.status_code, 201)
        
        # Listar os agendamentos (GET) com o parâmetro 'username'
        response_get = self.client.get("/api/agendamentos/", {"username": "test_user"})
        self.assertEqual(response_get.status_code, 200)

        agendamento_serializado = AgendamentoSerializer(Agendamento.objects.first()).data
        data_recebida = response_get.data[0]
        self.assertDictEqual(data_recebida, agendamento_serializado)


    def test_listagem_de_agendamentos_deletados(self): 
        self.client.login(username="test_user", password="password123")
        
        data = {
            "data_horario": "2026-01-12T14:30:00Z",
            "nome_cliente": "Pedro",
            "email_cliente": "pedro@email.com",
            "telefone_cliente": "+554781518965", 
            "prestador": "test_user",  
            "deletado": False, 
        }

        # Criação via POST
        response_post = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response_post.status_code, 201, response_post.json())  

        # Recupera o ID do agendamento criado
        agendamento_id = response_post.data["id"]

        # Realiza a deleção lógica via DELETE
        response_delete = self.client.delete(f"/api/agendamentos/{agendamento_id}/")
        self.assertEqual(response_delete.status_code, 204)

        # Verifica se o agendamento aparece como deletado
        agendamento = Agendamento.objects.get(id=agendamento_id)
        self.assertTrue(agendamento.deletado)

        # Verifica se o agendamento deletado é retornado com o filtro 'deletado=true'
        response_get = self.client.get("/api/agendamentos/", {"username": "test_user", "deletado": "true"})
        self.assertEqual(response_get.status_code, 200)  


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
        self.client.login(username="test_user", password="password123")
        
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
        self.client.login(username="test_user", password="password123")
        
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
        self.client.login(username="test_user", password="password123")
        
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
        
    
    def test_usuario_nao_autenticado_nao_pode_acessar(self):
        response_get = self.client.get("/api/agendamentos/", format="json")
        self.assertEqual(response_get.status_code, 403)
        

    def test_usuario_nao_pode_listar_agendamentos_de_outro_prestador(self):
        self.client.login(username="test_user", password="password123")
        
        data = {
            "data_horario": "2026-01-12T14:30:00Z",
            "nome_cliente": "Kaio",
            "email_cliente": "kaio@email.com",
            "telefone_cliente": "+55452214584",
            "prestador": "other_user",
            "deletado": False,
        }
        
        response_get = self.client.get("/api/agendamentos/", {"username": "other_user"})
        self.assertEqual(response_get.status_code, 403)
        

class TestPrestadorList(APITestCase):
    def setUp(self):
        self.prestador = User.objects.create_superuser(username="test_user", password="password123")
        self.outro_prestador = User.objects.create_user(username="other_user", password="123password")
     
        
    def test_acesso_permitido_do_superuser(self):
        self.client.login(username="test_user", password="password123")
        
        data = {
            "data_horario": "2026-01-12T14:30:00Z",
            "nome_cliente": "Oscar",
            "email_cliente": "oscar@email.com",
            "telefone_cliente": "+555325845984",
            "prestador": "test_user",
            "deletado": False,
        }
        
        response_post = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response_post.status_code, 201)
        
        response_get = self.client.get("/api/prestadores/", {"username": "test_user"})
        self.assertEqual(response_get.status_code, 200)
        
        
    def test_acesso_negado_para_user_comum(self):
        self.client.login(username="other_user", password="123password")
        
        data = {
            "data_horario": "2026-01-12T14:30:00Z",
            "nome_cliente": "Paulo",
            "email_cliente": "paulo@email.com",
            "telefone_cliente": "+5578565215",
            "prestador": "test_user",
            "deletado": False,
        }
        
        response_post = self.client.post("/api/agendamentos/", data, format="json")
        self.assertEqual(response_post.status_code, 201)
        
        response_get = self.client.get("/api/prestadores/", {"username": "other_user"})
        self.assertEqual(response_get.status_code, 403)


    def test_acesso_negado_user_nao_autenticado(self):
        response_get = self.client.get("/api/prestadores/")
        self.assertEqual(response_get.status_code, 403)
        
from unittest import mock
class TestGetHorario(APITestCase):
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
    def test_quando_data_e_feriado_retorna_lista_vazia(self, _):
        response = self.client.get("/api/horarios/?data=2026-12-25")
        self.assertEqual(response.json(), [])

        
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=False)
    def test_quando_data_e_dia_comum_lista_com_horarios(self, _):
        response = self.client.get("/api/horarios/?data=2026-12-20")
        horarios = [datetime.fromisoformat(h) for h in response.json()] # Converte str em datetime
        
        self.assertNotEqual(response.json(), [])
        self.assertEqual(horarios[0], datetime(2026, 12, 20, 9, tzinfo=timezone.utc))
        self.assertEqual(horarios[-1], datetime(2026, 12, 20, 17, 30, tzinfo=timezone.utc))