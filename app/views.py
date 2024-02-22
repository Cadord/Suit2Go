from .models import Roupas, ProdutoVariacao
from .forms import RoupasForms, DateForm
from .utils import connect_to_calendar
from datetime import datetime, time, timedelta, date
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import MultipleObjectsReturned
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from time import sleep
from allauth.socialaccount.signals import social_account_added, social_account_updated
from allauth.socialaccount.models import SocialToken, SocialAccount
from social_django.utils import psa
import ast
import logging
import json

logger = logging.getLogger(__name__)

#event = {
 #       'summary': f'{procedure.capitalize()}',
  #      'start': {
   #         'dateTime': f'{data_tempo.year}-{data_tempo.month}-{data_tempo.day}T{data_tempo.hour}:{data_tempo.minute}:00-03:00',
    #        'timeZone': 'America/Sao_Paulo',
     #   },
      #  'end': {
       #     'dateTime': f'{novo_data.year}-{novo_data.month}-{novo_data.day}T{novo_data.hour}:{novo_data.minute}:00-03:00',
        #    'timeZone': 'America/Sao_Paulo'
        #}

            #}
    #service.events().insert(calendarId='primary', body=event).execute()
# SCOPES = ['https://www.googleapis.com/auth/calendar.events']
# creds = None

# if os.path.exists('token.json'):
#     creds = Credentials.from_authorized_user_file('token.json')
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             'client_secret_860607395602-kldpfn6g61u968u3gop43jiu8b24bsfq.apps.googleusercontent.com.json', SCOPES 
#             )
#         creds = flow.run_local_server(port=0)
#     with open('token.json', 'w') as token:
#         token.write(creds.to_json())
# service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)


# Create your views here.
def obter_token_google(request):
    # Obter o token de acesso do usuário logado
    social_token = SocialToken.objects.get(account__user=request.user, account__provider='google')

    # Verificar se o token ainda é válido (opcional)
    if not social_token.expires_at or social_token.expires_at > timezone.now():
        # Obter o ID Token do Google
        id_token_info = id_token.verify_oauth2_token(
            social_token.token,
            Request(),
            social_token.app.client_id
        )

        # O token de acesso pode ser extraído assim
        access_token = social_token.token

        # Você também pode extrair informações adicionais do ID Token, se necessário
        user_id = id_token_info.get('sub')

        return access_token



def index(request):
    query = request.GET.get('q', '')
    roupas = Roupas.objects.all()
    precos = ProdutoVariacao.objects.all()
    roupas_enumeradas = list(enumerate(roupas))
    ultimas_roupas_query = Roupas.objects
    if (query):
        ultimas_roupas_query = ultimas_roupas_query.filter(Q(nome__icontains=query))
    ultimas_roupas = ultimas_roupas_query.order_by('nome').all

    context = {
        "roupas": ultimas_roupas,
        'roupas_enumeradas':roupas_enumeradas,
        'precos':precos
    }

    return render(request, "index.html",context)

@receiver(social_account_added)
@receiver(social_account_updated)
def handle_google_login(sender, request, sociallogin, **kwargs):
    if sociallogin.account.provider == 'google':
        # O código aqui será executado quando um usuário fizer login usando o provedor Google.
        # Você pode usar as credenciais do OAuth obtidas do Google para interagir com o Google Calendar API.
        # social_token = sociallogin.account.socialtoken_set.first()
        # google_access_token = social_token.token
        # google_refresh_token = social_token.token_secret
        pass


def cadastro_roupa(request):
    if request.method == 'POST':
        form = RoupasForms(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            form = RoupasForms()
            # return render(request, template_name='index.html')
        else:
            print(form.errors)

    else:
        form = RoupasForms()
    context = {'form': form}
    return render(request, template_name='cadastro_roupa.html', context=context)

def roupa_dinamico(request, idroupa):
    roupa = Roupas.objects.get(id_roupas=idroupa)
    cores = set()
    for produto_variacao in ProdutoVariacao.objects.select_related('cor').filter(produto=idroupa):
        cores.add(produto_variacao.cor)
    tamanhos = set()
    for produto_variacao in ProdutoVariacao.objects.select_related('tamanho').filter(produto=idroupa):
        tamanhos.add(produto_variacao.tamanho)
    variacoes = ProdutoVariacao.objects.select_related('cor').select_related('tamanho').filter(produto=idroupa)
    context = {'roupa': roupa, 'selected': {}, 'variacoes': variacoes, 'cores': cores, 'tamanhos': tamanhos}
    return render(request, 'roupa.html', context)

def aluguel(request, idroupa):
    form = DateForm()

    if request.method == 'POST':
        formulario = DateForm(request.POST)

        if formulario.is_valid():
            if request.user.is_authenticated:
                try:
                    # Obtendo o token de acesso do SocialAccount
                    social_account = SocialAccount.objects.get(user=request.user, provider='google')
                    access_token = social_account.socialtoken_set.get(account=social_account).token

                    # Utilizando o token de acesso para construir as credenciais
                    credentials = Credentials.from_authorized_user_info(
                        {'access_token': access_token},
                        scopes=['https://www.googleapis.com/auth/calendar'],
                    )

                    # Construindo o serviço da API do Google Calendar
                    service = build('calendar', 'v3', credentials=credentials)

                    data_1 = formulario.cleaned_data['date_1']
                    hora_1 = formulario.cleaned_data['time_1']
                    endereco = formulario.cleaned_data['endereco']

                    data_tempo = datetime.combine(data_1, hora_1)
                    evento = {
                        'summary': endereco,
                        'start': {
                            'dateTime': (data_tempo - timedelta(hours=3)).isoformat(),
                            'timeZone': 'America/Sao_Paulo',
                        },
                        'end': {
                            'dateTime': (data_tempo + timedelta(hours=1)).isoformat(),
                            'timeZone': 'America/Sao_Paulo',
                        },
                    }

                    # Restante do seu código para criar o evento no Google Calendar...
                    service.events().insert(calendarId='primary', body=evento).execute()
                    messages.success(request, 'Evento no Google Calendar criado com sucesso!')
                except SocialAccount.DoesNotExist:
                    messages.error(request, "Erro ao criar evento")

    return render(request, 'alugar.html', {'form': form, 'roupa': Roupas.objects.get(id_roupas=idroupa)})

def home(request):
    social_accounts = SocialAccount.objects.filter(user=request.user)
    
    if social_accounts.exists():
        # Assumindo que você está interessado apenas na conta do Google
        google_account = social_accounts.filter(provider='google').first()
        access_token = social_account.socialtoken_set.get(account=social_account).token
        user_name = google_account.extra_data.get('name', '').capitalize()
    else:
        user_name = ''
    
    return render(request, 'home.html', {'user_name': f"{user_name.capitalize()}"})

def user_profile(request):
    return render(request, 'user_profile.html')

def meu_carrinho(request):
    carrinho = request.COOKIES.get('suit2goCart', '{\'items\':[]}')
    return render(request, 'meu_carrinho.html', { 'carrinho': ast.literal_eval(carrinho) })

def checkout(request):
    carrinho = request.COOKIES.get('suit2goCart', '{\'items\':[]}')
    return render(request, 'checkout.html', { 'carrinho': ast.literal_eval(carrinho) })

def logout_view(request):
    logout(request)
    return redirect("/")

def authorize_google(request):
    return redirect('social:begin', 'google-oauth2')

def google_callback(request):
    # Lida com o retorno do Google após a autorização
    return redirect('/')