from datetime import date
import requests
from django.conf import settings
import logging

def is_feriado(data: date) -> bool:
   logging.info(f"Fazendo requisição para BrasilAPI para a data: {data.isoformat()}")
   if settings.TESTING == True:
      logging.info("Requisição não está sendo feita pois TESTING = True")
      if data.day == 25 and data.month == 12:
         return True
      return False
   
   ano = data.year
   r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
   if not r.status_code == 200:
      logging.error("Algum erro ocorreu na Brasil API")
      return False
      # raise ValueError("Não foi possível consultar os feriados!")
      
   # {'date': '2025-01-01', 'name': 'Confraternização mundial', 'type': 'national'}
   feriados = r.json()
   for feriado in feriados:
      data_feriado_as_str = feriado["date"]
      data_feriado = date.fromisoformat(data_feriado_as_str)
      if data == data_feriado:
         return True
   
   return False