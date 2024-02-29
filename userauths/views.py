from typing import Any
from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
#from utils import send_email_whith
from django.http import HttpResponse
from userauths.forms import EditUserProfileForm, UserRegisterForm, PasswordChangingForm, CreateUserProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings 
from userauths.models import User
from datetime import datetime
from django.views.generic import ListView, DetailView,CreateView, DeleteView, UpdateView, TemplateView

from django.views import generic
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

#User = settings.AUTH_USER_MODEL
from django.contrib.auth.decorators import login_required
from .decorators import group_required
from .models import UserProfile

def password_success(request):
    return render(request,'userauths/success.html')

class CreateUserProfile(CreateView):
    model = UserProfile
    template_name = 'userauths/create_profil.html'
    form_class = CreateUserProfileForm
    success_message = 'Profil créé avec succès👍✓✓'
    success_url = reverse_lazy('profil_user')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
class EditProfilView(UpdateView):
    model = UserProfile
    form_class = EditUserProfileForm
    template_name = "userauths/edit_profil.html"
    success_url = reverse_lazy('profil_user')
    success_message = 'Profil modifié avec succès👍✓✓'
    def form_valid(self, form):
        reponse =  super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_object(self):
        return self.request.user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context   
 
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    user_group = request.user.groups.first()
    return render(request, 'userauths/profil.html', {'profile':profile,'user_group':user_group.name if user_group else None})


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('profil_user')
    success_message = 'Mot de passe changé avec succès👍✓✓'
    def form_valid(self, form):
        reponse =  super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context



def registrerView(request, *args, **kwargs):  # sourcery skip: extract-method
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            #new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hi {username}, Votre compte à été créé avec succès!!!")
            #new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data["password1"])
            #login(request, new_user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request,'userauths/sign_up.html',context)



#@group_required(['Administrateurs', 'Service_comptable'])
def loginview(request):
    if request.user.is_authenticated:
        messages.warning(request,f"hey you are already logged In")
        return redirect("home")
    if request.method == "POST":
        email = request.POST.get("email")  
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            #
            #subjet = "Test d'envoi d'email"
            #template = 'userauths/sign_in.html'
            #context = {
            #'date':datetime.today().date,
            #'email':email,
            #}
            #receivers =[email]
            #has_send=send_email_whith(subjet=subjet, 
            #     receivers=receivers, 
            #     template=template,
            #     context=context)
            #
            #if has_send:
            #    return redirect("index", {{"msg":"mail envoyé avc succes"}})
            #
            if user is not None:
                login(request, user)
                if request.user.groups.filter(name='Administrateurs').exists():
                    if user.gender == "Homme":
                        messages.success(request, f"Bienvenue Mr. {user} à P&BENTREPRISE !!!")
                    else:
                        messages.success(request, f"Bienvenue Mme {user} à P&BENTREPRISE !!!")
                    return redirect('dash')
                
                elif request.user.groups.filter(name='Service_comptable').exists():
                    if user.gender == "Homme":
                        messages.success(request, f"Bienvenue Mr. {user} à P&BENTREPRISE !!!")
                    else:
                        messages.success(request, f"Bienvenue Mme {user} à P&BENTREPRISE !!!")
                    return redirect('dash')
                
                elif request.user.groups.filter(name='Chefs_exploitation').exists():
                    if user.gender == "Homme":
                        messages.success(request, f"Bienvenue Mr. {user} à P&BENTREPRISE !!!")
                    else:
                        messages.success(request, f"Bienvenue Mme {user} à P&BENTREPRISE !!!")
                    return redirect('dash')
                
                elif request.user.groups.filter(name='Gerant_vehicules').exists():
                    if user.gender == "Homme":
                        messages.success(request, f"Bienvenue Mr. {user} à P&BENTREPRISE !!!")
                    else:
                        messages.success(request, f"Bienvenue Mme {user} à P&BENTREPRISE !!!")
                    return redirect('tb_garag')
                else:
                    return HttpResponse('Pas de Groupe')
            else:
                messages.warning(request, "Email ou mot de passe erroné !!!")
        except:
            messages.warning(request, f"Cet utilisateur, {email} n'existe pas")
    return render(request, "userauths/sign_in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes deconnecté.")
    return redirect("home")

def interneView(request):
    return render(request,"userauths/interne.html")
