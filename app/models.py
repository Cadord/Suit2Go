# This is not an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from .utils import generate_file_name


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

class Cor(models.Model):
    id = models.AutoField(primary_key=True)
    titulo=models.CharField(max_length=100)
    cor_code=models.CharField(max_length=8)

    class Meta:
        managed = True
        db_table = 'cor'

class Estilo(models.Model):
    id = models.AutoField(primary_key=True)
    titulo=models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'estilo'

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    titulo=models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'categoria'

class Tamanho(models.Model):
    id = models.AutoField(primary_key=True)
    titulo=models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'tamanho'

class Roupas(models.Model):
    id_roupas = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    estilo = models.ForeignKey(Estilo, on_delete=models.CASCADE)
    preco_aluguel = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disponibilidade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'roupas'

class FotosRoupas(models.Model):
    id = models.AutoField(primary_key=True)
    roupa = models.ForeignKey(Roupas, on_delete=models.CASCADE)
    fotoUrl = models.ImageField(upload_to=generate_file_name)
    ordem = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'fotosRoupa'

class ProdutoVariacao(models.Model):
    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Roupas, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    estilo = models.ForeignKey(Estilo, on_delete=models.CASCADE)
    preco_aluguel = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'produto_variacao'

class FotosRoupaVariacao(models.Model):
    id = models.AutoField(primary_key=True)
    variacao = models.ForeignKey(ProdutoVariacao, on_delete=models.CASCADE)
    fotoUrl = models.ImageField(upload_to=generate_file_name)
    ordem = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'fotos_roupa_variacao'