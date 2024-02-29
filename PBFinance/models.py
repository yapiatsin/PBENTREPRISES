from django.db import models
from userauths.models import User

class Video(models.Model):
    title = models.CharField(max_length =50)
    video = models.FileField(upload_to ='video/%y')
    date = models.DateField()
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.title, self.video)

class Photo(models.Model):
    title = models.CharField(max_length =50)
    photo = models.FileField(upload_to ='photo')
    date_phot = models.DateField()
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.title, self.photo)

class Evenement(models.Model):
    auteur = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length =50)
    image = models.FileField(upload_to ='evenement')
    text = models.TextField(max_length=1000)
    date_event = models.DateField()
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):
        return '%s - %s - %s' % (self.title, self.image, self.auteur)

class Commentaire(models.Model):
    event = models.ForeignKey(Evenement,related_name='comments', on_delete=models.CASCADE)
    namuser = models.CharField(max_length=100)
    body = models.TextField(max_length=300)   
    date_comment = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.event.title, self.namuser)
