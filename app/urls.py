from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from allauth.account.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('cadastro_roupa/', views.cadastro_roupa, name='CadastroRoupa'),
    path('roupa/<int:idroupa>', views.roupa_dinamico, name='roupa'),
    path('meu_carrinho', views.meu_carrinho, name="meu_carrinho"),
    path('profile', views.user_profile, name='user_profile'),
    path('logout', views.logout_view, name='logout'),
    path('roupa/<int:idroupa>/alugar', views.aluguel, name='aluguel'),
    ]
