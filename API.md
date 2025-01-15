# API

- Listar horarios: GET /horarios/ 
- Listar agendamentos: GET /agendamentos/ #f
- Detalhar agendamento: GET /agendamento/<id>/ #f
- Criar agendamento: POST /agendamentos/
- Excluir agendamento: DELETE /agendamento/<id>/
- Editar agendamento: PUT /agendamento/<id>/


# Autorizations
-> Qualquer cliente (autenticado ou não) pode ser capaz de criar um Agendamento.
   -> Apenas o prestador de serviço pode visualizar todos os agendamentos em sua agenda.
   -> Apenas o prestador de serviço pode manipular os seus agendamentos.