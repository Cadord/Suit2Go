from django.contrib import admin
from app.models import Roupas,Categoria,Cor,Estilo,Tamanho,ProdutoVariacao,FotosRoupas,FotosRoupaVariacao

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Cor)
admin.site.register(Estilo)
admin.site.register(Tamanho)

class FotosRoupasAdmin(admin.StackedInline):
    model = FotosRoupas

class FotosRoupaVariacaoAdmin(admin.StackedInline):
    model = FotosRoupaVariacao

@admin.register(Roupas)
class RoupasAdmin(admin.ModelAdmin):
    list_display=("id_roupas", "nome", "categoria","tamanho","cor","estilo","preco_aluguel","disponibilidade")
    inlines = [FotosRoupasAdmin]


@admin.register(ProdutoVariacao)
class ProdutoVariacaoAdmin(admin.ModelAdmin):
    list_display=('id', 'produto', 'preco_aluguel', 'categoria', 'cor', 'tamanho', 'estilo')
    inlines = [FotosRoupaVariacaoAdmin]