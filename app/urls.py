from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from allauth.account.views import LoginView

urlpatterns = [
    path('', views.index, name='home'),
    path('cadastro_roupa/', views.cadastro_roupa, name='CadastroRoupa'),
    path('roupa/<int:idroupa>', views.roupa_dinamico, name='roupa'),
    path('roupa/<int:idroupa>/alugar', views.aluguel, name='aluguel'),
     ]
