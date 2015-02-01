from django.shortcuts import render
from django.http import HttpResponse
import oauth2 as oauth
import json
import urllib
import re

CONSUMER_KEY = "b6VE4Huq6ypz76CUdNsGulqXj"
CONSUMER_SECRET = "a7aJg9nyf1aEzg5Pck30fSiuDNU0ED2hzKLFSjne27eBVKXhdO"
ACCESS_KEY = "3008895899-nlv4Ni2JqEO7zieRxm7rtiw3PMZIIQVsmsXisjd"
ACCESS_SECRET = "hTQd68Y5fRnrOwLBiy6IEbEnI6IuMSTaw3LrmCzs1vkHT"

def processResponse(data):
    context = {'markers':[],'hashtags':{},'users':{},'tweets':[]}
    hashtags = {}
    pattern = None
    if 'keyword' in data:
        pattern = re.compile(re.escape(data['keyword']), re.IGNORECASE)
        
    for tweet in data['statuses']:
        # set geo position
        pos = tweet['coordinates']
        if pos != None and pos['type'] == 'Point':
            pos = pos['coordinates']
            context['markers'].append({'x':pos[1], 'y':pos[0]})
        
        # set hashtag info
        for tag in tweet['entities']['hashtags']:
            text = tag['text']
            hashtags[text] = hashtags.get(text, 0) + 1
            
        # set users info
        name = tweet['user']['name']
        context['users'][name] = tweet['user']['id']
        
        # set tweet info
        post = {}
        if pattern:
            post['text'] = pattern.sub('<b>'+data['keyword']+'</b>', tweet['text'])
        else:
            post['text'] = tweet['text']
        post['screen_name'] = tweet['user']['screen_name']
        post['name'] = tweet['user']['name']
        post['profile_image'] = tweet['user']['profile_image_url_https']
        post['retweet_count'] = tweet['retweet_count']
        post['favorite_count'] = tweet['favorite_count']
        context['tweets'].append(post)

    context['hashtags'] = sorted(hashtags.items(), key = lambda x: x[1], reverse=True)
    context['users'] = context['users'].items()
    
    return context

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

def index(request):
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    response, data = client.request(url)
    data = {'statuses': json.loads(data)}
    return render(request, 'tweet/index.html', processResponse(data))
    
def searchWord(request):
    if request.POST.has_key('search'):
        search=request.POST['search']
        params = {'q':search}
        url = "https://api.twitter.com/1.1/search/tweets.json?" + urllib.urlencode(params)
        response, data = client.request(url)
        data = json.loads(data)
        data['keyword'] = search
        return render(request, 'tweet/index.html', processResponse(data))
    else:
        return render(request, 'tweet/index.html', {'error': True})

def searchUser(request, user):
    params = {'user_id':user}
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?" + urllib.urlencode(params)
    response, data = client.request(url)
    data = {'statuses': json.loads(data)}
    return render(request, 'tweet/index.html', processResponse(data))
    

