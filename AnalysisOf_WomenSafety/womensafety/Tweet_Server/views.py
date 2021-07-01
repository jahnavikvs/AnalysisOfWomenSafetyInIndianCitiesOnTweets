
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count

# Create your views here.
from Remote_User.models import usertweets_Model,ClientRegister_Model,review_Model


def tweetserverlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('admin')
        password = request.POST.get('password')
        if admin == "Server" and password =="Server":
            return redirect('Viewalltweets')


    return render(request,'TServer/tweetserverlogin.html')

def viewtreandingquestions(request,chart_type):
    dd = {}
    pos,neu,neg =0,0,0
    poss=None
    topic = usertweets_Model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics=t['ratings']
        pos_count=usertweets_Model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss=pos_count
        for pp in pos_count:
            senti= pp['names']
            if senti == 'positive':
                pos= pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics]=[pos,neg,neu]
    return render(request,'TServer/viewtreandingquestions.html',{'object':topic,'dd':dd,'chart_type':chart_type})

def View_Senti_Reviews(request):
    stype = request.POST.get('stype')
    obj = review_Model.objects.all().filter(sanalysis=stype)
    return render(request, 'TServer/View_Senti_Reviews.html', {'list_objects': obj})


def viewallclients(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'TServer/viewallclients.html',{'objects':obj})

def ViewTrendings(request):
    topic = usertweets_Model.objects.values('topics').annotate(dcount=Count('topics')).order_by('dcount')
    return  render(request,'TServer/ViewTrendings.html',{'objects':topic})

def negativechart(request,chart_type):
    dd = {}
    pos, neu, neg = 0, 0, 0
    poss = None

    topic = usertweets_Model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('dcount')
    for t in topic:
        topics = t['ratings']
        pos_count = usertweets_Model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss = pos_count
        for pp in pos_count:
            senti = pp['names']
            if senti == 'positive':
                pos = pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics] = [pos, neg, neu]
    return render(request,'TServer/negativechart.html',{'object':topic,'dd':dd,'chart_type':chart_type})


def charts(request,chart_type):
    chart1 = usertweets_Model.objects.values('names').filter(sanalysis='positive').annotate(dcount=Count('ratings'))
    charts1 = review_Model.objects.values('city').filter(sanalysis='positive').annotate(dcount=Count('ureview'))

    print(chart1)
    print(len(chart1))
    tot = 0

    for e in chart1:
        for i in charts1:
            if e['names'] == i['city']:
                e['dcount']+=i['dcount']
                break
        tot += e['dcount']
    print(tot)
    chart1 = usertweets_Model.objects.values('names').filter(sanalysis='positive').annotate(dcount=((Count('ratings')*100.0)/tot))
    return render(request,"TServer/charts.html", {'form':chart1, 'chart_type':chart_type})

def dislikeschart(request,dislike_chart):
    charts = usertweets_Model.objects.values('names').filter(sanalysis='negative').annotate(dcount=Count('dislikes'))
    charts1 = review_Model.objects.values('city').filter(sanalysis='negative').annotate(dcount=Count('ureview'))
    tot = 0
    print(charts1)
    for e in charts:
        for i in charts1:
            if e['names'] == i['city']:
                e['dcount']+=i['dcount']
                break
        tot += e['dcount']
    print(tot)
    charts = usertweets_Model.objects.values('names').filter(sanalysis='negative').annotate(dcount=((Count('dislikes')*100.0)/tot))
    return render(request,"TServer/dislikeschart.html", {'form':charts, 'dislike_chart':dislike_chart})

def Viewalltweets(request):
    chart = usertweets_Model.objects.values('names','tname','ratings','dislikes','uses','sanalysis','tdesc','uname').annotate(dcount=Avg('usefulcounts'))
    return render(request,'TServer/Viewalltweets.html',{'objects':chart})

def View_Senti_Analysis(request):


        mcityname = request.POST.get('mcity')
        obj1 = usertweets_Model.objects.all().filter(names=mcityname)
        return render(request,'TServer/View_Senti_Analysis.html',{'objects':obj1})

def View_User_Reviews(request):

    obj = review_Model.objects.all()

    return render(request,'TServer/View_User_Reviews.html',{'list_objects': obj})