from django import forms
from django.forms import ModelForm


class SongForm(forms.Form):  
    song_name = forms.CharField(label="Enter Song Name",max_length=200)  
    song_file = forms.FileField() 

