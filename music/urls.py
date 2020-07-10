from django.urls import path
from . import views

app_name = "music"

urlpatterns = [
    path('',views.index,name = "home"),
    path('add/song',views.add_song,name='add'),
    path('view/<str:playlist>',views.viewplay),
    path('follow/',views.follow),
    path('playlist/create/',views.create_playlist,name="create"),
    path('playlist/edit/',views.edit,name='edit'),
    path('playlist/edit/transfer/<str:playlist>',views.transfer,name='transfer'),
    path('playlist/edit/sort/<str:playlist>',views.sort,name='sort'),

]