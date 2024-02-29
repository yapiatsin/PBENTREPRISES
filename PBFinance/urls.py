from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('identites', views.apropos, name='Apropos'),
    path('contacts', views.contact, name='contact'),
    
    path('equips', views.equip, name='equipes'),
    path('politiqs', views.politiq, name='politiq_pb'),
    
    path('Vtcs', views.Vtc, name='vtc'),
    path('VentPiec', views.Vent_piece, name='ventpiec'),
    path('Locations', views.Location, name='locations'),
    path('Hyrocarbures', views.hyrocarbure, name='hyrocarbures'),
    
    path('Photos', views.Photos, name='photo'),
    path('add_photo', AddPhotoView.as_view(), name='addphoto'),
    path('photo/<int:pk>/modifier', UpdatPhotoView.as_view(), name='updatphoto'),
    path('photo/<int:pk>/supprimer', DeletPhotoView.as_view(), name='deletphoto'),
    
    path('Videos', views.Videos, name='video'),
    path('add_video', AddVideoView.as_view(), name='addvideo'),
    path('video/<int:pk>/modifier', UpdatVideoView.as_view(), name='updatvideo'),
    path('video/<int:pk>/supprimer', DeletVideoView.as_view(), name='deletvideo'),
    
    path('Events', Evenements.as_view(), name='event'),
    path('add_event', AddEvenementView.as_view(), name='addevent'),
    path('event/<int:pk>/comment', AddCommentView.as_view(), name='addcoment'),
    path('event/<int:pk>/modifier', UpdatEvenementView.as_view(), name='updatevent'),
    path('event/<int:pk>/supprimer', DeletEvenementView.as_view(), name='deletevent'),
    path('event/<int:pk>/detail', DetailEvenementtView.as_view(), name='detailtevent'),
    
    path('Service', views.Activite, name='service'),
]
