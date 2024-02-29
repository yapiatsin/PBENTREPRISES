from django import forms
from django.forms import DateInput
from .models import *

class DateForm(forms.Form):
    date_debut = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))
    date_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))

class DatebilanForm(forms.Form):
    date_bilan = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))

class DateFormArret(forms.Form):
    date_debut = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))
    date_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))

class DateAllForm(forms.Form):
    date_debut = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))
    date_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}))

class CategorieForm(forms.ModelForm):
    class Meta:
        model = CategoVehi
        fields = ('cid','category','image')
        widgets = {
            'cid': forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.TextInput(attrs={'class':'form-control'}),
        }

class Solde_JourForm(forms.ModelForm):
    date = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = SoldeJour
        fields = ('montant','date')
        widgets = {
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
        }

class AddTempsArretForm(forms.ModelForm):
    class Meta:
        model = TempsArret
        fields = ('recet','motif','motif_autre','date_debut','date_fin')
        widgets = {
            'recet': forms.NumberInput(attrs={'class':'form-control'}),
            'motif_autre': forms.TextInput(attrs={'class':'form-control'}),
            'motif': forms.Select(attrs={'class':'form-control'}),
            'date_debut' :DateInput(attrs={"type": "datetime-local","class":"form-control"}, format="%Y-%m-%dT%H:%M",),
            'date_fin' :DateInput(attrs={"type": "datetime-local","class":"form-control"}, format="%Y-%m-%dT%H:%M",),
        } 
    def __init__(self, *args, **kwargs):
        super(AddTempsArretForm, self).__init__(*args, **kwargs)
        self.fields["date_debut"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["date_fin"].input_formats = ("%Y-%m-%dT%H:%M",)

class UpdatTempsArretForm(forms.ModelForm):
    class Meta:
        model = TempsArret
        fields = ('recet','motif','motif_autre','date_debut','date_fin')
        widgets = {
            'recet': forms.NumberInput(attrs={'class':'form-control'}),
            'motif_autre': forms.TextInput(attrs={'class':'form-control'}),
            'motif': forms.Select(attrs={'class':'form-control'}),
            'date_debut' :DateInput(attrs={"type": "datetime-local","class":"form-control"}, format="%Y-%m-%dT%H:%M",),
            'date_fin' :DateInput(attrs={"type": "datetime-local","class":"form-control"}, format="%Y-%m-%dT%H:%M",),
        } 
    def __init__(self, *args, **kwargs):
        super(UpdatTempsArretForm, self).__init__(*args, **kwargs)
        self.fields["date_debut"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["date_fin"].input_formats = ("%Y-%m-%dT%H:%M",)

class ChargeAdminisForm(forms.ModelForm):
    date = forms.DateTimeField(widget= forms.DateTimeInput(format=('%m/%d/%Y %H:%M'), attrs={'class':'form-control','format':'yyyy-mm-dd HH-ii ss', 'type':'date'}))
    class Meta:
        model = ChargeAdminis
        fields = ('libelle','montant','cpte_comptable','Num_piece','Num_fact','date')
        widgets = {
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'cpte_comptable': forms.TextInput(attrs={'class':'form-control'}),
            'Num_fact': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.NumberInput(attrs={'class':'form-control'}),
        }
               
class VehiculeForm(forms.ModelForm):
    date_acquisition = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    dat_edit_carte_grise = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    date_mis_service = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Vehicule
        fields = ('immatriculation','marque','duree','image','photo_carte_grise','num_cart_grise','num_Chassis','date_acquisition','cout_acquisition','dat_edit_carte_grise','date_mis_service','category')
        widgets = {
            'immatriculation': forms.TextInput(attrs={'class':'form-control'}),
            'marque': forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'duree': forms.NumberInput(attrs={'class':'form-control'}),
            'num_cart_grise': forms.TextInput(attrs={'class':'form-control'}),
            'num_Chassis': forms.TextInput(attrs={'class':'form-control'}),
            'cout_acquisition': forms.NumberInput(attrs={'class':'form-control'}),
        }
class UpdatVehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ('immatriculation','marque','duree','image','photo_carte_grise','num_cart_grise','num_Chassis','date_acquisition','cout_acquisition','dat_edit_carte_grise','date_mis_service','category')
        widgets = {
            'immatriculation': forms.TextInput(attrs={'class':'form-control'}),
            'marque': forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'duree': forms.NumberInput(attrs={'class':'form-control'}),
            'num_cart_grise': forms.TextInput(attrs={'class':'form-control'}),
            'num_Chassis': forms.TextInput(attrs={'class':'form-control'}),
            'cout_acquisition': forms.NumberInput(attrs={'class':'form-control'}),
            'date_acquisition' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'dat_edit_carte_grise' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'date_mis_service' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
    def __init__(self, *args, **kwargs):
        super(UpdatVehiculeForm, self).__init__(*args, **kwargs)
    def clean_date(self):
        date_acquisition = self.cleaned_data['date_acquisition']
        formatted_date = date_acquisition.strftime('%Y-%m-%d',)
        return formatted_date
    
class BilletageForm(forms.ModelForm):
    class Meta:
        model = Billetage
        fields = ('valeur','nombre','type_valeur')
        widgets = {
            'valeur': forms.Select(attrs={'class':'form-control'}),
            'nombre': forms.NumberInput(attrs={'class':'form-control'}),
            'type_valeur': forms.Select(attrs={'class':'form-control'}),
        }

class CartStationForm(forms.ModelForm):
    date = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    date_prochain_paiement = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Cart_Stationnement
        fields = ('montant','date_prochain_paiement','montant','date','piece_jointe')
        widgets = {
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
        }
      
class UpdatCartStationForm(forms.ModelForm):
    class Meta:
        model = Cart_Stationnement
        fields = ('montant', 'date', 'date_prochain_paiement','piece_jointe')
        widgets = {
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'date': DateInput(attrs={'class':'form-control', 'type':"datetime-local","class":"form-control"}, format='%Y-%m-%dT%H:%M')  ,  
            'date_prochain_paiement': DateInput(attrs={'class':'form-control', 'type':"datetime-local","class":"form-control"}, format='%Y-%m-%dT%H:%M'),
        }
    def __init__(self, *args, **kwargs):
        super(UpdatCartStationForm, self).__init__(*args, **kwargs)
        self.fields["date"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["date_prochain_paiement"].input_formats = ("%Y-%m-%dT%H:%M",)


class PatenteForm(forms.ModelForm):
    date = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    date_prochain_paiement = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Patente
        fields = ('montant','date_prochain_paiement','montant','date','piece_jointe')
        widgets = {
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
        }
        
class UpdatPatenteForm(forms.ModelForm):
    class Meta:
        model = Patente
        fields = ('montant', 'date', 'date_prochain_paiement','piece_jointe')
        widgets = {
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'date': DateInput(attrs={'class':'form-control', 'type':"datetime-local","class":"form-control"}, format='%Y-%m-%dT%H:%M')  ,  
            'date_prochain_paiement': DateInput(attrs={'class':'form-control', 'type':"datetime-local","class":"form-control"}, format='%Y-%m-%dT%H:%M'),
        }
    def __init__(self, *args, **kwargs):
        super(UpdatPatenteForm, self).__init__(*args, **kwargs)
        self.fields["date"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["date_prochain_paiement"].input_formats = ("%Y-%m-%dT%H:%M",)
        
        
class VignetteForm(forms.ModelForm):
    date = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    date_prochain_paiement = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Vignette
        fields = ('montant','date_prochain_paiement','montant','date','piece_jointe')
        widgets = {
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
        }
        
class UpdatVignetteForm(forms.ModelForm):
    class Meta:
        model = Vignette
        fields = ('montant', 'date', 'date_prochain_paiement','piece_jointe')
        widgets = {
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'date_prochain_paiement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d')
        }
    def __init__(self, *args, **kwargs):
        super(UpdatVignetteForm, self).__init__(*args, **kwargs)
    def clean_date(self):
        date = self.cleaned_data['date']
        formatted_date = date.strftime('%Y-%m-%d')
        return formatted_date   
        
class Decaissement_JournalierForm(forms.ModelForm):
    date = forms.DateField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Decaissement_Journalier
        fields = ('Num_piece','libelle','montant','date')
        widgets = {
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
        }
        
class UpdatDecaissement_JournalierForm(forms.ModelForm):
    class Meta:
        model = Encaissement_Journalier
        fields = ('Num_piece','libelle','montant','date')
        widgets = {
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d')
        }
    def __init__(self, *args, **kwargs):
        super(UpdatDecaissement_JournalierForm, self).__init__(*args, **kwargs)
    def clean_date(self):
        date = self.cleaned_data['date']
        formatted_date = date.strftime('%Y-%m-%d')
        return formatted_date

class Encaissement_JournalierForm(forms.ModelForm):
    date = forms.DateField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Encaissement_Journalier
        fields = ('Num_piece','libelle','montant','date')
        widgets = {
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
        }
        
class UpdatEncaissement_JournalierForm(forms.ModelForm):
    class Meta:
        model = Encaissement_Journalier
        fields = ('Num_piece','libelle','montant','date')
        widgets = {
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d')
        }
    def __init__(self, *args, **kwargs):
        super(UpdatEncaissement_JournalierForm, self).__init__(*args, **kwargs)
    def clean_date(self):
        date = self.cleaned_data['date']
        formatted_date = date.strftime('%Y-%m-%d')
        return formatted_date
        
class RecetteForm(forms.ModelForm):
    date = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Recette
        fields = ('chauffeur','montant','cpte_comptable','Num_piece','numero_fact','date')
        widgets = {
            'chauffeur': forms.TextInput(attrs={'class':'form-control'}),
            'cpte_comptable': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'numero_fact': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
        }

class UpdateRecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ('chauffeur','montant','cpte_comptable','Num_piece','numero_fact','date')
        widgets = {
            'chauffeur': forms.TextInput(attrs={'class':'form-control'}),
            'cpte_comptable': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'numero_fact': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'date' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
    def __init__(self, *args, **kwargs):
        super(UpdateRecetteForm, self).__init__(*args, **kwargs)
    def clean_date(self):
        date = self.cleaned_data['date']
        formatted_date = date.strftime('%Y-%m-%d',)
        return formatted_date
                
class ChargeFixForm(forms.ModelForm):
    date = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = ChargeFixe
        fields = ('libelle','montant','cpte_comptable','Num_piece','Num_fact','date')
        widgets = {
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'cpte_comptable': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'Num_fact': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
        }

class UpdatChargeFixForm(forms.ModelForm):
    class Meta:
        model = ChargeFixe
        fields = ('libelle','montant','cpte_comptable','Num_piece','Num_fact','date')
        widgets = {
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'cpte_comptable': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'Num_fact': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'date' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
    def __init__(self, *args, **kwargs):
        super(UpdatChargeFixForm, self).__init__(*args, **kwargs)
    def clean_date(self):
        date = self.cleaned_data['date']
        formatted_date = date.strftime('%Y-%m-%d',)
        return formatted_date
        
class ChargeVarForm(forms.ModelForm):
    date = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = ChargeVariable
        fields = ('libelle','montant','cpte_comptable','Num_piece','Num_fact','date')
        widgets = {
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'cpte_comptable': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'Num_fact': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
        }
class updatChargeVarForm(forms.ModelForm):
    #date = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = ChargeVariable
        fields = ('libelle','montant','cpte_comptable','Num_piece','Num_fact','date')
        widgets = {
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'cpte_comptable': forms.TextInput(attrs={'class':'form-control'}),
            'Num_piece': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'Num_fact': forms.TextInput(attrs={'class':'form-control'}),
            'montant': forms.NumberInput(attrs={'class':'form-control'}),
            'date' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
    def __init__(self, *args, **kwargs):
        super(updatChargeVarForm, self).__init__(*args, **kwargs)
    def clean_date(self):
        date = self.cleaned_data['date']
        formatted_date = date.strftime('%Y-%m-%d',)
        return formatted_date
  
class VisiteTechniqueForm(forms.ModelForm):
    date_visite = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    date_prochaine_visite = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = VisiteTechnique
        fields = ('date_prochaine_visite','date_visite','cout','piece_jointe')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
        }
class UpdatVisiteTechniqueForm(forms.ModelForm):
    class Meta:
        model = VisiteTechnique
        fields = ('date_prochaine_visite','date_visite','cout','piece_jointe')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
            'date_visite' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'date_prochaine_visite' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        } 
    def __init__(self, *args, **kwargs):
        super(UpdatVisiteTechniqueForm, self).__init__(*args, **kwargs)
        self.fields["date_visite"].input_formats = ("%Y-%m-%d",)
        self.fields["date_prochaine_visite"].input_formats = ("%Y-%m-%d",)
        
class AssuranceForm(forms.ModelForm):
    date = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    date_proch_assur = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Assurance
        fields = ('date','date_proch_assur','cout','piece_jointe')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
        }

class UpdatAssuranceForm(forms.ModelForm):
    class Meta:
        model = Assurance
        fields = ('date','date_proch_assur','cout','piece_jointe')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
            'date' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'date_proch_assur' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
    def __init__(self, *args, **kwargs):
        super(UpdatAssuranceForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["date"].input_formats = ("%Y-%m-%d",)
        self.fields["date_proch_assur"].input_formats = ("%Y-%m-%d",) 
        
class EntretienForm(forms.ModelForm):
    date_Entretien = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    date_proch_Entretien = forms.DateTimeField(widget= forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control','placeholder':'Selection une date...', 'format':'yyyy-mm-dd', 'type':'date'}))
    class Meta:
        model = Entretien
        fields = ('cout','date_Entretien','date_proch_Entretien','piece_jointe')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
        }


class UpdatEntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        fields = ('cout','date_Entretien','date_proch_Entretien','piece_jointe')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
            'date_proch_Entretien' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'date_Entretien' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
        
    def __init__(self, *args, **kwargs):
        super(UpdatEntretienForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["date_Entretien"].input_formats = ("%Y-%m-%d",)
        self.fields["date_proch_Entretien"].input_formats = ("%Y-%m-%d",) 
        
        
class ReparationForm(forms.ModelForm):
    class Meta:
        model = Reparation
        fields = ('date_entree','date_sortie','num_fich_repat','identification','description','cout','piece_jointe')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
            'num_fich_repat': forms.NumberInput(attrs={'class':'form-control'}),
            'identification': forms.Textarea(attrs={'class':'form-control','rows':'3'},),
            'description': forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'date_entree' :DateInput(attrs={"type": "datetime-local","class":"form-control"}, format="%Y-%m-%dT%H:%M",),
            'date_sortie' :DateInput(attrs={"type": "datetime-local","class":"form-control"}, format="%Y-%m-%dT%H:%M",),
        } 
    def __init__(self, *args, **kwargs):
        super(ReparationForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["date_entree"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["date_sortie"].input_formats = ("%Y-%m-%dT%H:%M",)   


class UpdatReparationForm(forms.ModelForm):
    class Meta:
        model = Reparation
        fields = ('date_entree','date_sortie','num_fich_repat','identification','description','cout','piece_jointe')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
            'num_fich_repat': forms.NumberInput(attrs={'class':'form-control'}),
            'identification': forms.Textarea(attrs={'class':'form-control','rows':'3'},),
            'description': forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'date_entree' :DateInput(attrs={"type": "datetime-local","class":"form-control"}, format="%Y-%m-%dT%H:%M",),
            'date_sortie' :DateInput(attrs={"type": "datetime-local","class":"form-control"}, format="%Y-%m-%dT%H:%M",),
        } 
    def __init__(self, *args, **kwargs):
        super(UpdatReparationForm, self).__init__(*args, **kwargs)
        self.fields["date_entree"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["date_sortie"].input_formats = ("%Y-%m-%dT%H:%M",)   


class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ('libelle','cout','date_achat')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'date_achat' :DateInput(attrs={"type": "datetime-local","class":"form-control"}, format="%Y-%m-%dT%H:%M",),
        }
    def __init__(self, *args, **kwargs):
        super(PieceForm, self).__init__(*args, **kwargs)
        self.fields["date_achat"].input_formats = ("%Y-%m-%dT%H:%M",)
        
        
class UpdatPieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ('libelle','cout','date_achat')
        widgets = {
            'cout': forms.NumberInput(attrs={'class':'form-control'}),
            'libelle': forms.TextInput(attrs={'class':'form-control'}),
            'date_achat' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
    def __init__(self, *args, **kwargs):
        super(UpdatPieceForm, self).__init__(*args, **kwargs)
        self.fields["date_achat"].input_formats = ("%Y-%m-%d",)

