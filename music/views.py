from django.shortcuts import render, redirect
from .forms import SongForm
from django.http import HttpResponse 
from .models import Songs,Playlist,Followers
import os 
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    songs = Songs.objects.all()
    pub_list = Playlist.objects.filter(visibility = '1')
    pvt_list = Playlist.objects.filter(visibility = '2')
    follow_list = Playlist.objects.filter(visibility='3')
    try:
        user_following = (Followers.objects.filter(user=str(request.user)))[0].follow.values()
    except:
        user_following = []
    print(user_following)
    ls = []
    nls = set()
    for i in pvt_list:
        if i.creator.values()[0]['username'] == str(request.user):
            ls.append(i)
    for i in user_following:
        for j in follow_list:
            if j.creator.values()[0]['username'] == i['username']:
                nls.add(j)
    return render(request,'home.html',{
        "songs":songs,
        "public":pub_list,
        "private":ls,
        "follow":nls,
    })

def viewplay(request,playlist):
    playlist = Playlist.objects.get(playlist_name=playlist)
    songs = playlist.playlist_songs.values()
    return render(request,'viewplay.html',{
        "pl":playlist,
        "songs":songs,
        })

def add_song(request):
    if request.method == 'GET':
        return render(request,"song.html",{'form':SongForm()})
    else:
        form = SongForm(request.POST, request.FILES)  
        if form.is_valid():
            song = Songs()
            song.song_name = request.POST['song_name']
            song.song_file = form.cleaned_data['song_file']
            path_to_uploads = (os.path.join((os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'uploads')),'uploads'))
            song_path = os.path.join(path_to_uploads,song.song_file.name)
            print(request.user)
            song.save()
            song.size = os.stat(song_path).st_size
            song.uploader.add(request.user)
            song.save()  
            return HttpResponse("Song uploaded successfuly")

def create_playlist(request):
    songs = Songs.objects.all()
    if request.method == 'GET':
        return render(request,"playlist.html",{"songs":songs})
    else:
        playlist = Playlist()
        playlist.playlist_name = request.POST.get("playlist_name")
        playlist.visibility = request.POST.get("visibility")
        playlist.save()
        for i in request.POST.getlist("playlist_songs"):
            print(i)
            playlist.playlist_songs.add(i)
        playlist.creator.add(request.user)
        return HttpResponse("Playlist created successfuly")

def edit(request):
    playlist = Playlist.objects.all()
    if request.method == 'GET':
        return render(request,"edit.html",{"playlist":playlist})
    else:
        playlist = request.POST.get('playlist')
        operation = request.POST.get('operation')
        if operation == '1':
            return redirect('/music/playlist/edit/transfer/{}'.format(playlist))
        elif operation == '2':
            return redirect('/music/playlist/edit/sort/{}'.format(playlist))

def transfer(request, playlist):
    obj = Playlist.objects.filter(playlist_name = playlist)[0]
    playlist = Playlist.objects.all()
    if request.method == 'GET':
        return render(request,'transfer.html',{
            "songs":obj.playlist_songs.values(),
            "playlist":playlist,
            "obj":obj
            })
    else:
        songs_to_add = request.POST.getlist("playlist_songs")
        playlist_chosen = request.POST.getlist("playlist")
        for i in songs_to_add:
            song = Songs.objects.get(song_name=i)
            for j in playlist_chosen:
                playlist = Playlist.objects.get(pk=j)
                playlist.playlist_songs.add(song)
        return HttpResponse("Songs transffered succesfully")

def sort(request, playlist):
    obj = Playlist.objects.filter(playlist_name = playlist)[0]
    playlist = Playlist.objects.all()
    if request.method == 'GET':
        return render(request,'sort.html',{
            "songs":obj.playlist_songs.values(),
            "playlist":playlist,
            "obj":obj,
            "value":0,
            })
    else:
        if request.POST.get("basis") == '1':
            dic = obj.playlist_songs.values().order_by('size')
            return render(request,'sort.html',{
                "songs":dic,
                "value":1,
                "playlist":playlist,
                "obj":obj,
            })

def follow(request):
    if request.method == 'GET':
        return render(request,'follow.html',{
        "users" : User.objects.all()
        })
    else:
        to_follow = request.POST.getlist('follow')
        print(to_follow)
        curr_user = request.user
        try:
            obj = Followers.objects.get(user = curr_user)
        except:
            obj = Followers()
            obj.user = curr_user
        obj.save()
        obj.follow.clear()        
        for i in to_follow:
            user = User.objects.get(username=i)
            print(user)
            obj.follow.add(user)
        return HttpResponse("Now you are following them")
