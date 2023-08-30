from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Instancia(models.Model):
    id_instancia = models.AutoField(primary_key=True)
    nome_instancia = models.TextField()
    temperatura = models.IntegerField()
    umidade_ar = models.IntegerField()
    umidade_solo = models.IntegerField()
    tipo_solo = models.IntegerField()
    tipo_cultura = models.IntegerField()
    nitrogenio = models.IntegerField()
    potassio = models.IntegerField()
    fosforo = models.IntegerField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    tipo_fertilizante = models.IntegerField()
    data = models.DateField()
    description = models.TextField()
    id_instancia = models.ForeignKey(Instancia, on_delete=models.CASCADE)       