from datetime import date
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
    data = models.DateField(default=date.today)

class Descricao(models.Model):
    id_descricao = models.AutoField(primary_key=True)
    id_fertilizante = models.IntegerField()
    descricao = models.TextField()

class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    tipo_fertilizante = models.TextField()
    data = models.DateField()
    id_descricao = models.ForeignKey(Descricao, on_delete=models.CASCADE, default=1)
    id_instancia = models.ForeignKey(Instancia, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=17)


class InstanciaCrop(models.Model):
    id_instancia = models.AutoField(primary_key=True)
    nome_instancia = models.TextField()
    temperatura = models.FloatField()
    umidade = models.FloatField()
    nitrogenio = models.IntegerField()
    potassio = models.IntegerField()
    fosforo = models.IntegerField()
    ph = models.FloatField()
    chuva = models.FloatField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField(default=date.today)

class DescricaoCrop(models.Model):
    id_descricao = models.AutoField(primary_key=True)
    id_fertilizante = models.IntegerField()
    descricao = models.TextField()

class ResultadoCrop(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    cultura = models.TextField()
    data = models.DateField(default=date.today)
    id_descricao = models.ForeignKey(DescricaoCrop, on_delete=models.CASCADE, default=1)
    id_instancia = models.ForeignKey(InstanciaCrop, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=17)

