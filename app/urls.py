from django.urls import path, reverse  # Remova a vírgula aqui
from . import views
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import LoginView
from django.contrib.auth import views as auth_views
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView

urlpatterns = [
    path('', views.index, name='home'),
    path('cadastro_roupa/', views.cadastro_roupa, name='CadastroRoupa'),
    path('roupa/<int:idroupa>', views.roupa_dinamico, name='roupa'),
    path('meu_carrinho', views.meu_carrinho, name="meu_carrinho"),
    path('profile', views.user_profile, name='user_profile'),
    path('logout', views.logout_view, name='logout'),
    path('roupa/<int:idroupa>/alugar', views.aluguel, name='aluguel'),
    path('social/google-oauth2/', views.authorize_google, name='authorize_google'),
    path('google/callback/', views.google_callback, name='google_callback'),
]