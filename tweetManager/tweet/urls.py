from django.conf.urls import patterns, url

from tweet import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search.html$', views.searchWord, name='searchWord'),
    url(r'^user/(?P<user>\w+)/$', views.searchUser, name='searchUser'),
)
