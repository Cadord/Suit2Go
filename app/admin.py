from django.contrib import admin
from app.models import Roupas,Categoria,Cor,Estilo,Tamanho,ProdutoVariacao,FotosRoupas,FotosRoupaVariacao,Clientes,Locacoes,ItensLocacao

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Cor)
admin.site.register(Estilo)
admin.site.register(Tamanho)
admin.site.register(Clientes)
admin.site.register(Locacoes)
admin.site.register(ItensLocacao)

class FotosRoupasAdmin(admin.StackedInline):
    model = FotosRoupas

class FotosRoupaVariacaoAdmin(admin.StackedInline):
    model = FotosRoupaVariacao

@admin.register(Roupas)
class RoupasAdmin(admin.ModelAdmin):
    list_display=("id_roupas", "nome", "categoria","estilo")
    inlines = [FotosRoupasAdmin]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
    
    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

@admin.register(ProdutoVariacao)
class ProdutoVariacaoAdmin(admin.ModelAdmin):
    list_display=('id', 'produto', 'preco_aluguel', 'cor', 'tamanho')
    inlines = [FotosRoupaVariacaoAdmin]