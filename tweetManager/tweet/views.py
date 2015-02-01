from django.shortcuts import render
from django.http import HttpResponse
import oauth2 as oauth
import json
import urllib

CONSUMER_KEY = "ViIjagjU58lD7dGmlbS16iSaR"
CONSUMER_SECRET = "yTKbfcCrCYjm8WmnUavNMota8JSnumCcuPWuiH49lEt8mjMTrD"
ACCESS_KEY = "3008895899-mdHYwFdRs1bEjrkqVwpy3Cq3X5pocaI6XcVx8ar"
ACCESS_SECRET = "z1TvjeKuiHfp8VI6GLbg7itRqyYEZwH6uyh9Lt9P5kBX1"

def processResponse(data):
    context = {'markers':[]}
    print data[0]
    for tweet in data:
        # set geo position
        pos = tweet['coordinates']
        #print pos
        #print tweet['text']
        if pos != None and pos['type'] == 'Point':
            pos = pos['coordinates']
            context['markers'].append({'x':pos[1], 'y':pos[0]})
        
        # set hashtag info
        #TODO
    
    #context={'markers':[{'x':43.34583, 'y':-8.4108}]}
    return context

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

def index(request):
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    response, data = client.request(url)
    return render(request, 'tweet/index.html', processResponse(json.loads(data)))
    
def searchWord(request):
    return 
    
def searchUser(request):
    return
    

