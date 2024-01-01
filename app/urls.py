from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('cadastro_roupa/', views.cadastro_roupa, name='CadastroRoupa'),
    path('roupa/<int:idroupa>', views.roupa_dinamico, name='roupa'),
]
