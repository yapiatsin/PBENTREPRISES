from django.shortcuts import render
from datetime import date, datetime, timedelta, timezone
from typing import Any
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView,CreateView, DeleteView, UpdateView, TemplateView
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Count
from django.db.models import Sum,F
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models.functions import Coalesce
from userauths.decorators import group_required
from django.utils.decorators import method_decorator
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator

# Create your views here.
def home(resquest):
    evenement = Evenement.objects.all().order_by('-date_saisie')[:5]
    context = {
        'evenement': evenement
        }
    return render(resquest, 'pbent/index.html',context)

def apropos(resquest):
    return render(resquest, 'pbent/about.html',)
def contact(resquest):
    return render(resquest,'pbent/contacts.html', )

#-----------présentation-----------#
def equip(resquest):
    return render(resquest,'pbent/equipe.html', )
def identite(resquest):
    return render(resquest,'pb/presentation/identite.html', )
def politiq(resquest):
    return render(resquest,'pb/presentation/politiq.html', )

#-----------Services-----------#
def Vtc(resquest):
    return render(resquest,'pbent/details_vtc.html', )
def Location(resquest):
    return render(resquest,'pbent/details_location.html', )
def Vent_piece(resquest):
    return render(resquest,'pbent/details_ventepiece.html', )
def hyrocarbure(resquest):
    return render(resquest,'pbent/details_hydro.html', )

#-----------media-----------#
def Photos(resquest):
    tof = Photo.objects.all().order_by('-date_saisie')
    return render(resquest,'pbent/photo.html', {'tof':tof})
class AddPhotoView(CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'news/site/add_photo.html'
    success_message = 'Photo Ajoutée avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('addphoto')
    def form_valid(self, form):
        reponse =  super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None,
        context['phot'] = Photo.objects.all()
        return context
class UpdatPhotoView(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'news/site/add_photo.html'
    success_message = 'Photo modifiée avec succès👍✓✓'
    success_url = reverse_lazy ('addphoto')
    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context

class DeletPhotoView(DeleteView):
    model = Photo
    template_name = 'news/site/delet_photo.html' 
    success_message = 'Photo Supprimée avec succès👍✓✓'
    success_url =reverse_lazy ('addphoto')
    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
        
def Videos(resquest):
    deo = Video.objects.all().order_by('-date_saisie')
    return render(resquest,'pbent/video.html', {'deo':deo})
class AddVideoView(CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'news/site/add_video.html'
    success_message = 'Vidéo Ajoutée avec succès👍✓✓'
    success_url = reverse_lazy ('addvideo')
    def form_valid(self, form):
        reponse =  super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['vid'] = Video.objects.all()
        return context
class UpdatVideoView(UpdateView):
    model = Video
    form_class = UpdatVideoForm
    template_name = 'news/site/add_video.html'
    success_message = 'Video modifiée avec succès👍✓✓'
    success_url = reverse_lazy ('addvideo')
    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
    
class DeletVideoView(DeleteView):
    model = Video
    template_name = 'news/site/delet_video.html' 
    success_message = 'Video Supprimée avec succès👍✓✓'
    success_url =reverse_lazy ('addvideo')
    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        return context
    
def Evenements(resquest):
    context={}
    event = Evenement.objects.all().order_by('-date_saisie')
    context['event'] = event   
    paginate_by = 6
    paginator = Paginator(event, self.paginate_by)
    page = self.request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
    print("--------------", events)
    return render(resquest,'pbent/evenement.html',context)


class Evenements(TemplateView):
    template_name = 'pbent/evenement.html'
    ordering = ['-date_saisie']
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        #context['event'] = Evenement.objects.all().order_by('-date_saisie')
        events_list = Evenement.objects.all().order_by("-date_saisie")
        paginator = Paginator(events_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            events = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            events = paginator.page(paginator.num_pages)
        context['event'] = events
        return context      

class AddCommentView(CreateView):
    model = Commentaire
    form_class = CommentForm
    template_name = 'pbent/addcommentaire.html'
    success_message = 'Commentaire Ajouté avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy('event')
    def form_valid(self, form):
        form.instance.event_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context

class AddEvenementView(CreateView):
    model = Evenement
    form_class = EvenementForm
    template_name = 'news/site/add_event.html'
    success_message = 'Evenement Ajouté avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('addevent')
    def form_valid(self, form):
        reponse =  super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['event'] = Evenement.objects.all().order_by('-date_saisie')
        return context
   
class UpdatEvenementView(UpdateView):
    model = Evenement
    form_class = UpdatEvenementForm
    template_name = 'news/site/add_event.html'
    success_message = 'Evenement modifié avec succès👍✓✓'
    success_url = reverse_lazy ('addevent')
    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context

class DetailEvenementtView(DetailView):
    model = Evenement
    template_name = 'pbent/detail_evenement.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['Event'] = Evenement.objects.all().order_by('-date_saisie')[:5]
        return context
    
class DeletEvenementView(DeleteView):
    model = Evenement
    template_name = 'news/site/delet_event.html' 
    success_message = 'Evenement Supprimé avec succès👍✓✓'
    success_url =reverse_lazy ('addevent')
    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context    
#-----------actualite-----------#
def Activite(resquest):
    return render(resquest,'pbent/activites.html', )
