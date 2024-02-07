# This is not an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime
from django.contrib import admin
from allauth.socialaccount.models import SocialApp

class Clientes(models.Model):
    id_clientes = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    telefone = models.CharField(max_length=200, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'clientes'


class Locacoes(models.Model):
    cliente_id = models.IntegerField(blank=True, null=True)
    roupa_id = models.IntegerField(blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_termino = models.DateField(blank=True, null=True)
    valor_aluguel = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'locacoes'


class Roupas(models.Model):
    id_roupas = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.CharField(max_length=200, blank=True, null=True)
    tamanho = models.CharField(max_length=200, blank=True, null=True)
    cor = models.CharField(max_length=200, blank=True, null=True)
    estilo = models.CharField(max_length=200, blank=True, null=True)
    preco_aluguel = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disponibilidade = models.IntegerField(blank=True, null=True)
    foto = models.ImageField(upload_to='%Y/%m/%d/', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'roupas'

class FotosRoupas(models.Model):
    id = models.AutoField(primary_key=True)
    roupa_id = models.IntegerField(blank=True, null=True)
    fotoUrl = models.ImageField(upload_to='%Y/%m/%d/')
    ordem = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'fotosRoupa'

class SocialAppAdmin(admin.ModelAdmin):
    list_display = ('provider', 'name', 'client_id', 'secret', 'sites')
    search_fields = ('provider',)