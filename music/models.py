from django.db import models
from django.contrib.auth import get_user_model

class Songs(models.Model):
    song_name = models.CharField(max_length=200)
    song_file = models.FileField(upload_to="uploads/")
    size = models.BigIntegerField(blank=True,null=True)
    uploader = models.ManyToManyField(get_user_model(),blank=True)
    def __str__(self):
        return self.song_name

class Playlist(models.Model):
    playlist_name = models.CharField(max_length=200)
    playlist_songs = models.ManyToManyField(Songs)
    choice = (
        ("1","public"),
        ("2","private"),
        ("3","followers")
    ) 
    visibility = models.CharField(choices = choice, max_length = 100)
    creator = models.ManyToManyField(get_user_model(),blank=True)
    def __str__(self):
        return self.playlist_name 

class Followers(models.Model):
    user = models.CharField(max_length=200,blank=True,null=True)
    follow = models.ManyToManyField(get_user_model(),blank=True,related_name='+')
    def __str__(self):
        return self.user

