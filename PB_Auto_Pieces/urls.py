from django.urls import path
from . import views

urlpatterns = [
    path('vent_index', views.Vente_index, name="vente_home")
]

