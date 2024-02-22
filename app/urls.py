from django.urls import path, reverse  # Remova a vírgula aqui
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('cadastro_roupa/', views.cadastro_roupa, name='CadastroRoupa'),
    path('roupa/<int:idroupa>', views.roupa_dinamico, name='roupa'),
    path('meu_carrinho', views.meu_carrinho, name="meu_carrinho"),
    path('checkout', views.checkout, name="checkout"),
    path('profile', views.user_profile, name='user_profile'),
    path('logout', views.logout_view, name='logout'),
    path('roupa/<int:idroupa>/alugar', views.aluguel, name='aluguel')
]