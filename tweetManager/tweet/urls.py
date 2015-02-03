from django.conf.urls import patterns, url

from tweet import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search.html$', views.searchWord, name='searchWord'),
    url(r'^user/(?P<user>\w+)/$', views.searchUser, name='searchUser'),
    url(r'^blocAction.html$', views.blocAction, name='blocAction'),
    url(r'^newTweet.html$', views.newTweet, name='newTweet'),
)
