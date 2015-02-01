from django.conf.urls import patterns, url

from tweet import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search.html$', views.searchWord, name='searchWord'),
    url(r'^user/(?P<user>\w+)/$', views.searchUser, name='searchUser'),
    url(r'^login/?$', views.twitter_login, name='twitter_login'),
    url(r'^logout/?$', views.twitter_logout, name='twitter_logout'),
    url(r'^login/authenticated/?$', views.twitter_authenticated, name='twitter_authenticated'),
)
