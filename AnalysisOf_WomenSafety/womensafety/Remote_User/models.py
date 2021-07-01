from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)



class usertweets_Model(models.Model):
    userId = models.ForeignKey(ClientRegister_Model, on_delete=CASCADE)
    uname = models.CharField(max_length=300)

    tname= models.CharField(max_length=500)
    uses = models.CharField(max_length=100)
    tdesc = models.CharField(max_length=500)
    topics = models.CharField(max_length=300)
    sanalysis = models.CharField(max_length=300)
    names= models.CharField(max_length=300)
    senderstatus = models.CharField(default="process", max_length=300 )
    ratings = models.IntegerField(default=0)
    usefulcounts = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)



class review_Model(models.Model):
    uid= models.IntegerField(default=0)
    uname = models.CharField(max_length=100)
    ureview = models.CharField(max_length=100)
    sanalysis = models.CharField(max_length=100)
    city = models.CharField(max_length=300)
    dt= models.CharField(max_length=300)
    tname= models.CharField(max_length=300)
    suggestion = models.CharField(max_length=300)


