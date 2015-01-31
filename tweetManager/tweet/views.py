from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context={'markers':[{'x':43.34583, 'y':-8.4108}]}
    return render(request, 'tweet/index.html', context)
