from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
import datetime

# Create your views here.
from Remote_User.models import review_Model,ClientRegister_Model,usertweets_Model
import joblib
import flair
from flair.models import TextClassifier

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:

            enter = ClientRegister_Model.objects.get(username=username, password=password)
            request.session["userid"] = enter.id
            return redirect('CreateTweet')
        except:
            pass

    return render(request,'RUser/login.html')



def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city)

        return render(request, 'RUser/Register1.html')
    else:

        return render(request,'RUser/Register1.html')


def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})

def Review(request,pk):
    userid = request.session['userid']
    userObj = ClientRegister_Model.objects.get(id=userid)
    username = userObj.username
    saved_model = joblib.load(r'C:/Users/user/Downloads/AnalysisOf_WomenSafety/womensafety/save2.pkl')

    objs = usertweets_Model.objects.get(id=pk)
    u_id = userid
    city = objs.names
    datetime_object = datetime.datetime.now()

    result = ''
    pos = []
    neg = []
    oth = []
    se = 'se'
    suggestion1 = "suggestion"

    if request.method == "POST":
        uname = request.POST.get('uname')
        tname1 = request.POST.get('tname')
        cmd = request.POST.get('review')


        if '#' in cmd:
            startingpoint = cmd.find('#')
            a = cmd[startingpoint:]
            endingPoint = a.find(' ')
            title = a[0:endingPoint]
            result = title[1:]
        # return redirect('')

        sentence=flair.data.Sentence(cmd)


        saved_model.predict(sentence)
        total_sentiment = sentence.labels
        s2=str(total_sentiment[0])
        s2 = s2[0:8]
        
        if s2 == 'POSITIVE':
            se = 'positive'
        else:
            se = 'negative'
        review_Model.objects.create(uname=uname , uid = u_id,ureview=cmd,sanalysis=se,city = city, dt=datetime_object,tname=tname1 ,suggestion=suggestion1)

    return render(request,'RUser/Review.html', {'objc':username, 'uid':u_id, 'city':city, 'result': result, 'se': se})

def CreateTweet(request):
    userid = request.session['userid']
    userObj = ClientRegister_Model.objects.get(id=userid)
    userid = userObj.username
    saved_model = joblib.load(r'C:/Users/user/Downloads/AnalysisOf_WomenSafety/womensafety/save2.pkl')

    result = ''
    pos = []
    neg = []
    oth = []
    se = 'se'
    if request.method == "POST":
        uname = request.POST.get('uname')
        tname ="assault"
        uses = "use"
        cmd = request.POST.get('tdesc')
        mcity = request.POST.get('mcity')

        if '#' in cmd:
            startingpoint = cmd.find('#')
            a = cmd[startingpoint:]
            endingPoint = a.find(' ')
            title = a[0:endingPoint]
            result = title[1:]
        sentence=flair.data.Sentence(cmd)


        saved_model.predict(sentence)
        total_sentiment = sentence.labels
        s2=str(total_sentiment[0])
        s2 = s2[0:8]
        
        if s2 == 'POSITIVE':
            se = 'positive'
        else:
            se = 'negative'

        usertweets_Model.objects.create(userId=userObj,uname=uname ,tname=tname , tdesc=cmd, topics=result, sanalysis=se,
                                        senderstatus='process',names=mcity)

    return render(request,'RUser/CreateTweet.html', {'objc':userid,'result': result, 'se': se})

def ViewAllTweets(request):
    userid = request.session['userid']
    obj = usertweets_Model.objects.all()

    return render(request,'RUser/ViewAllTweets.html',{'list_objects': obj})

def Viewreviews(request):

    obj = review_Model.objects.all()

    return render(request,'RUser/Viewreviews.html',{'list_objects': obj})


def charts(request,chart_type):
    chart1 = usertweets_Model.objects.values('names').filter(sanalysis='positive').annotate(dcount=Count('ratings'))
    charts1 = review_Model.objects.values('city').filter(sanalysis='positive').annotate(dcount=Count('ureview'))
    tot = 0

    for e in chart1:
        for i in charts1:
            if e['names'] == i['city']:
                e['dcount']+=i['dcount']
                break
        tot += e['dcount']
    print(tot)
    chart1 = usertweets_Model.objects.values('names').filter(sanalysis='positive').annotate(dcount=((Count('ratings')*100.0)/tot))
    return render(request,"RUser/chart1.html", {'form':chart1, 'chart_type':chart_type})

def dislikechart1(request,dislike_chart):
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
    return render(request,"RUser/dislikechart1.html", {'form':charts, 'dislike_chart':dislike_chart})
def ratings(request,pk):
    vott1, vott, neg = 0, 0, 0
    objs = usertweets_Model.objects.get(id=pk)
    unid = objs.id
    vot_count = usertweets_Model.objects.all().filter(id=unid)
    for t in vot_count:
        vott = t.ratings
        vott1 = vott + 1
        obj = get_object_or_404(usertweets_Model, id=unid)
        obj.ratings = vott1
        obj.save(update_fields=["ratings"])
        return redirect('ViewAllTweets')

    return render(request,'RUser/ratings.html',{'objs':vott1})


def dislikes(request,pk):
    vott1, vott, neg = 0, 0, 0
    objs = usertweets_Model.objects.get(id=pk)
    unid = objs.id
    vot_count = usertweets_Model.objects.all().filter(id=unid)
    for t in vot_count:
        vott = t.dislikes
        vott1 = vott + 1
        obj = get_object_or_404(usertweets_Model, id=unid)
        obj.dislikes = vott1
        obj.save(update_fields=["dislikes"])
        return redirect('ViewAllTweets')
    return render(request,'RUser/dislikes.html',{'objs':vott1})



def ViewTrending(request):
    topic = usertweets_Model.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return render(request, 'RUser/ViewTrending.html', {'objects': topic})