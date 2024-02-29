from django.contrib import admin
from .models import *

class ChargeAdminisAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'cpte_comptable', 'Num_piece', 'Num_fact', 'montant','date',]
    list_filter = ['libelle']

class TempsArretAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'recet', 'date_debut', 'date_fin', 'motif','date_saisie']
    list_filter = ['vehicule','motif']

class AssuranceAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'date', 'date_proch_assur', 'cout', 'date_saisie']
    list_filter = ['vehicule']

class ReparationAdmin(admin.ModelAdmin):
    list_display = ['vehicule','date_entree','date_sortie','identification','num_fich_repat','cout','date_saisie']
    list_filter = ['vehicule']

class PieceAdmin(admin.ModelAdmin):
    list_display = ['reparation','libelle','cout','date_achat','date_saisie']
    list_filter = ['libelle']
 
    
class VisiteTechniqueAdmin(admin.ModelAdmin):
    list_display = ['vehicule','date_visite','cout','date_saisie']
    list_filter = ['vehicule',"cout"]
  
class EntretienAdmin(admin.ModelAdmin):
    list_display = ['vehicule','date_Entretien','date_proch_Entretien', 'cout','date_saisie']
    list_filter = ['vehicule',"cout"]
     
class RecetteAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'montant', 'cpte_comptable','Num_piece','chauffeur','date', 'date_saisie']
    list_filter = ['vehicule',"montant"]
    
class PrevisionAdmin(admin.ModelAdmin):
    list_display = ['mois', 'montant_previs']
    list_filter =  ['mois', 'montant_previs']
      
class ContraventionAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'montant', 'type_contravention']
    list_filter = ['vehicule',"montant", "type_contravention"]
       
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ['immatriculation', 'marque', 'category','cout_acquisition','photo_carte_grise' ,'date_mis_service','date_saisie']
    list_filter = ['immatriculation',"marque", "category"]

class CategoVehiAdmin(admin.ModelAdmin):
    list_display =['category', 'image']
    
class ChargeVariableAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'Num_piece','cpte_comptable','libelle','date', 'date_saisie','montant']
    list_filter = ['vehicule',"libelle", "cpte_comptable","date"]
       
class ChargeFixeAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'Num_piece','cpte_comptable','libelle','date','date_saisie' ,'montant']
    list_filter = ['vehicule',"libelle", "cpte_comptable","date"]

class RelicatAdmin(admin.ModelAdmin):
    list_display = ['vehicule','montant']
    list_filter = ['vehicule','date']
    
class VignetteAdmin(admin.ModelAdmin):
    list_display = ['vehicule','montant']
    list_filter = ['vehicule','date']
    
class PatenteAdmin(admin.ModelAdmin):
    list_display = ['vehicule','montant']
    list_filter = ['vehicule','date']
    
class CartStationAdmin(admin.ModelAdmin):
    list_display = ['vehicule','montant']
    list_filter = ['vehicule','date']
    
class Encaissement_JournalierAdmin(admin.ModelAdmin):
    list_display = ['libelle','montant']
    list_filter = ['libelle','date_saisie']

class Decaissement_JournalierAdmin(admin.ModelAdmin):
    list_display = ['libelle','montant']
    list_filter = ['libelle','date_saisie']

class BilletageAdmin(admin.ModelAdmin):
    list_display = ['valeur','nombre','type_valeur', 'date_saisie']
    list_filter = ['valeur','nombre',]

class SoldeJourAdmin(admin.ModelAdmin):
    list_display = ['montant', 'date', 'date_saisie']
    list_filter = ['montant','date',]


admin.site.register(SoldeJour, SoldeJourAdmin)
admin.site.register(Billetage, BilletageAdmin)
admin.site.register(Relicat, RelicatAdmin)
admin.site.register(Encaissement_Journalier, Encaissement_JournalierAdmin)
admin.site.register(Decaissement_Journalier, Decaissement_JournalierAdmin)
admin.site.register(Vignette, VignetteAdmin)
admin.site.register(Patente, PatenteAdmin)
admin.site.register(Cart_Stationnement, CartStationAdmin)
admin.site.register(Prevision, PrevisionAdmin)
admin.site.register(TempsArret, TempsArretAdmin)
admin.site.register(Vehicule, VehiculeAdmin)
admin.site.register(ChargeAdminis, ChargeAdminisAdmin)
admin.site.register(Piece, PieceAdmin)
admin.site.register(Recette, RecetteAdmin)
admin.site.register(Reparation,ReparationAdmin)
admin.site.register(VisiteTechnique, VisiteTechniqueAdmin)
admin.site.register(Entretien, EntretienAdmin)
admin.site.register(CategoVehi, CategoVehiAdmin)
admin.site.register(ChargeFixe, ChargeFixeAdmin)
admin.site.register(Assurance, AssuranceAdmin)
admin.site.register(Contravention, ContraventionAdmin)
admin.site.register(ChargeVariable, ChargeVariableAdmin)

 


