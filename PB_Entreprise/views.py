from datetime import date, datetime, timedelta, timezone
from typing import Any
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
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
# Create your views here.
from .forms import DateForm, DateFormArret
from userauths.decorators import group_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

def Error_404(request):
    return render(request, 'pbent/page_404.html')

def news(request):
    return render(request, 'news/base/baz.html')

def da(request):
    return render(request, 'news/appl/temp_arret.html')

class ResumeView(TemplateView):
    template_name = 'pbent/resume_to_day.html'

class SuiviFinancierView(TemplateView):
    model = Vehicule
    template_name = 'news/applist/suivie_financier_vehi.html' 
    context_object_name = 'vehicule'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        
        all_vehicule = Vehicule.objects.all()
        resultat_vehicule = []
        if all_vehicule:
            for vehicule in all_vehicule:
                recettes = Recette.objects.filter(vehicule = vehicule).aggregate(Sum('montant'))['montant__sum'] or 1
                charge_fix = ChargeFixe.objects.filter(vehicule = vehicule).aggregate(Sum('montant'))['montant__sum'] or 0
                charge_var = ChargeVariable.objects.filter(vehicule = vehicule).aggregate(Sum('montant'))['montant__sum'] or 0
                
                Total_charge = charge_fix + charge_var
                marg_contr = recettes - charge_var
                taux_marge = (marg_contr*100/(recettes))
                taux_marge_format ='{:.2f}'.format(taux_marge)
                resultat = recettes-Total_charge
                reparations = Reparation.objects.filter(vehicule = vehicule)
                context['som_piece'] = Piece.objects.filter(reparation__in = reparations).aggregate(total_piece=Sum('cout'))['total_piece'] or 0
                resultat_vehicule.append({'vehicule': vehicule, 'recettes':recettes, 'charge_fix':charge_fix, 'charge_var':charge_var, 'Total_charge':Total_charge, 'marg_contr':marg_contr, 'taux_marge_format':taux_marge_format, 'resultat': resultat, 'som_piece':context['som_piece'] or 0 })
        else:
            charge_fix =0
            charge_var =0
            Total_charge = 0
            marg_contr = 0
            taux_marge_format = 0
            resultat = 0
            marg_contr = 0
            resultat_vehicule = 0
            recettes = 0
        #context['som_piece'] = som_piece 
        context['charge_fix'] = charge_fix
        context['charge_var'] = charge_var
        context['Total_charge'] = Total_charge
        context['marg_contr'] = marg_contr
        context['taux_marge_format'] = taux_marge_format
        context['resultat'] = resultat
        context['resultat_vehicule'] = resultat_vehicule
        context['all_vehicule'] = all_vehicule
        context['total_recet_verse'] = recettes
        return context

class DashboardView(TemplateView):
    template_name = 'news/appl/dashboard.html'
    form_class = DateForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        
        catego_vehi = CategoVehi.objects.all().annotate(vehicule_count=Count("category"))
        recette= Recette.objects.all()
        Total_recettes = sum(recet.montant for recet in recette)
        Total_recette_format ='{:,}'.format(Total_recettes).replace('',' ')
        vehicules = Vehicule.objects.all()
        recette_mois = Recette.objects.annotate(mois_de_recettes=ExtractMonth("date")).values("mois_de_recettes").annotate(total_recet=Sum("montant")).values("mois_de_recettes","total_recet").order_by('mois_de_recettes')
        charg_var_mois = ChargeVariable.objects.annotate(month_chvar=ExtractMonth("date")).values("month_chvar").annotate(total_chvar=Sum("montant")).values("month_chvar","total_chvar").order_by('month_chvar')
        month_piece =[]
        marg_par_mois = []
        for reccete, chargess in zip(recette_mois,charg_var_mois):
            month_recets = (calendar.month_name[reccete['mois_de_recettes']][:2])
            if month_recets:
                month_recets = (calendar.month_name[reccete['mois_de_recettes']][:2])
            else:
                month_recets = (calendar.month_name[reccete['mois_de_recettes']][:2])
            cumul_recettes = reccete['total_recet']
            cumul_charges = chargess['total_chvar'] if chargess['total_chvar'] else 0
            marge = cumul_recettes - cumul_charges
            if cumul_recettes==0:
                taux =0
            else:
                taux = round(((marge)*100/cumul_recettes),2)
        if marg_par_mois:
            marg_par_mois.append({'month_recets': month_recets, 'marge': marge,'taux':taux})
        else:
            marg_par_mois.append({})
        
#-----------------------------------Pour Faire les filtre selon les dates entrées---------------------------------
        form = self.form_class(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin'] 
            
            recettes = Recette.objects.filter(date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum'] 
            context['recettes_totales'] = recettes if recettes is not None else 0
            
            piecs = Piece.objects.filter(date_achat__range=[date_debut, date_fin]).aggregate(Sum('cout'))['cout__sum'] 
            context['pieces_totales'] = piecs if piecs is not None else 0
            
            charges_variables = ChargeVariable.objects.filter(date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']
            context['charges_variables_totales'] = charges_variables if charges_variables is not None else 0
            
            charges_fixe = ChargeFixe.objects.filter(date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']
            context['charges_fixes_totales'] = charges_fixe if charges_fixe is not None else 0
            
            context['charges_totales'] =charges_fixe + context['charges_variables_totales'] if charges_fixe is not None else 0

            context['marge_totale'] = recettes - context['charges_variables_totales'] if recettes is not None else 0

            taux_recette = Recette.objects.filter(date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum'] or 1
            taux_diviseur = context['recettes_totales'] - (context['charges_variables_totales'])
            
            context['taux_vehi'] = round(taux_diviseur*100/ taux_recette, 2 ) if taux_recette is not None and taux_diviseur is not None else 0
            
            taux_mois= round(taux_diviseur*100/ taux_recette, 2 ) if taux_recette is not None and taux_diviseur is not None else 0
            context['taux_par_mois'] = [taux_mois] * 12 if taux_recette else [0] * 12

            resultat = (context['recettes_totales'] - context['charges_totales'])
            context['resultat_total'] = resultat if resultat is not None else 0
            
#-------------------------------------------Pour les Graphes---------------------------------------------
            recets = Recette.objects.filter(date__range=[date_debut, date_fin])
            charvars = ChargeVariable.objects.filter(date__range=[date_debut, date_fin])
            charfix = ChargeFixe.objects.filter(date__range=[date_debut, date_fin])
            pieces = Piece.objects.filter(date_achat__range=[date_debut, date_fin])
            
            recettes_mensuelles = {month: 0 for month in range(1, 13)}
            charges_variables_mensuelles = {month: 0 for month in range(1, 13)}
            charges_fixe_mensuelles = {month: 0 for month in range(1, 13)}
            piece_mensuelles = {month: 0 for month in range(1, 13)}
            
            for recette in recets:
                recettes_mensuelles[recette.date.month] += recette.montant
                
            for charge_variable in charvars:
                charges_variables_mensuelles[charge_variable.date.month] += charge_variable.montant
            
            for charge_fixe in charfix:
                charges_fixe_mensuelles[charge_fixe.date.month] += charge_fixe.montant
            
            for piec in pieces:
                piece_mensuelles[piec.date_achat.month] += piec.cout
            
            piece_data = [piece_mensuelles[month] for month in range(1, 13)]
            piece_data = [0 if piec == 0 else piece_data[i - 1] for i, piec in enumerate(piece_data, start=1)]
            
            recette_data = [recettes_mensuelles[month] for month in range(1, 13)]
            recette_data = [0 if recette == 0 else recette_data[i - 1] for i, recette in enumerate(recette_data, start=1)]
            
            charg_vari_data = [charges_variables_mensuelles[month] for month in range(1, 13)]
            charg_vari_data = [0 if charge_variable == 0 else charg_vari_data[i - 1] for i, charge_variable in enumerate(charg_vari_data, start=1)]
            
            charg_fixe_data = [charges_fixe_mensuelles[month] for month in range(1, 13)]
            charg_fixe_data = [0 if charge_fixe == 0 else charg_fixe_data[i - 1] for i, charge_fixe in enumerate(charg_fixe_data, start=1)]
            
            marges_mensuelles = {month: recettes_mensuelles[month] - charges_variables_mensuelles[month] for month in range(1, 13)}
            taux_mensuels = {month: (marges_mensuelles[month] * 100) / recettes_mensuelles[month] if recettes_mensuelles[month] > 0 else 0 for month in range(1, 13)}
            context['labels'] = [month[:2] for month in list(calendar.month_name)[1:]]
            
            taux_data = [taux_mensuels[month] for month in range(1, 13)]
            taux_data = [0 if taux == 0 else taux_data[i - 1] for i, taux in enumerate(taux_data, start=1)]
            
            marge_contri = []
            all_vehicule = Vehicule.objects.all()[:6]
            all_recettes= Recette.objects.all()[:6]
            best_recets = []
            best_marge = []
            best_taux = []
            for vehicule in all_vehicule:
                recs = Recette.objects.filter(vehicule=vehicule, date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum'] 
                context['rece_all'] = recs if recs is not None else 0
                
                charges_variables = ChargeVariable.objects.filter(vehicule = vehicule, date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']
                context['chargvari_all'] = charges_variables if charges_variables is not None else 0
                
                marge_cont = context['rece_all'] - context['chargvari_all']
                context['marge'] = marge_cont if marge_cont is not None else 0
                
                if context['rece_all'] == 0:
                    context['taux'] =0
                else:
                    taux = round((context['marge']*100)/context['rece_all'],2)
                    context['taux'] = taux if taux is not None else 0
                    
                best_taux.append({'vehicule': vehicule, 'taux':taux})
                best_marge.append({'vehicule': vehicule, 'marge_cont':marge_cont})
                best_recets.append({'vehicule': vehicule, 'recs':recs})
            best_marge = sorted([x for x in best_marge if x['marge_cont'] is not None], key=lambda x: x['marge_cont'], reverse=True)[:3] 
            best_recets = sorted([x for x in best_recets if x['recs'] is not None], key=lambda x: x['recs'], reverse=True)[:5] 
            
            context['taux_data'] = taux_data
            context['best_taux'] = best_taux
            context['best_marge'] = best_marge
            context['best_recets'] = best_recets
            context['recette_data'] = recette_data
            context['charg_vari_data'] = charg_vari_data
            context['charg_fixe_data'] = charg_fixe_data
            context['piece_data'] = piece_data
        else:
            all_vehicule = Vehicule.objects.all()
            marge_contri = []
            recettes= Recette.objects.all()[:5]
            top_recets = []
            for vehicule in all_vehicule:
                total_recets = Recette.objects.filter(vehicule = vehicule).aggregate(Sum('montant'))['montant__sum'] or 1
                total_charg_var = ChargeVariable.objects.filter(vehicule = vehicule).aggregate(Sum('montant'))['montant__sum'] or 0
                marge_contribution = total_recets - total_charg_var
                taux = round(((marge_contribution)*100/total_recets),2)
                marge_contri.append({'vehicule': vehicule, 'marge_contribution':marge_contribution,'taux':taux})
                top_recets.append({'vehicule': vehicule, 'total_recets':total_recets})
#-------    ----------------------Top marge----------------------------
            marge_contri = sorted(marge_contri, key=lambda x: x['marge_contribution'], reverse=True)[:3]    
            top_recets = sorted(top_recets, key=lambda x: x['total_recets'], reverse=True)[:3]
            
            context['marge_contri'] = marge_contri
            context['top_recets'] = top_recets
            context['labels'] = [month[:2] for month in list(calendar.month_name)[1:]]
            context['taux_data'] = [0] * 12
        context['form'] = form
        
        catego_vehi = CategoVehi.objects.all()
        context['categories'] = CategoVehi.objects.all()
        categorie_id = self.request.GET.get('categorie')
        if categorie_id:
            categorie = CategoVehi.objects.get(pk=categorie_id)
            context['somme_par_categorie'] = Recette.objects.filter(vehicule_id__category=categorie).aggregate(Sum('montant'))['montant__sum']
        else:
            context['somme_par_categorie'] = Recette.objects.all().aggregate(Sum('montant'))['montant__sum']
        
#_____________________________TOTAL DES CHARGES VARIABLES_____________________________#
        cahargevariable = ChargeVariable.objects.all()
        Total_charg_var = sum(chargvar.montant for chargvar in cahargevariable)
        
        Total_charg_var_format ='{:,}'.format(Total_charg_var).replace('',' ')
#_____________________________TOTAL DES CHARGES FIXES_____________________________#       
        chargefix = ChargeFixe.objects.all()
        Total_charg_fix = sum(chargfix.montant for chargfix in chargefix)
        Total_charg_fix_format ='{:,}'.format(Total_charg_fix).replace('',' ')
#_____________________________TOTAL DES CHARGES_____________________________#
        total_charg = Total_charg_fix + Total_charg_var
        total_charge_format ='{:,}'.format(total_charg).replace('',' ')
#_____________________________MARGE CONTRIBUTION_____________________________#
        marge_contribution = Total_recettes - Total_charg_var
#_____________________________TAUX CONTRIBUTION_____________________________#
        if Total_recettes == 0:
            taux_marge = 0
        else:
            taux_marge = (marge_contribution*100/(Total_recettes))
        taux_marge_format ='{:.2f}'.format(taux_marge)
#_____________________________RESULTAT_____________________________#
        resultat = Total_recettes - total_charg
        resultat_format ='{:,}'.format(resultat).replace('',' ')
#_________________________________PIECE______________________________#
        piece = Piece.objects.all()
        totl_piece = sum(piece.cout for piece in piece)
        totl_piece_format ='{:,}'.format(totl_piece).replace('',' ')
        
        total_piece_mois = Piece.objects.annotate(month_piece=ExtractMonth("date_achat")).values("month_piece").annotate(total_piece=Sum("cout")).values("month_piece","total_piece")
        month_piece =[]
        total_piece = []
        for i in total_piece_mois:
            month_piece.append(calendar.month_name[i["month_piece"]][:2])
            total_piece.append(i['total_piece'])
        
        #-------------------------------------------Pour les Graphes---------------------------------------------
        recets = Recette.objects.all()
        charvars = ChargeVariable.objects.all()
        charfix = ChargeFixe.objects.all()
        piecs = Piece.objects.all()
        
        recettes_mensuelles = {month: 0 for month in range(1, 13)}
        charges_variables_mensuelles = {month: 0 for month in range(1, 13)}
        charges_fixe_mensuelles = {month: 0 for month in range(1, 13)}
        piece_mensuelles = {month: 0 for month in range(1, 13)}
        
        for recette in recets:
            recettes_mensuelles[recette.date.month] += recette.montant
            
        for charge_variable in charvars:
            charges_variables_mensuelles[charge_variable.date.month] += charge_variable.montant
        
        for charge_fixe in charfix:
            charges_fixe_mensuelles[charge_fixe.date.month] += charge_fixe.montant
        
        for piec in piecs:
            piece_mensuelles[piec.date_achat.month] += piec.cout
            
        recette_mois_data = [recettes_mensuelles[month] for month in range(1, 13)]
        recette_mois_data = [0 if recette == 0 else recette_mois_data[i - 1] for i, recette in enumerate(recette_mois_data, start=1)]
        context['recette_mois_data'] = recette_mois_data
        context['label_recette_mois'] = [month[:2] for month in list(calendar.month_name)[1:]]
        
        charg_fixe_mois_data = [charges_fixe_mensuelles[month] for month in range(1, 13)]
        charg_fixe_mois_data = [0 if charge_fixe == 0 else charg_fixe_mois_data[i - 1] for i, charge_fixe in enumerate(charg_fixe_mois_data, start=1)]
        context['charg_fixe_mois_data'] = charg_fixe_mois_data
        
        charg_vari_mois_data = [charges_variables_mensuelles[month] for month in range(1, 13)]
        charg_vari_mois_data = [0 if charge_variable == 0 else charg_vari_mois_data[i - 1] for i, charge_variable in enumerate(charg_vari_mois_data, start=1)]
        context['charg_vari_mois_data'] = charg_vari_mois_data
        
        piece_mois_data = [piece_mensuelles[month] for month in range(1, 13)]
        context['piece_mois_data'] = [0 if piec == 0 else piece_mois_data[i - 1] for i, piec in enumerate(piece_mois_data, start=1)]
           
        mois = list(range(1, 13))
        total_recettes_mois = [0] * 12
        total_charges_variables_mois = [0] * 12
        
        for re in recette_mois:
            total_recettes_mois[re['mois_de_recettes'] - 1] = re['total_recet']
        for chvar in charg_var_mois:
            total_charges_variables_mois[chvar['month_chvar'] - 1] = chvar['total_chvar']
        context['taux_mois'] = [round(((total_recet - chvar) * 100) / total_recet, 2) if total_recet > 0 else 0 for total_recet, chvar in zip(total_recettes_mois, total_charges_variables_mois)]
    
        mois_noms = [calendar.month_name[mois][:2] for mois in mois]
        context['mois_noms'] = mois_noms
        
        context['label_mois'] = [month[:2] for month in list(calendar.month_name)[1:]]
        
        #somme_recettes_par_categorie_aujourd = []
        #for categorie in categories:
        #    vehicules_categorie = Vehicule.objects.filter(category=categorie)
        #    recettes_categorie = Recette.objects.filter(vehicule__in=vehicules_categorie, date=date.today())
        #    somme_recette = recettes_categorie.aggregate(Sum('montant'))['montant__sum'] or 0
        #    somme_recettes_par_categorie_aujourd.append({
        #        'categorie': categorie.category,
        #        'somme_recette': somme_recette
        #    })
        #print("------------Aujourd'hui--------------", somme_recettes_par_categorie_aujourd)
        
        context['catego_vehi'] = catego_vehi
        context['marge_contri'] = marge_contri
        context['total_piece'] = total_piece
        context['month_piece'] = month_piece
        context['Total_recette_format'] = Total_recette_format
        context['Total_charg_fix_format'] = Total_charg_fix_format
        context['Total_charg_var_format'] = Total_charg_var_format
        context['total_charge_format'] = total_charge_format
        context['taux_marge_format'] = taux_marge_format
        context['resultat_format'] = resultat_format
        context['totl_piece_format'] = totl_piece_format
        context['catego_vehi'] = catego_vehi
        return context


class BilletageView(CreateView):
    model = Billetage
    form_class = BilletageForm
    template_name = 'news/appl/billetage.html'
    success_message = 'Saisie éffectuée avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('saise_billetage')
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
        context['Date'] = date.today()
        return context

class AddDecaissementView(CreateView):
    model = Decaissement_Journalier
    form_class = Decaissement_JournalierForm
    template_name = 'news/appl/add_decaissement.html'
    success_message = 'Sortie de caisse enregistrée avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('bilan_journalier')
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
        return context

class UpdatDecaissementView(UpdateView):
    model = Decaissement_Journalier
    form_class = UpdatDecaissement_JournalierForm
    template_name = 'news/appl/updat_decaissement.html'
    success_message = 'Sortir de caisse Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('list_decaissement')
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
        return context

class ListDecaissementView(ListView):
    model = Decaissement_Journalier
    template_name = 'news/applist/list_decaissement.html' 
    context_object_name = 'listvehi'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_decais'] = Decaissement_Journalier.objects.filter(date__range=[date_debut, date_fin])
            print("***********************", context['all_decais'])
        context['form'] = form
        return context
    
class DeletDecaissementView(DeleteView):
    model = Decaissement_Journalier
    template_name = 'news/appl/delet_decaissement.html' 
    success_message = 'Sortie de caisse Supprimé avec succès👍✓✓'
    success_url = reverse_lazy ('list_decaissement')
    def form_valid(self, form):
        reponse =  super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
      
class DetailDecaissementView(DetailView):
    model = Decaissement_Journalier
    template_name = 'news/applist/detail_decaissement.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context

class AddEncaissementView(CreateView):
    model = Encaissement_Journalier
    form_class = Encaissement_JournalierForm
    template_name = 'news/appl/add_encaissement.html'
    success_message = 'Entrée de caisse enregistrée avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('bilan_journalier')
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
        return context
    
class AddSoldeJourView(CreateView):
    model = SoldeJour
    form_class = Solde_JourForm
    template_name = 'news/appl/solde_jour.html'
    success_message = 'Solde de la journée enregistrée avec succès👍✓✓'
    error_message = "Un solde existe deja pour cette journée ✘✘ "
    success_url = reverse_lazy ('bilan_journalier')
    def form_valid(self, form):
        # Vérifie si un solde existe déjà pour la date spécifiée
        date = form.cleaned_data['date']
        solde_exist = SoldeJour.objects.filter(date=date).exists()
        if solde_exist:
            # Si un solde existe déjà pour cette date, renvoie une erreur
            form.add_error('date', 'Un solde existe déjà pour cette date.')
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
    
class UpdatEncaissementView(UpdateView):
    model = Encaissement_Journalier
    form_class = UpdatEncaissement_JournalierForm
    template_name = 'news/appl/updat_encaissement.html'
    success_message = 'Entrée de caisse Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('list_encaissement')
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
        return context

class ListEncaissementView(ListView):
    model = Encaissement_Journalier
    template_name = 'news/applist/list_encaissement.html' 
    context_object_name = 'listvehi'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_encais'] = Encaissement_Journalier.objects.filter(date__range=[date_debut, date_fin])
        context['form'] = form
        return context
    
class DeletEncaissementView(DeleteView):
    model = Encaissement_Journalier
    template_name = 'news/appl/delet_encaissement.html' 
    success_message = 'Entrée de caisse Supprimé avec succès👍✓✓'
    success_url =reverse_lazy ('list_encaissement')
    def form_valid(self, form):
        reponse =  super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        return context
    
class DetailEncaissementView(DetailView):
    model = Encaissement_Journalier
    template_name = 'news/applist/detail_encaissement.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        return context

class BilanJournalierView(TemplateView):
    template_name = 'news/appl/bilan_journalier.html'
    form_class = DatebilanForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        #recettes_taxi = Recette.objects.filter(vehicule__category__category='Taxi', date=date.today()).aggregate(Sum('montant'))['montant__sum'] or 0
        #recettes_yango = Recette.objects.filter(vehicule__category__category='Yango', date=date.today()).aggregate(Sum('montant'))['montant__sum'] or 0
        
        form = DatebilanForm(self.request.GET)
        if form.is_valid():
            date_bilan = form.cleaned_data['date_bilan']
            context['total_entrees'] = Encaissement_Journalier.objects.filter(date=date_bilan).aggregate(Sum('montant'))['montant__sum'] or 0
            context['total_sorties'] = Decaissement_Journalier.objects.filter(date=date_bilan).aggregate(Sum('montant'))['montant__sum'] or 0
            context['en_caisser'] = Encaissement_Journalier.objects.filter(date=date_bilan)
            context['de_caisser'] = Decaissement_Journalier.objects.filter(date=date_bilan)
            
            # Récupérer le solde de début de journée du jour précédent
            solde_debut_jour = SoldeJour.objects.filter(date=date_bilan - timedelta(days=1)).first()
            context['solde_deb_jour'] = solde_debut_jour.montant if solde_debut_jour else 0
            
            solde_init = SoldeJour.objects.filter(date=date_bilan - timedelta(days=2)).last()
            #solde_init = SoldeJour.objects.order_by('date').last()
            solde_init = solde_init.montant if solde_init else 0
            # Récupérer le solde initial du jour précédent
            solde_initial_preced = SoldeJour.objects.filter(date=date_bilan - timedelta(days=1)).aggregate(Sum('montant'))['montant__sum'] or 0
            solde_initial_preced = solde_initial_preced if solde_initial_preced else solde_init

            context['solde_init'] = solde_init
            context['solde_initial_preced'] = solde_initial_preced
            context['tot_entree_jour'] = context['total_entrees'] + context['solde_initial_preced']
            context['solde_final'] = context['total_entrees'] + context['solde_initial_preced'] - context['total_sorties']
            
            billet = Billetage.objects.filter(type_valeur='Billet', date_saisie=date_bilan)
            bille = []              
            som_tot_bill = 0
            for b in billet:
                val = b.valeur
                nb = b.nombre   
                res = b.valeur * b.nombre   
                som_tot_bill += res or 0    
                bille.append({'val': val, 'nb':nb,'res':res})
            context['som_tot_bill'] = som_tot_bill
            context['bille'] = bille

            piece = Billetage.objects.filter(type_valeur='Piece', date_saisie=date_bilan)
            piec = []
            som_tot_piece = 0
            for p in piece:
                val = p.valeur or 0
                nb = p.nombre or 0
                res = p.valeur * p.nombre
                som_tot_piece += res or 0
                piec.append({'val': val, 'nb':nb,'res':res})
            context['som_tot_piece'] = som_tot_piece
            context['piec'] = piec

            context['data'] = date_bilan
            context['billet'] = billet
            context['piece'] = piece
            context['total_piece_bille'] = context['som_tot_piece'] + context['som_tot_bill']
            context['diff'] = context['solde_final'] - context['total_piece_bille']

        context['form'] = form
        context['encaisser'] = Encaissement_Journalier.objects.filter(date=date.today())
        context['decaisser'] = Decaissement_Journalier.objects.filter(date=date.today())
        
        jour = SoldeJour.objects.filter(date=date.today()).aggregate(Sum('montant'))['montant__sum'] or 0
        
        context['Date'] = date.today()
        
        # Calculer le total des encaissements pour la journée actuelle
        context['entree'] = Encaissement_Journalier.objects.filter(date=date.today()).aggregate(Sum('montant'))['montant__sum'] or 0
        context['sortie'] = Decaissement_Journalier.objects.filter(date=date.today()).aggregate(Sum('montant'))['montant__sum'] or 0
        date_courante = date.today()

        # Récupérer le solde de début de journée du jour précédent
        solde_debut_jour = SoldeJour.objects.filter(date=date_courante - timedelta(days=1)).first()
        context['solde_deb_jour'] = solde_debut_jour.montant if solde_debut_jour else 0
        
        # Récupérer le solde initial (le premier solde enregistré)
        #solde_initializ = SoldeJour.objects.order_by('date').first()
        solde_initializ = SoldeJour.objects.filter(date=date_courante - timedelta(days=2)).last()
        
        solde_initializ = solde_initializ.montant if solde_initializ else 0
        # Récupérer le solde initial du jour précédent
        solde_initial_precedent = SoldeJour.objects.filter(date=date_courante - timedelta(days=1)).aggregate(Sum('montant'))['montant__sum'] or 0
        solde_initial_precedent = solde_initial_precedent if solde_initial_precedent else solde_initializ
        
        context['solde_initializ'] = solde_initializ
        context['solde_deb_jour'] =  context['solde_deb_jour']
        context['solde_initial_precedent'] = solde_initial_precedent
        context['Tot_entree'] = context['entree'] + context['solde_initial_precedent']
        
        context['solde_fin_journee'] = context['entree'] + context['solde_initial_precedent'] - context['sortie']
        
        som_billets = Billetage.objects.filter(type_valeur='Billet', date_saisie=date.today()).aggregate(Sum('valeur'))['valeur__sum'] or 0
        nb_bill = Billetage.objects.filter(type_valeur='Billet', date_saisie=date.today()).count() 
        
        som_pieces = Billetage.objects.filter(type_valeur='Piece', date_saisie=date.today()).aggregate(Sum('valeur'))['valeur__sum'] or 0
        context['som_billets'] = som_billets
        context['som_pieces'] = som_pieces
        
        bill = Billetage.objects.filter(type_valeur='Billet', date_saisie=date.today())
        bil = []
        som_tot_bil = 0
        for b in bill:
            val = b.valeur
            nb = b.nombre
            res = b.valeur * b.nombre
            som_tot_bil += res or 0
            bil.append({'val': val, 'nb':nb,'res':res})
        context['som_tot_bil'] = som_tot_bil
        context['bil'] = bil
        
        piece = Billetage.objects.filter(type_valeur='Piece', date_saisie=date.today())
        pie = []
        som_tot_piec = 0
        for p in piece:
            val = p.valeur or 0
            nb = p.nombre or 0
            res = p.valeur * p.nombre
            som_tot_piec += res or 0
            pie.append({'val': val, 'nb':nb,'res':res})
        context['som_tot_piec'] = som_tot_piec
        context['pie'] = pie
        context['Total_piec_bill'] = context['som_tot_piec'] + context['som_tot_bil']
        context['ecart'] = context['solde_fin_journee'] - context['Total_piec_bill']
        
        #self.request.user.last_login_solde = solde_init
        self.request.user.save()
        return context
    


class dashgaragView(TemplateView):
    template_name = 'news/appl/dash_garag.html'
    def get_context_data(self,*args, **kwargs):  
        context = super().get_context_data(*args,**kwargs)  
        user_group = self.request.user.groups.first()   
        context['user_group'] =user_group.name if user_group else None  
        now = datetime.now()
        context["Entretiens"] = Entretien.objects.filter(Q(date_Entretien__lte=now) & Q(date_proch_Entretien__gte=now)).count()
        context["Visites"] = VisiteTechnique.objects.filter(Q(date_visite__lte=now) & Q(date_prochaine_visite__gte=now)).count()
        context["Reparations"] = Reparation.objects.filter(Q(date_entree__lte=now) & Q(date_sortie__gte=now)).count()
        context["Assurances"] = Assurance.objects.filter(Q(date__lte=now) & Q(date_proch_assur__gte=now)).count()
        
        context["Vignette"] = Vignette.objects.filter(Q(date__lte=now) & Q(date_prochain_paiement__gte=now)).count()
        context["Patente"] = Patente.objects.filter(Q(date__lte=now) & Q(date_prochain_paiement__gte=now)).count()
        context["Cartstation"] = Cart_Stationnement.objects.filter(Q(date__lte=now) & Q(date_prochain_paiement__gte=now)).count()
        
        all_vehicule =Vehicule.objects.all()
        all_visite = VisiteTechnique.objects.all()
        nb_visit= VisiteTechnique.objects.count()
        nb_entretien= Entretien.objects.count()
        nb_reparation = Reparation.objects.count()
        
        context['nb_vignett'] = Vignette.objects.count()
        context['nb_patente'] = Patente.objects.count()
        context['nb_cartstation'] = Cart_Stationnement.objects.count()
        
        reparation_mois = Reparation.objects.annotate(month=ExtractMonth("date_entree")).values("month").annotate(total=Count("id")).values("month","total").order_by('month')
        month = []
        
        total_reparat = []
        for i in reparation_mois:
            month.append(calendar.month_name[i["month"]][:2])
            total_reparat.append(i['total'])
        
        resultat_vehicule = []
        alert_color = ""
        for vehicule in all_vehicule:
            visite = VisiteTechnique.objects.filter(vehicule = vehicule).order_by('date_visite')
            entretiens = Entretien.objects.filter(vehicule = vehicule).order_by('date_Entretien')
            assurances = Assurance.objects.filter(vehicule = vehicule).order_by('date_proch_assur')
            vignettes = Vignette.objects.filter(vehicule = vehicule).order_by('date_prochain_paiement')
            patentes = Patente.objects.filter(vehicule = vehicule).order_by('date_prochain_paiement')
            cartstaions = Cart_Stationnement.objects.filter(vehicule = vehicule).order_by('date_prochain_paiement')

            jours_cartsta_restant = cartstaions
            if jours_cartsta_restant:
                for cartstaion in jours_cartsta_restant:
                    jours_cartsta_restant = cartstaion.jours_cartsta_restant
                    alert_cartsta_color = 'red' if jours_cartsta_restant <=10 else 'orange' if jours_cartsta_restant < 30 else 'green'
            else: 
                jours_cartsta_restant = ""    
                alert_cartsta_color = ""
            
            jours_pate_restant = patentes
            if jours_pate_restant:
                for patente in jours_pate_restant:
                    jours_pate_restant = patente.jours_pate_restant
                    alert_pate_color = 'red' if jours_pate_restant <=10 else 'orange' if jours_pate_restant < 30 else 'green'
            else: 
                jours_pate_restant = ""    
                alert_pate_color = ""
                
            jours_vign_restant = vignettes
            if jours_vign_restant:
                for vignette in jours_vign_restant:
                    jours_vign_restant = vignette.jours_vign_restant
                    alert_vign_color = 'red' if jours_vign_restant <=10 else 'orange' if jours_vign_restant < 334 else 'green'
            else: 
                jours_vign_restant = ""    
                alert_vign_color = ""
                
            jours_assu_restant = assurances
            if jours_assu_restant:
                for assurance in jours_assu_restant:
                    jours_assu_restant = assurance.jours_assu_restant
                    alert_assu_color = 'red' if jours_assu_restant <=7 else 'orange' if jours_assu_restant < 15 else 'green'
            else: 
                jours_assu_restant = ""    
                alert_assu_color = ""
                
            jours_ent_restant = entretiens
            if jours_ent_restant:
                for entretien in jours_ent_restant:
                    jours_ent_restant = entretien.jours_ent_restant
                    alert_ent_color = 'red' if jours_ent_restant <=3 else 'orange' if jours_ent_restant < 8 else 'green'
            else: 
                jours_ent_restant = " "     
                alert_ent_color = " "    
            jours_restant = visite  
            
            if jours_restant:       
                for visit in jours_restant:         
                    jours_restant = visit.jour_restant      
                    alert_color = 'red' if jours_restant <=32 else 'orange' if jours_restant <92 else 'green'
            else: 
                jours_restant = ""    
                alert_color = ""    
            resultat_vehicule.append({'vehicule': vehicule, 'jours_restant':jours_restant, 'alert_color':alert_color, 'alert_ent_color':alert_ent_color, 'jours_ent_restant':jours_ent_restant,'alert_assu_color':alert_assu_color,'jours_assu_restant':jours_assu_restant,'jours_vign_restant':jours_vign_restant,'alert_vign_color':alert_vign_color, 'jours_pate_restant':jours_pate_restant,'alert_pate_color':alert_pate_color, 'jours_cartsta_restant':jours_cartsta_restant,'alert_cartsta_color':alert_cartsta_color,})

        context['month'] = month
        context['total_reparat'] = total_reparat
        context['reparation_mois'] = reparation_mois
        context['nb_visit'] = nb_visit
        context['nb_entretien'] = nb_entretien
        context['nb_reparation'] = nb_reparation
        context['resultat_vehicule'] = resultat_vehicule
        context['all_vehicule'] = all_vehicule
        return context

class AddVehiculeView(CreateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = 'news/appl/add_vehicule.html'
    success_message = 'véhicule enregistré avec succès👍✓✓'
    error_message = "Erreur de saisie un véhicule enregistré utilise déjà ces informations verifié l'immatriculation, Numero chassis ou la carte grise ✘✘ "
    success_url = reverse_lazy ('add_car')
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
        context['user_group'] =user_group.name if user_group else None
        context['vehicules'] = Vehicule.objects.all()
        return context

class ListVehiculeView(ListView):
    model = Vehicule
    template_name = 'news/applist/list_vehicule.html' 
    context_object_name = 'listvehi'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        context['vehicule'] =Vehicule.objects.all()
        return context

class DetailVehiculeView(DetailView):
    model = Vehicule
    template_name = 'news/appl/dash_car.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        vehicule = self.get_object()
        form = DateForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            recettes = Recette.objects.filter(vehicule = vehicule, date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum'] 
            context['recettes_totales'] = recettes if recettes is not None else 0
            charges_variables = ChargeVariable.objects.filter(vehicule = vehicule, date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']
            context['charges_variables_totales'] = charges_variables if charges_variables is not None else 0
            charges_fixe = ChargeFixe.objects.filter(vehicule = vehicule, date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']
            context['charges_fixes_totales'] = charges_fixe if charges_fixe is not None else 0
            
            context['charges_totales'] =charges_fixe + context['charges_variables_totales'] if charges_fixe is not None else 0
            context['marge_totale'] = recettes - context['charges_variables_totales'] if recettes is not None else 0

            taux_recette = Recette.objects.filter(vehicule = vehicule, date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum'] or 1
            taux_diviseur = context['recettes_totales'] - (context['charges_variables_totales'])
            context['taux_vehicule'] = round(taux_diviseur*100/ taux_recette, 2 ) if taux_recette is not None and taux_diviseur is not None else 0
            
            taux_mois = round(taux_diviseur*100/ taux_recette, 2 ) if taux_recette is not None and taux_diviseur is not None else 0
            context['taux_par_mois'] = [taux_mois] * 12 if taux_recette else [0] * 12
            resultat = (context['recettes_totales'] - context['charges_totales'])
            context['resultat_total']= resultat if resultat is not None else 0
#-------------------------------------------Pour les Graphes---------------------------------------------
            recets = Recette.objects.filter(vehicule = vehicule, date__range=[date_debut, date_fin])
            charvars = ChargeVariable.objects.filter(vehicule = vehicule, date__range=[date_debut, date_fin])
            charfix = ChargeFixe.objects.filter(vehicule = vehicule, date__range=[date_debut, date_fin])
            
            reparations = Reparation.objects.filter(date_entree__range=[date_debut, date_fin],vehicule = vehicule)
            piess = Piece.objects.filter(reparation__in = reparations)
            
            recettes_mensuelles = {month: 0 for month in range(1, 13)}
            charges_variables_mensuelles = {month: 0 for month in range(1, 13)}
            charges_fixe_mensuelles = {month: 0 for month in range(1, 13)}
            piece_mensuelles = {month: 0 for month in range(1, 13)}
            
            for pies in piess:
                piece_mensuelles[pies.date_achat.month] += pies.cout
            for recette in recets:
                recettes_mensuelles[recette.date.month] += recette.montant
            for charge_variable in charvars:
                charges_variables_mensuelles[charge_variable.date.month] += charge_variable.montant
            for charge_fixe in charfix:
                charges_fixe_mensuelles[charge_fixe.date.month] += charge_fixe.montant
            
            piece_vehi_data = [piece_mensuelles[month] for month in range(1, 13)]
            piece_vehi_data = [0 if pies == 0 else piece_vehi_data[i - 1] for i, pies in enumerate(piece_vehi_data, start=1)]
            
            recette_data = [recettes_mensuelles[month] for month in range(1, 13)]
            recette_data = [0 if recette == 0 else recette_data[i - 1] for i, recette in enumerate(recette_data, start=1)]
            
            charg_vari_data = [charges_variables_mensuelles[month] for month in range(1, 13)]
            charg_vari_data = [0 if charge_variable == 0 else charg_vari_data[i - 1] for i, charge_variable in enumerate(charg_vari_data, start=1)]
            
            charg_fixe_data = [charges_fixe_mensuelles[month] for month in range(1, 13)]
            charg_fixe_data = [0 if charge_fixe == 0 else charg_fixe_data[i - 1] for i, charge_fixe in enumerate(charg_fixe_data, start=1)]
            
            marges_mensuelles = {month: recettes_mensuelles[month] - charges_variables_mensuelles[month] for month in range(1, 13)}
            taux_mensuels = {month: (marges_mensuelles[month] * 100) / recettes_mensuelles[month] if recettes_mensuelles[month] > 0 else 0 for month in range(1, 13)}
            context['labels'] = [month[:2] for month in list(calendar.month_name)[1:]]
            
            taux_data = [taux_mensuels[month] for month in range(1, 13)]
            context['taux_data'] = [0 if taux == 0 else taux_data[i - 1] for i, taux in enumerate(taux_data, start=1)]
          
            context['Nbreparation'] = Reparation.objects.filter(date_entree__range=[date_debut, date_fin],vehicule = vehicule).count() or 0
            
            reparations = Reparation.objects.filter(date_entree__range=[date_debut, date_fin],vehicule = vehicule)
            context['som_piece'] = Piece.objects.filter(reparation__in = reparations).aggregate(total_piece=Sum('cout'))['total_piece'] or 0

            context['recette_data'] = recette_data
            context['charg_vari_data'] = charg_vari_data
            context['charg_fixe_data'] = charg_fixe_data 
            context['piece_vehi_data'] = piece_vehi_data
        else:
            recettes = Recette.objects.filter(vehicule = vehicule).aggregate(Sum('montant'))['montant__sum'] or 1
            charge_fix = ChargeFixe.objects.filter(vehicule = vehicule).aggregate(Sum('montant'))['montant__sum'] or 0
            charge_var = ChargeVariable.objects.filter(vehicule = vehicule).aggregate(Sum('montant'))['montant__sum'] or 0

            Total_charge = charge_fix + charge_var
            marg_contr = recettes - charge_var
            taux_marge = (marg_contr*100/(recettes))
            
            taux_marge_format='{:.2f}'.format(taux_marge)
            resultat = recettes-Total_charge
            Nbreparation = Reparation.objects.filter(vehicule = vehicule).count()
            reparations = Reparation.objects.filter(vehicule = vehicule)
            som_piece = Piece.objects.filter(reparation__in = reparations).aggregate(total_piece=Sum('cout'))['total_piece']
            reparation_mois = Reparation.objects.filter(vehicule = vehicule).annotate(month=ExtractMonth("date_entree")).values("month").annotate(total=Count("id")).values("month","total").order_by('month')

            recets = Recette.objects.filter(vehicule = vehicule)
            charvars = ChargeVariable.objects.filter(vehicule = vehicule)
            charfix = ChargeFixe.objects.filter(vehicule = vehicule)
            
            reparations = Reparation.objects.filter(vehicule = vehicule)
            piess = Piece.objects.filter(reparation__in = reparations)
            
            recettes_mensuelles = {month: 0 for month in range(1, 13)}
            charges_variables_mensuelles = {month: 0 for month in range(1, 13)}
            charges_fixe_mensuelles = {month: 0 for month in range(1, 13)}
            piece_mensuelles = {month: 0 for month in range(1, 13)}
            
            for pies in piess:
                piece_mensuelles[pies.date_achat.month] += pies.cout
            for recette in recets:
                recettes_mensuelles[recette.date.month] += recette.montant
            for charge_variable in charvars:
                charges_variables_mensuelles[charge_variable.date.month] += charge_variable.montant
            for charge_fixe in charfix:
                charges_fixe_mensuelles[charge_fixe.date.month] += charge_fixe.montant
            
            piece_vehi_mois_data = [piece_mensuelles[month] for month in range(1, 13)]
            piece_vehi_mois_data = [0 if pies == 0 else piece_vehi_mois_data[i - 1] for i, pies in enumerate(piece_vehi_mois_data, start=1)]
            
            recette_mois_data = [recettes_mensuelles[month] for month in range(1, 13)]
            recette_mois_data = [0 if recette == 0 else recette_mois_data[i - 1] for i, recette in enumerate(recette_mois_data, start=1)]
            
            charg_vari_mois_data = [charges_variables_mensuelles[month] for month in range(1, 13)]
            charg_vari_mois_data = [0 if charge_variable == 0 else charg_vari_mois_data[i - 1] for i, charge_variable in enumerate(charg_vari_mois_data, start=1)]
            
            charg_fixe_mois_data = [charges_fixe_mensuelles[month] for month in range(1, 13)]
            charg_fixe_mois_data = [0 if charge_fixe == 0 else charg_fixe_mois_data[i - 1] for i, charge_fixe in enumerate(charg_fixe_mois_data, start=1)]
            
            marges_mensuelles = {month: recettes_mensuelles[month] - charges_variables_mensuelles[month] for month in range(1, 13)}
            taux_mensuels = {month: (marges_mensuelles[month] * 100) / recettes_mensuelles[month] if recettes_mensuelles[month] > 0 else 0 for month in range(1, 13)}
            context['labels_mois'] = [month[:2] for month in list(calendar.month_name)[1:]]
            
            
            marges_mensuelles = {month: recettes_mensuelles[month] - charges_variables_mensuelles[month] for month in range(1, 13)}
            taux_mensuels = {month: (marges_mensuelles[month] * 100) / recettes_mensuelles[month] if recettes_mensuelles[month] > 0 else 0 for month in range(1, 13)}
            
            taux_mois_data = [taux_mensuels[month] for month in range(1, 13)]
            context['taux_mois_data'] = [0 if taux == 0 else taux_mois_data[i - 1] for i, taux in enumerate(taux_mois_data, start=1)]
              
            context['recette_mois_data'] = recette_mois_data 
            context['charg_fixe_mois_data'] = charg_fixe_mois_data 
            context['charg_vari_mois_data'] = charg_vari_mois_data 
            context['piece_vehi_mois_data'] = piece_vehi_mois_data 
            context['Nbreparation'] = Nbreparation or 0
            context['som_piece'] = som_piece or 0
            context['charge_fix'] = charge_fix 
            context['charge_var'] = charge_var
            context['Total_charge'] = Total_charge
            context['marg_contr'] = marg_contr
            context['taux_marge_format'] = taux_marge_format
            context['resultat'] = resultat
            context['recettes'] = recettes
        context['form'] = form
        return context 
    
class UpdatVehiculeView(UpdateView):
    model = Vehicule
    form_class =UpdatVehiculeForm
    template_name = 'news/appl/update_vehicule.html'
    success_message = 'véhicule Modifié avec succès👍✓✓'
    error_message = "Erreur de saisie un véhicule enregistré utilise déjà des informations verifié l'immatriculation, Numero chassis ou la carte grise ✘✘ "
    success_url = reverse_lazy ('listvehi')
    def form_valid(self, form):
        reponse = super().form_valid(form)
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
        return context
    
class DeletVehiculeView(DeleteView):
    model = Vehicule
    template_name = 'news/appl/delet_car.html' 
    success_message = 'véhicule Supprimé avec succès👍✓✓'
    success_url =reverse_lazy ('listvehi')
    def form_valid(self, form):
        reponse =  super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        return context
    
class JournalGaragView(TemplateView):
    template_name = 'news/appl/journal_saisi_garag.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicule =Vehicule.objects.all()
        context['vehicule'] = vehicule
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context

class TempArret(TemplateView):
    template_name = 'news/appl/temp_arret.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        vehi = Vehicule.objects.all()
        vehicules = Vehicule.objects.all()
        temps_arret_list = TempsArret.objects.all()
        temps_arrets = TempsArret.objects.count()
        now = datetime.now()
        context["temps_arret_en_cours"] = TempsArret.objects.filter( Q(date_debut__lte=now) & Q(date_fin__gte=now)).count()
        context["temps_arret_passe"] = TempsArret.objects.filter(date_fin__lt=now).count()
        context['temps_arrets_recette'] = TempsArret.objects.aggregate(Sum('recet'))['recet__sum']
        form_arret = DateFormArret(self.request.GET)
        if form_arret.is_valid():
            date_debut = form_arret.cleaned_data['date_debut'] 
            date_fin = form_arret.cleaned_data['date_fin']
            context['tot_recet'] = TempsArret.objects.filter(date_debut__range=[date_debut, date_fin]).aggregate(Sum('recet'))['recet__sum'] or 0
            temps_arrets = TempsArret.objects.filter(date_debut__range=[date_debut, date_fin]).count()
            temps_arret_data = []
            for vehicule in vehicules:
                temps_arret = TempsArret.objects.filter(date_debut__range=[date_debut, date_fin],vehicule=vehicule)
                total_temps_arret = temps_arret.count()
                total_recette = temps_arret.aggregate(Sum('recet'))['recet__sum'] or 0
                motif_counts = {
                    'Reparation': temps_arret.filter(motif='Reparation').count(),
                    'Accident': temps_arret.filter(motif='Accident').count(),
                    'Visite': temps_arret.filter(motif='Visite').count(),
                    'Entretien': temps_arret.filter(motif='Entretien').count(),
                    'Autre': temps_arret.filter(motif='Autre').count(),
                    'Autres': temps_arret.filter(motif='Autre').values('motif'),
                    'motif_autre': temps_arret.filter(motif_autre='motif_autre').values('motif_autre'),
                }
                temps_arret_data.append({'vehicule': vehicule, 'total_temps_arret': total_temps_arret, 'total_recette': total_recette, 'motif_counts': motif_counts,})
            
            context['temps_arret_data'] = temps_arret_data
            context['vehi'] = vehi
            context['temps_arrets'] = temps_arrets
            context['form_arret'] = form_arret
        else:    
            temps_arret_data = []
            for vehicule in vehicules:
                temps_arret = TempsArret.objects.filter(vehicule=vehicule)
                total_temps_arret = temps_arret.count()
                total_recette = temps_arret.aggregate(Sum('recet'))['recet__sum'] or 0
                motif_counts = {
                    'Reparation': temps_arret.filter(motif='Reparation').count(),
                    'Accident': temps_arret.filter(motif='Accident').count(),
                    'Visite': temps_arret.filter(motif='Visite').count(),
                    'Entretien': temps_arret.filter(motif='Entretien').count(),
                    'Autre': temps_arret.filter(motif='Autre').count(),
                    'Autres': temps_arret.filter(motif='Autre').values('motif'),
                    'motif_autre': temps_arret.filter(motif_autre='motif_autre').values('motif_autre'),
                }
                temps_arret_data.append({'vehicule': vehicule, 'total_temps_arret': total_temps_arret, 'total_recette': total_recette, 'motif_counts': motif_counts,})
            context['temps_arret_data'] = temps_arret_data
            context['vehi'] = vehi
            context['temps_arrets'] = temps_arrets 
        context['form_arret'] = form_arret
        return context 
 
class AddTempArretView(CreateView):
    model = TempsArret
    template_name= 'news/appl/add_temp_arret.html'
    form_class = AddTempsArretForm
    success_message = "Temps d'arrêt Ajouté avec succès👍✓✓"
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy('temp_arret')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
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

class ListTempArretView(ListView):
    model = TempsArret
    template_name = 'news/applist/list_temps_arret.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_tempar'] = TempsArret.objects.filter(date_debut__range=[date_debut, date_fin])
        context['form'] = form
        return context
    
class UpdatTemp_arretView(UpdateView):
    model = TempsArret
    template_name= 'news/appl/updat_temp_arret.html'
    form_class = UpdatTempsArretForm
    success_message = "Temps d'arrêt modifié avec succès👍✓✓"
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy('temp_arret')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def form_invalid(self, form):
        reponse = super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
    
class Detail_temp_arretView(DetailView):
    model = TempsArret
    template_name = "news/applist/detail_temp_arret.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
    
class DeletTemp_arretView(DeleteView):
    model = TempsArret
    template_name= 'news/appl/delet_temp_arret.html'
    success_message = "Temps d'arrêt supprimé avec succès👍✓✓"
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy('temp_arret')
    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
    
class DashbComptView(TemplateView):
    template_name = 'news/appl/journal_saisi_compta.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        vehicule =Vehicule.objects.all()
        catego_vehi = CategoVehi.objects.all().annotate(vehicule_count=Count("category"))
        recette= Recette.objects.all()
        Total_recettes = sum(recet.montant for recet in recette)
        Total_recette_format ='{:,}'.format(Total_recettes).replace('',' ')
        
#_____________________________TOTAL DES CHARGES VARIABLES_____________________________#
        cahargevariable = ChargeVariable.objects.all()
        Total_charg_var = sum(chargvar.montant for chargvar in cahargevariable)
        Total_charg_var_format ='{:,}'.format(Total_charg_var).replace('',' ')
#_____________________________TOTAL DES CHARGES FIXES_____________________________#       
        chargefix = ChargeFixe.objects.all()
        Total_charg_fix = sum(chargfix.montant for chargfix in chargefix)
        Total_charg_fix_format ='{:,}'.format(Total_charg_fix).replace('',' ')
#_____________________________TOTAL DES CHARGES_____________________________#
        total_charg = Total_charg_fix + Total_charg_var
        total_charge_format ='{:,}'.format(total_charg).replace('',' ')
#_____________________________MARGE CONTRIBUTION_____________________________#
        marge_contribution = Total_recettes - Total_charg_var
#_____________________________TAUX CONTRIBUTION_____________________________#
        if Total_recettes == 0:
            taux_marge = 0
        else:
            taux_marge = (marge_contribution*100/(Total_recettes))
        taux_marge_format ='{:.2f}'.format(taux_marge)
#_____________________________RESULTAT_____________________________#
        resultat = Total_recettes - total_charg
        resultat_format ='{:,}'.format(resultat).replace('',' ')
        
        piece = Piece.objects.all()
        totl_piece = sum(piece.cout for piece in piece)
        totl_piece_format ='{:,}'.format(totl_piece).replace('',' ')
        
        context['Total_recette_format'] = Total_recette_format
        context['Total_charg_fix_format'] = Total_charg_fix_format
        context['Total_charg_var_format'] = Total_charg_var_format
        context['total_charge_format'] = total_charge_format
        context['taux_marge_format'] = taux_marge_format
        context['resultat_format'] = resultat_format
        context['totl_piece_format'] = totl_piece_format
        context['catego_vehi'] = catego_vehi
        context['vehicule']=vehicule
        return context

#------------------------------COMPTABLE-------------------------------
class AddRecetteView(CreateView):
    model = Recette
    form_class = RecetteForm
    template_name= "news/appl/add_recette.html"
    success_message = 'Recette Ajoutée avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy('journal_compta')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
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
        context['recettes'] = Recette.objects.all()
        return context  

class ListRecetView(ListView):
    model = Recette
    template_name = 'news/applist/list_recet.html'
    context_object = 'listrecet'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['All_recet'] = Recette.objects.filter(date__range=[date_debut, date_fin])
            print("***********************", context['All_recet'])
        context['form'] = form
        return context 
    
class UpdateRecetView(UpdateView):
    model = Recette
    form_class = UpdateRecetteForm
    template_name = "news/appl/update_recette.html"
    context_object = 'listvehi'  
    success_message = 'Recette Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie✘✘ "
    success_url = reverse_lazy ('listrecet')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def form_invalid(self, form):
        reponse = super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 

class DetailRecetteView(DetailView):
    model = Recette
    template_name = "news/applist/detail_recette.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
    
class DeletRecetteView(DeleteView):
    model = Recette
    template_name = 'news/appl/delet_recette.html' 
    success_message = 'Recette Supprimé avec succès👍✓✓'
    success_url =reverse_lazy ('listrecet')
    def form_valid(self, form):
        reponse =  super().form_valid(form)
        messages.success(self.request, self.success_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        return context

class AddChargeFixView(CreateView):
    model = ChargeFixe
    form_class = ChargeFixForm
    template_name= "news/appl/add_charg_fix.html"
    success_message = 'Saisie de charge effectuée avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('journal_compta')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        context['charfix'] = ChargeFixe.objects.all()
        return context
    
class DetailChargeFixeView(DetailView):
    model = ChargeFixe
    template_name = "news/applist/detail_charg_fix.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
    
class ListChargeFixView(ListView):
    model = ChargeFixe
    template_name = 'news/applist/list_charg_fix.html'
    context_object = 'list_charg_fix'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['charg_fix'] = ChargeFixe.objects.all()
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_charfix'] = ChargeFixe.objects.filter(date__range=[date_debut, date_fin])
            print("***********************", context['all_charfix'])
        context['form'] = form
        return context

class UpdateChargFixView(UpdateView):
    model = ChargeFixe
    form_class = UpdatChargeFixForm
    template_name = "news/appl/update_charg_fix.html"
    context_object = 'listvehi'  
    success_message = 'Charge Fixe Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie✘✘ "
    success_url = reverse_lazy ('list_charg_fix')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        return context 
    
class DeletChargFixView(DeleteView):
    model = ChargeFixe
    template_name = 'news/appl/delet_charg_fix.html' 
    success_message = 'Charge Fixe Supprimée avec succès👍✓✓'
    success_url =reverse_lazy ('list_charg_fix')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context   
    
class AddChargeVarView(CreateView):
    model = ChargeVariable
    form_class = ChargeVarForm
    template_name= "news/appl/add_charg_var.html"
    success_message = 'Saisie de charge effectuée avec succès👍✓✓'
    success_url = reverse_lazy ('journal_compta')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        context['charvar'] = ChargeVariable.objects.all()
        return context

class DetailChargeVarView(DetailView):
    model = ChargeVariable
    template_name = "news/applist/detail_charg_vari.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
    
class ListChargeVarView(ListView):
    model = ChargeVariable
    template_name = 'news/applist/list_charg_var.html'
    context_object = 'list_charg_var'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        context['charg_var'] =ChargeVariable.objects.all()
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_charvar'] = ChargeVariable.objects.filter(date__range=[date_debut, date_fin])
            print("***********************", context['all_charvar'])
        context['form'] = form
        return context

class UpdateChargeVarView(UpdateView):
    model = ChargeVariable
    form_class = updatChargeVarForm
    template_name = "news/appl/update_charg_vari.html"
    context_object = 'listvehi'  
    success_message = 'Charge Variable Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie✘✘"
    success_url = reverse_lazy ('list_charg_var')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
    
class DeletChargeVarView(DeleteView):
    model = ChargeVariable
    template_name = 'news/appl/delet_charg_vari.html' 
    success_message = 'Charge Variable Supprimée avec succès👍✓✓'
    success_url =reverse_lazy ('list_charg_var')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context  

#class DetailAdminisView(DetailView):
#    model = ChargeAdminis

class AddChargeAdminisView(CreateView):
    model = ChargeAdminis
    form_class = ChargeAdminisForm
    template_name = 'news/appl/add_charg_admin.html'
    success_message = 'Charge administrative enregistrée avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('add_charg_administ')
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
        context['chargadminist'] = ChargeAdminis.objects.all()
        recette= Recette.objects.all()
        Total_recettes = sum(recet.montant for recet in recette)
        context['Total_recette_format'] ='{:,}'.format(Total_recettes).replace('',' ')
        
        form_admin = DateForm(self.request.GET)
        if form_admin.is_valid():
            date_debut = form_admin.cleaned_data['date_debut'] 
            date_fin = form_admin.cleaned_data['date_fin']   
            
            context['charge_adminis_all'] = ChargeAdminis.objects.filter(date__range=[date_debut, date_fin])
            
            recettes = Recette.objects.filter(date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum'] 
            context['recettes_totales'] = recettes if recettes is not None else 0
            
            charges_variables = ChargeVariable.objects.filter(date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']
            context['charges_variables_totales'] = charges_variables if charges_variables is not None else 0
            
            charges_fixe = ChargeFixe.objects.filter(date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']
            context['charges_fixes_totales'] = charges_fixe if charges_fixe is not None else 0
            
            charges_adminis = ChargeAdminis.objects.filter(date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum']
            context['charges_adminis_totales'] = charges_adminis if charges_adminis is not None else 0
            
            context['Somme_charge_Totale'] = context['charges_variables_totales'] + context['charges_fixes_totales'] + context['charges_adminis_totales']
            
            context['charges_totales'] = charges_fixe + context['charges_variables_totales'] if charges_fixe is not None else 0

            context['marge_totale'] = recettes - context['charges_variables_totales'] if recettes is not None else 0

            taux_recette = Recette.objects.filter(date__range=[date_debut, date_fin]).aggregate(Sum('montant'))['montant__sum'] or 1
            taux_diviseur = context['recettes_totales'] - (context['charges_variables_totales'])
            
            context['taux_vehi'] = round(taux_diviseur*100/ taux_recette, 2 ) if taux_recette is not None and taux_diviseur is not None else 0
            
            taux_mois= round(taux_diviseur*100/ taux_recette, 2 ) if taux_recette is not None and taux_diviseur is not None else 0
            context['taux_par_mois'] = [taux_mois] * 12 if taux_recette else [0] * 12

            resultat = (context['recettes_totales'] - context['Somme_charge_Totale'])
            context['resultat_total'] = resultat if resultat is not None else 0
#-------------------------------------------Pour les Graphes---------------------------------------------

            chargadmin = ChargeAdminis.objects.filter(date__range=[date_debut, date_fin])
            charg_adminis_mensuelles = {month: 0 for month in range(1, 13)}
            for charge_admin in chargadmin:
                charg_adminis_mensuelles[charge_admin.date.month] += charge_admin.montant
            
            charg_administ_data = [charg_adminis_mensuelles[month] for month in range(1, 13)]
            context['charg_administ_data'] = [0 if charge_admin == 0 else charg_administ_data[i - 1] for i, charge_admin in enumerate(charg_administ_data, start=1)]
            context['labels'] = [month[:2] for month in list(calendar.month_name)[1:]]
            
        chargeadminist = ChargeAdminis.objects.all()
        Total_charg_admin = sum(chargadmin.montant for chargadmin in chargeadminist)
        context['Total_charg_admin_format'] = '{:,}'.format(Total_charg_admin).replace('',' ')
        #______________________TOTAL DES CHARGES VARIABLES_____________________________#
        chargevariable = ChargeVariable.objects.all()
        Total_charg_var = sum(chargvar.montant for chargvar in chargevariable)
        context['Total_charg_var_format'] ='{:,}'.format(Total_charg_var).replace('',' ')
#_____________________________TOTAL DES CHARGES FIXES_____________________________#       
        chargefix = ChargeFixe.objects.all()
        Total_charg_fix = sum(chargfix.montant for chargfix in chargefix)
        context['Total_charg_fix_format'] ='{:,}'.format(Total_charg_fix).replace('',' ')
#_____________________________TOTAL DES CHARGES_____________________________#
        total_charg = Total_charg_fix + Total_charg_var + Total_charg_admin
        context['total_charge_format'] ='{:,}'.format(total_charg).replace('',' ')
#_____________________________MARGE CONTRIBUTION_____________________________#
        marge_contribution = Total_recettes - Total_charg_var

        marg_brut = Total_charg_fix + Total_charg_var
        marg_brute = Total_recettes - marg_brut
        context['marg_brute_format'] ='{:,}'.format(marg_brute).replace('',' ')
#_____________________________TAUX CONTRIBUTION_____________________________#
        if Total_recettes == 0:
            taux_marge = 0
        else:
            taux_marge = (marge_contribution*100/(Total_recettes))
        context['taux_marge_format'] ='{:.2f}'.format(taux_marge)
#_____________________________RESULTAT_____________________________#
        resultat = marg_brute - Total_charg_admin
        context['resultat_format'] ='{:,}'.format(resultat).replace('',' ')
        context['form_admin'] = form_admin
        charg_admin = ChargeAdminis.objects.all()
        charg_adminis_mensuelles = {month: 0 for month in range(1, 13)}
        for charge_admin in charg_admin:
            charg_adminis_mensuelles[charge_admin.date.month] += charge_admin.montant
            
        charg_administ_mois = [charg_adminis_mensuelles[month] for month in range(1, 13)]
        context['charg_administ_mois'] = [0 if charge_admin == 0 else charg_administ_mois[i - 1] for i, charge_admin in enumerate(charg_administ_mois, start=1)]
        context['labels_mois'] = [month[:2] for month in list(calendar.month_name)[1:]]
        return context   

#----------------------------Garage-------------------------------
class AddCartStationView(CreateView):
    model = Cart_Stationnement
    form_class = CartStationForm
    template_name= "news/appl/add_cartestation.html"
    success_message = 'Saisie de carte de station éffectuée avec succès👍✓✓'
    success_url = reverse_lazy ('journal_garag')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,self.error_message)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        return context
    
class UpdatCartStationView(UpdateView):
    model = Cart_Stationnement
    form_class = UpdatCartStationForm
    template_name= "news/appl/updat_cartestation.html"
    success_message = 'Modification de carte de station éffectuée avec succès👍✓✓'
    success_url = reverse_lazy ('list_cart_station')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        return context

class DetailCartStationView(DetailView):
    model = Cart_Stationnement
    template_name = "news/applist/detail_cartestation.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
         
class DeletCartStationView(DeleteView):
    model = Cart_Stationnement
    template_name= "news/appl/delet_cartestation.html"
    success_message = 'Suppression de carte de station éffectuée avec succès👍✓✓'
    success_url = reverse_lazy ('list_cart_station')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
    
class ListCartStationView(ListView):
    model = Cart_Stationnement
    template_name = 'news/applist/list_cartstation.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_cart'] = Cart_Stationnement.objects.filter(date__range=[date_debut, date_fin])
        context['form'] = form 
        return context

class AddPatenteView(CreateView):
    model = Patente
    form_class = PatenteForm
    template_name= "news/appl/add_patente.html"
    success_message = 'Saisie de Patente effectuée avec succès👍✓✓'
    success_url = reverse_lazy ('journal_garag')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,self.error_message)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['visites'] = VisiteTechnique.objects.all()
        return context
    
class UpdatPatenteView(UpdateView):
    model = Patente
    form_class = UpdatPatenteForm
    template_name= "news/appl/updat_patente.html"
    success_message = 'Saisie de Patente modifiée avec succès👍✓✓'
    success_url = reverse_lazy ('list_patente')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['visites'] = VisiteTechnique.objects.all()
        return context

class DeletPatenteView(DeleteView):
    model = Patente
    template_name= "news/appl/delet_patente.html"
    success_message = 'Suppression de Patente éffectuée avec succès👍✓✓'
    success_url = reverse_lazy ('list_patente')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 

class DetailPatenteView(DetailView):
    model = Patente
    template_name = "news/applist/detail_patente.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context

class ListPatenteView(ListView):
    model = Patente
    template_name = 'news/applist/list_patente.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_pat'] = Patente.objects.filter(date__range=[date_debut, date_fin])
        context['form'] = form
        return context

class AddVignetteView(CreateView):
    model = Vignette
    form_class = VignetteForm
    template_name= "news/appl/add_vignette.html"
    success_message = 'Saisie de Vignette effectuée avec succès👍✓✓'
    success_url = reverse_lazy ('journal_garag')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,self.error_message)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        return context


class DetailVignetteView(DetailView):
    model = Vignette
    template_name = "news/applist/detail_vignette.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context

class UpdatVignetteView(UpdateView):
    model = Vignette
    form_class = UpdatVignetteForm
    template_name = "news/appl/updat_vignette.html"
    success_message = 'Saisie de Vignette effectuée avec succès👍✓✓'
    success_url = reverse_lazy ('list_vignet')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] =user_group.name if user_group else None
        context['visites'] = VisiteTechnique.objects.all()
        return context

class DeletVignetteView(DeleteView): 
    model = Vignette 
    template_name= "news/appl/delet_vignette.html" 
    success_message = 'Suppression de vignette éffectuée avec succès👍✓✓' 
    success_url = reverse_lazy('list_vignet') 
    def form_valid(self, form): 
        response = super().form_valid(form) 
        messages.success(self.request, self.success_message) 
        return response 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        user_group = self.request.user.groups.first() 
        context['user_group'] = user_group.name if user_group else None 
        return context 

class DetailVignetteView(DetailView):
    model = Vignette
    template_name = "news/applist/detail_vignette.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context

class ListVignetteView(ListView):
    model = Vignette
    template_name = 'news/applist/list_vignette.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_vignet'] = Vignette.objects.filter(date__range=[date_debut, date_fin])
        context['form'] = form
        return context

class AddVisitView(CreateView):
    model = VisiteTechnique
    form_class = VisiteTechniqueForm
    template_name= "news/appl/add_visit.html"
    success_message = 'Saisie de Visiste effectuée avec succès👍✓✓'
    success_url = reverse_lazy ('journal_garag')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,self.error_message)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['visites'] = VisiteTechnique.objects.all()
        return context

class ListVisitView(ListView):
    model = VisiteTechnique
    template_name = 'news/applist/list_visit.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['visites'] = VisiteTechnique.objects.all()  
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_visit'] = VisiteTechnique.objects.filter(date_visite__range=[date_debut, date_fin])
        context['form'] = form  
        return context

class DetailVisiteView(DetailView):
    model = VisiteTechnique
    template_name = "news/applist/detail_visite.html"
    ordoring = ['date_saisie']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 

class UpdateVisiteView(UpdateView):
    model = VisiteTechnique
    form_class = UpdatVisiteTechniqueForm
    template_name = "news/appl/updat_visit.html" 
    success_message = 'Charge Variable Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie✘✘"
    success_url = reverse_lazy ('list_visit')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
    
class DeletVisiteView(DeleteView):
    model = VisiteTechnique
    template_name = 'news/appl/delet_visit.html' 
    success_message = 'Charge Variable Supprimée avec succès👍✓✓'
    success_url = reverse_lazy ('list_visit')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context  
    
class AddAssuranceView(CreateView):
    model = Assurance
    form_class = AssuranceForm
    template_name= "news/appl/add_assurance.html"
    success_message = 'Assurance enregistré avec succès👍✓✓'
    success_url = reverse_lazy ('journal_garag')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,self.error_message)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['assurances'] = Assurance.objects.all()
        return context

class DetailAssuranceView(DetailView):
    model = Assurance
    template_name = "news/applist/detail_assurance.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
    
class ListAssuranceView(ListView):
    model = Assurance
    template_name = 'news/applist/list_assurance.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_assu'] = Assurance.objects.filter(date__range=[date_debut, date_fin])
        context['form'] = form  
        return context

class UpdateAssuranceView(UpdateView):
    model = Assurance
    form_class = UpdatAssuranceForm
    template_name = "news/appl/updat_assurance.html" 
    success_message = 'Assurance Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie✘✘"
    success_url = reverse_lazy ('list_visit')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
    
class DeletAssuranceView(DeleteView):
    model = Assurance
    template_name = 'news/appl/delet_assurance.html' 
    success_message = 'Assurance Supprimée avec succès👍✓✓'
    success_url =reverse_lazy ('list_visit')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context  
    
class AddReparationView(CreateView):
    model = Reparation
    form_class = ReparationForm
    template_name= "news/appl/add_reparation.html"
    success_message = 'Saisie de reparation effectuée avec succès👍✓✓'
    success_url = reverse_lazy ('journal_garag')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,self.error_message)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        
        return context
     
class DetailReparatView(DetailView):
    model = Reparation
    template_name = "news/applist/detail_reparation.html"
    ordoring = ['date_saisie']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        reparation = self.object
        duree_reparation = reparation.date_sortie - reparation.date_entree
        context['heure_rearat'] = duree_reparation.total_seconds() / 3600
        return context 

class UpdateReparationView(UpdateView):
    model = Reparation
    form_class = UpdatReparationForm
    template_name = "news/appl/updat_reparation.html"
    context_object = 'listvehi'  
    success_message = 'Charge Fixe Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie✘✘ "
    success_url = reverse_lazy ('list_repa')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 

class DeletReparationView(DeleteView):
    model = Reparation
    template_name = 'news/appl/delet_reparation.html' 
    success_message = 'Reparation Supprimée avec succès👍✓✓'
    success_url =reverse_lazy ('list_repa')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context  

class AddPieceView(CreateView):
    model = Piece
    form_class = PieceForm
    template_name= "news/appl/add_piece.html"
    success_message = 'Saisie de Piece effectuée avec succès👍✓✓'
    error_message = "cout, Le cout total des pieces ne peut pas être superieur au coût de la reparation"
    success_url = reverse_lazy ('list_repa')
    def form_valid(self, form):
        reparation_id = self.kwargs['pk']
        reparation = Reparation.objects.get(pk=reparation_id)
        cout_piece = Piece.objects.filter(reparation=reparation).aggregate(Sum('cout'))['cout__sum'] or 0
        total_reparation = reparation.cout
        cout_priece_actuel = form.cleaned_data['cout']
        if cout_piece + cout_priece_actuel > total_reparation:
            messages.success(self.request, self.error_message)
            return self.form_invalid(form)
        form.instance.reparation=reparation
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('list_repa')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['pieces'] = Piece.objects.all()
        return context

class DetailPieceView(DetailView):
    model = Piece
    template_name = "news/applist/detail_piece.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
     
class ListPieceView(ListView):
    model = Piece
    template_name = 'news/applist/list_piece.html'
    context_object = 'listpiece'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['pieces'] =Piece.objects.all()
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_piec'] = Piece.objects.filter(date_achat__range=[date_debut, date_fin])
        context['form'] = form
        return context
    
class UpdatPieceView(UpdateView):
    model = Piece
    form_class = UpdatPieceForm
    template_name = "news/appl/updat_piece.html"
    context_object = 'listvehi'  
    success_message = 'Pièce Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie✘✘ "
    success_url = reverse_lazy ('list_piece')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 

class DeletPieceView(DeleteView):
    model = Piece
    template_name = 'news/appl/delet_piece.html' 
    success_message = 'Pièce Supprimée avec succès👍✓✓'
    success_url =reverse_lazy ('list_piece')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context    

class ListReparationView(ListView):
    model = Reparation
    template_name = 'news/applist/list_reparat.html'
    ordering = ['date_saisie']
    context_object = 'listereparation'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['reparations'] = Reparation.objects.all()
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_reparat'] = Reparation.objects.filter(date_entree__range=[date_debut, date_fin])
        context['form'] = form
        return context
     
class AddEntretienView(CreateView):
    model = Entretien
    form_class = EntretienForm
    template_name= "news/appl/add_entretien.html"
    success_message = 'Entretien effectué avec succès👍✓✓'
    error_message = "Erreur de saisie ✘✘ "
    success_url = reverse_lazy ('journal_garag')
    def form_valid(self, form):
        form.instance.vehicule_id = self.kwargs['pk']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,self.error_message)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['entretiens'] = Entretien.objects.all()
        return context


class DetailEntretienView(DetailView):
    model = Entretien
    template_name = "news/applist/detail_entretien.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context
    
class ListEntretienView(ListView):
    model = Entretien
    template_name = 'news/applist/list_entretien.html'
    ordering = ['date_saisie']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['entretiens'] = Entretien.objects.all()
        form = DateAllForm(self.request.GET)
        if form.is_valid():
            date_debut = form.cleaned_data['date_debut'] 
            date_fin = form.cleaned_data['date_fin']
            context['all_ent'] = Entretien.objects.filter(date_Entretien__range=[date_debut, date_fin])
        context['form'] = form
        return context
      
class UpdatEntretienView(UpdateView):
    model = Entretien
    form_class = UpdatEntretienForm
    template_name = "news/appl/update_entretien.html"
    context_object = 'listvehi'  
    success_message = 'Entretien Modifiée avec succès👍✓✓'
    error_message = "Erreur de saisie✘✘ "
    success_url = reverse_lazy ('list_entretien')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def form_invalid(self, form):
        reponse =  super().form_invalid(form)
        messages.success(self.request, self.error_message)
        return reponse
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context 
    
class DeletEntretienView(DeleteView):
    model = Entretien
    template_name = "news/appl/delet_entretien.html"
    success_message = "Entretien Supprimée avec succès👍✓✓"
    success_url =reverse_lazy ('list_entretien')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        return context  

class AddCategoriVehi(CreateView):  
    model = CategoVehi      
    form_class = CategorieForm      
    template_name = 'news/appl/add_catego_vehi.html'
    success_message = 'Categorie enregistré avec succès👍✓✓'
    error_message = "Erreur de saisie, cette categorie ou cet identifiant existe✘✘"
    success_url= reverse_lazy('add_catego_vehi')
    def form_valid(self, form):
        messages.success(self.request,self.success_message)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,self.error_message)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        context['user_group'] = user_group.name if user_group else None
        context['categovehi'] = CategoVehi.objects.all()
        return context
    
def CategoVehiculeListView(request, cid):
    categorys= CategoVehi.objects.get(cid=cid)
    cars = Vehicule.objects.filter(category=categorys)
    user_group = request.user.groups.first()
    user_group = user_group.name if user_group else None
    context = {
        'user_group':user_group,
        'categorys':categorys,
        'cars':cars,
    }
    return render(request, 'news/applist/list_vehi_categor.html',context)

