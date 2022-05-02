import profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import requests
from .models import User, Event, Profile
from sorcery import dict_of

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
BASE_URL = 'https://api.seatgeek.com/2/events?'
PER_PAGE = '&per_page=20'
CLIENT_ID = "&client_id=MjAxNTMyNjV8MTY1MTE4OTU5My40NDUzMzAx"


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)

      # Create Profile object for user
      newUser = User.objects.get(username=user.username)
      newProfile = Profile(user=newUser)
      newProfile.save()

      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


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

    kind = responseData['events'][0]['type']
    image = responseData['events'][0]['performers'][0]['image']

    context = dict_of(title, seekgeek_id, url, pub, performer,
                      performers, performerArray, kind, image)
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
    if response:
        eventsContext = []
        for event in responseData['events']:
            title = event['title']
            seekgeek_id = event['id']
            url = event['url']
            pub = event['datetime_utc']
            kind = event['type']
            image = event['performers'][0]['image']
            # performer = event['performers'][1]['name']
            performers = event['performers']
            performerArray = []
            for performer in performers:
                performerArray.append(performer['name'])

            context = dict_of(title, seekgeek_id, url, pub, performer,
                              performers, performerArray, kind, image)

            eventsContext.append(context)

        return render(request, 'events/results.html', {'eventsContext': eventsContext})
    return redirect('/')


# @login_required
def events_details(request, seekgeek_id):
    query = f'{BASE_URL}id={seekgeek_id}{CLIENT_ID}'
    # API Call
    response = requests.get(query)
    responseData = response.json()

    # Build Context
    title = responseData['events'][0]['title']
    seekgeek_id = responseData['events'][0]['id']
    url = responseData['events'][0]['url']
    pub = responseData['events'][0]['datetime_utc']
    performers = responseData['events'][0]['performers']
    performerArray = []
    for performer in performers:
        performerArray.append(performer['name'])
    kind = responseData['events'][0]['type']
    image = responseData['events'][0]['performers'][0]['image']
    context = dict_of(title, seekgeek_id, url, pub, performer,
                      performers, performerArray, kind, image)
    return render(request, 'events/detail.html', {'context': context})


@login_required
def dashboard_index(request, seekgeek_id):
    if request.method == 'GET':
        # get User info....
        currentUser = User.objects.get(username=request.user.username)
        #get Profile object..
        currentUserProfile = Profile.objects.get(user_id=currentUser.id)

        # get all events with profile.user_id
        allEvents = Event.objects.filter(profile=currentUserProfile)
        print(allEvents)

        return render(request, 'dashboard/index.html', {'context': allEvents})


    elif request.method == 'POST':
        query = f'{BASE_URL}id={seekgeek_id}{CLIENT_ID}'
        # API Call
        response = requests.get(query)
        responseData = response.json()

        # Build Context
        title = responseData['events'][0]['title']
        seekgeek_id = responseData['events'][0]['id']
        url = responseData['events'][0]['url']
        pub = responseData['events'][0]['datetime_utc']
        kind = responseData['events'][0]['type']
        image = responseData['events'][0]['performers'][0]['image']
        performers = responseData['events'][0]['performers']
        performerArray = []
        for performer in performers:
            performerArray.append(performer['name'])
        if len(performerArray) > 2:
            performerString = ' '.join(performerArray[:2])
        else:
            performerString = ' '.join(performerArray)

        # get User info....
        currentUser = User.objects.get(username=request.user.username)
        #get Profile object..
        currentUserProfile = Profile.objects.get(user_id=currentUser.id)
        
        myEvent = Event(title=title, seekgeek_id=seekgeek_id,
                        url=url, pub=pub, performer=performerString, kind=kind, profile=currentUserProfile)
        myEvent.save()
        

        return render(request, 'events/detail.html')
