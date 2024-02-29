from django.contrib import admin
from .models import *

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title','date']
    list_filter = ['title','date']

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title','date_phot']
    list_filter = ['title','date_phot']

class EvenementAdmin(admin.ModelAdmin):
    list_display = ['title','auteur','date_event']
    list_filter = ['title','date_event']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['namuser','event','date_comment']
    list_filter = ['namuser','date_comment']

admin.site.register(Video, VideoAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Commentaire, CommentAdmin)
admin.site.register(Evenement, EvenementAdmin)