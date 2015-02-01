from django.conf.urls import patterns, include, url
from django.contrib import admin
from tweet import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tweetManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tweet/', include('tweet.urls')),
    url(r'^accounts/login/?$', views.twitter_login, name='twitter_login'),
    url(r'^accounts/logout/?$', views.twitter_logout, name='twitter_logout'),
    url(r'^accounts/login/authenticated/?$', views.twitter_authenticated, name='twitter_authenticated'),
)
