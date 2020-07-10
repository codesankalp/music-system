from django.contrib import admin
from .models import Songs,Playlist,Followers
# Register your models here.
admin.site.register(Songs)
admin.site.register(Playlist)
admin.site.register(Followers)