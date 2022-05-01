from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from sorcery import dict_of

# Create your views here.


def index(request):
    response = requests.get(
        "https://api.seatgeek.com/2/events?q=gorillaz&per_page=1&client_id=MjAxNTMyNjV8MTY1MTE4OTU5My40NDUzMzAx")

    responseData = response.json()

    title = responseData['events'][0]['title']
    seekgeek_id = responseData['events'][0]['id']
    url = responseData['events'][0]['url']
    pub = responseData['events'][0]['datetime_utc']
    performer = responseData['events'][0]['performers'][3]['name']
    performers = responseData['events'][0]['performers']
    performerArray = []
    for performer in performers:
        performerArray.append(performer['name'])

    print(performerArray)
    kind = responseData['events'][0]['type']
    image = responseData['events'][0]['performers'][0]['image']

    context = dict_of(title, seekgeek_id, url, pub, performer, performers, performerArray, kind, image)
    print(context)
    return render(request, 'events/index.html', {'context': context})


def results(request):
    #     # build query
    zip = request.GET.get('zip')
    radius = request.GET.get('radius')
    type = request.GET.get('type')
    query = f'{BASE_URL}geoip={zip}&range={radius}mi{PER_PAGE}{CLIENT_ID}'

#     # api call
    response = requests.get(query)
    responseData = response.json()


#     # compile variables
    eventsContext = []
    for event in responseData['events']:
        print(f'{event} ----- EVENT!!')
        title = responseData['events'][0]['title']

        seekgeek_id = responseData['events'][0]['id']
        url = responseData['events'][0]['url']
        pub = responseData['events'][0]['datetime_utc']
        kind = responseData['events'][0]['type']
        image = responseData['events'][0]['performers'][0]['image']
        performer = responseData['events'][0]['performers'][1]['name']
        performers = responseData['events'][0]['performers']
        performerArray = []
        for performer in performers:
            performerArray.append(performer['name'])

        context = dict_of(title, seekgeek_id, url, pub, performer,
                          performers, performerArray, kind, image)

        eventsContext.append(context)

    print(eventsContext)
    return render(request, 'events/results.html', {'eventsContext': eventsContext})


