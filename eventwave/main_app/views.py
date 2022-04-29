from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from sorcery import dict_of

# Create your views here.


def index(request):
    response = requests.get(
        "https://api.seatgeek.com/2/events?geoip=98.213.245.205&per_page=1&client_id=MjAxNTMyNjV8MTY1MTE4OTU5My40NDUzMzAx")

    responseData = response.json()

    title = responseData['events'][0]['title']
    seekgeek_id = responseData['events'][0]['id']
    url = responseData['events'][0]['url']
    pub = responseData['events'][0]['datetime_utc']
    performer = responseData['events'][0]['performers'][0]['name']
    kind = responseData['events'][0]['type']

    context = dict_of(title, seekgeek_id, url, pub, performer, kind)

    return render(request, 'events/index.html', context)
