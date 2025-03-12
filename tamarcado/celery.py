from celery import Celery


app = Celery('tamarcado', broker='redis://localhost:6379/0')
app.conf.broker_connection_retry_on_startup = True



@app.task
def soma(a, b):
   return a + b