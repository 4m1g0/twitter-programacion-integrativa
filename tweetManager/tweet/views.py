from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import oauth2 as oauth
import cgi
import json
import urllib
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from tweet.models import Profile

CONSUMER_KEY = "b6VE4Huq6ypz76CUdNsGulqXj"
CONSUMER_SECRET = "a7aJg9nyf1aEzg5Pck30fSiuDNU0ED2hzKLFSjne27eBVKXhdO"
#ACCESS_KEY = "3008895899-nlv4Ni2JqEO7zieRxm7rtiw3PMZIIQVsmsXisjd"
#ACCESS_SECRET = "hTQd68Y5fRnrOwLBiy6IEbEnI6IuMSTaw3LrmCzs1vkHT"

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

#consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
#access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
#client = oauth.Client(consumer, access_token)
consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://twitter.com/oauth/request_token?oauth_callback=http://54.152.186.74:8000/accounts/login/authenticated/'
access_token_url = 'https://twitter.com/oauth/access_token'
authenticate_url = 'https://twitter.com/oauth/authenticate'

def twitter_login(request):
    # Step 1. Get a request token from Twitter.
    #body = urllib.urlencode(dict(oauth_callback='http://localhost:8000/accounts/login/authenticated/'))
    resp, content = client.request(request_token_url, "POST")
    print resp['status']
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    # Step 2. Store the request token in a session for later use.
    request.session['request_token'] = dict(cgi.parse_qsl(content))

    # Step 3. Redirect the user to the authentication URL.
    url = "%s?oauth_token=%s" % (authenticate_url,
        request.session['request_token']['oauth_token'])

    return HttpResponseRedirect(url)


@login_required
def twitter_logout(request):
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    logout(request)
    return HttpResponseRedirect('/')

def twitter_authenticated(request):
    verifier_token = request.GET['oauth_verifier']
    # Step 1. Use the request token in the session to build a new client.
    token = oauth.Token(request.session['request_token']['oauth_token'],
        request.session['request_token']['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    body = urllib.urlencode(dict(oauth_verifier=verifier_token))
    

    # Step 2. Request the authorized access token from Twitter.
    resp, content = client.request(access_token_url, "POST", body=body)
    if resp['status'] != '200':
        print content
        raise Exception("Invalid response from Twitter.")

    """
    This is what you'll get back from Twitter. Note that it includes the
    user's user_id and screen_name.
    {
        'oauth_token_secret': 'IcJXPiJh8be3BjDWW50uCY31chyhsMHEhqJVsphC3M',
        'user_id': '120889797', 
        'oauth_token': '120889797-H5zNnM3qE0iFoTTpNEHIz3noL9FKzXiOxwtnyVOD',
        'screen_name': 'heyismysiteup'
    }
    """
    access_token = dict(cgi.parse_qsl(content))

    # Step 3. Lookup the user or create them if they don't exist.
    try:
        user = User.objects.get(username=access_token['screen_name'])
    except User.DoesNotExist:
        user = User.objects.create_user(access_token['screen_name'],
            '%s@twitter.com' % access_token['screen_name'],
            access_token['oauth_token_secret'])

        # Save our permanent token and secret for later.
        profile = Profile()
        profile.user = user
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()

    # Authenticate the user and log them in using Django's pre-built 
    # functions for these things.
    user = authenticate(username=access_token['screen_name'],
        password=access_token['oauth_token_secret'])
    login(request, user)

    return HttpResponseRedirect(reverse('views.index'))
    
@login_required
def index(request):
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    response, data = client.request(url)
    data = {'statuses': json.loads(data)}
    return render(request, 'tweet/index.html', processResponse(data))
    
@login_required
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

@login_required
def searchUser(request, user):
    params = {'user_id':user}
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?" + urllib.urlencode(params)
    response, data = client.request(url)
    data = {'statuses': json.loads(data)}
    return render(request, 'tweet/index.html', processResponse(data))
    

