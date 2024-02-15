from allauth.socialaccount.models import SocialAccount,SocialToken
from google.oauth2.credentials import Credentials
from django.contrib.auth.models import User
from googleapiclient.discovery import build
import uuid
import os

def connect_to_calendar(request):
    #Fetches the User of the request
    qs=SocialAccount.objects.filter(user=request.user)
    print(request.user)
    #Fetches the Acces token of the User
    token=SocialToken.objects.filter(account=qs[0]).values('token')

    #The scope of service like if we want readonly etc
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    #Finally making a connection request
    creds = Credentials(token[0]['token'],SCOPES )
    service = build('calendar', 'v3', credentials=creds)
    return service

def convert_attendees_to_list(attendees):
        res=list()
        for i in attendees.split(','):
            d=dict()
            d['email']=i.strip()
            res.append(d)
        return res

def convert_RFC(date):
    return str(date.isoformat('T'))
    
def prepare_event(data):
    start=convert_RFC(data["start_time"])
    end=convert_RFC(data["end_time"])
    email=convert_attendees_to_list(data['attendees'])
    event = {
        'summary': data["summary"],
        'description': data["description"],
        'start': {
            'dateTime': start,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': email,
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        }
    }
    return event

def generate_file_name(instance, filename):
    _, ext = os.path.splitext(filename)
    novo_id = uuid.uuid4()
    filename = f"{novo_id}{ext}"
    return filename