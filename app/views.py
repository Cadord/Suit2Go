from .models import Roupas
from .forms import RoupasForms, DateForm
from django.db.models import Q
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from time import sleep
from datetime import datetime, time, timedelta, date
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery
import tkinter as tk
from tkintermapview import TkinterMapView
import os

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
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_860607395602-kldpfn6g61u968u3gop43jiu8b24bsfq.apps.googleusercontent.com.json', SCOPES 
            )
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)


# Create your views here.
def index(request):
    query = request.GET.get('q', '')
    ultimas_roupas_query = Roupas.objects
    if (query):
        ultimas_roupas_query = ultimas_roupas_query.filter(Q(nome__icontains=query))
    ultimas_roupas = ultimas_roupas_query.order_by('nome').all
    context = {
        "roupas": ultimas_roupas
    }
    return render(request, "index.html", context)


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

def roupa_dinamico(request,idroupa):
    context = {'roupa':Roupas.objects.get(id_roupas=idroupa)}
    return render(request,'roupa.html',context)
    
def aluguel(request, idroupa):
    form = DateForm()
    if request.method == 'POST':
        formulario = DateForm(request.POST)
        if formulario.is_valid():
            data_1 = formulario.cleaned_data['date_1']
            hora_1 = formulario.cleaned_data['time_1']
            endereco = formulario.cleaned_data['endereco']

            # Combina data e hora para criar um objeto datetime
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
            # Insira o evento na sua agenda
            service.events().insert(calendarId='primary', body=evento).execute()
            messages.success(request,"Aluguel efetuado com sucesso!")
    win = tk.Tk()
    win_map = TkinterMapView(tk, width=800, height=800)
    win_map.pack(fill='both', expand= True)
    win_map.set_tile_server("http://mt0.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", max_zoom=22)
    win_map.set_address(f'{endereco}', marker=True)
    while True:
        win.mainloop()


    return render(request, 'alugar.html',{'form':form,'roupa':Roupas.objects.get(id_roupas=idroupa)})
def home(request):
    try:
        social_account = SocialAccount.objects.get(user=request.user, provider='google')
        user_name = social_account.extra_data.get('name', '')
    except SocialAccount.DoesNotExist:
        user_name = ''

    return render(request, 'home.html', {'user_name': user_name})

def user_profile(request):
    return render(request, 'user_profile.html')

def logout_view(request):
    logout(request)
    return redirect("/")
    