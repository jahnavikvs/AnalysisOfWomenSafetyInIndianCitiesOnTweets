"""womensafety URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Remote_User import views as remoteuser
from womensafety import settings
from Tweet_Server import views as tweetserver
from django.conf.urls.static import static


urlpatterns = [
    url('admin/', admin.site.urls),

    url(r'^$', remoteuser.login, name="login"),


    url(r'^Register1/$', remoteuser.Register1, name="Register1"),

    url(r'^CreateTweet/$', remoteuser.CreateTweet, name="CreateTweet"),
    url(r'^Review/(?P<pk>\d+)/$', remoteuser.Review, name="Review"),
    url(r'^ViewAllTweets/$', remoteuser.ViewAllTweets, name="ViewAllTweets"),
    url(r'^Viewreviews/$', remoteuser.Viewreviews, name="Viewreviews"),
    url(r'^chart1/(?P<chart_type>\w+)', remoteuser.charts,name="chart1"),
    url(r'^dislikechart1/(?P<dislike_chart>\w+)', remoteuser.dislikechart1,name="dislikechart1"),
    url(r'^ratings/(?P<pk>\d+)/$', remoteuser.ratings, name="ratings"),
    url(r'^dislikes/(?P<pk>\d+)/$', remoteuser.dislikes, name="dislikes"),
    url(r'ViewTrending/$', remoteuser.ViewTrending, name="ViewTrending"),
    url(r'^ViewYourProfile/$', remoteuser.ViewYourProfile, name="ViewYourProfile"),

    url(r'^tweetserverlogin/$',tweetserver.tweetserverlogin, name="tweetserverlogin"),
    url(r'viewallclients/$',tweetserver.viewallclients,name="viewallclients"),
    url(r'ViewTrendings/$',tweetserver.ViewTrendings,name="ViewTrendings"),
    url(r'^charts/(?P<chart_type>\w+)', tweetserver.charts,name="charts"),
    url(r'^dislikeschart/(?P<dislike_chart>\w+)', tweetserver.dislikeschart,name="dislikeschart"),
    url(r'^Viewalltweets/$', tweetserver.Viewalltweets, name='Viewalltweets'),
    url(r'^View_Senti_Analysis/$', tweetserver.View_Senti_Analysis, name='View_Senti_Analysis'),
     url(r'^View_Senti_Reviews/$', tweetserver.View_Senti_Reviews, name="View_Senti_Reviews"),
    url(r'^View_User_Reviews/$', tweetserver.View_User_Reviews, name='View_User_Reviews'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
