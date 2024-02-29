from django.urls import path
from . import views
from .views import *

urlpatterns = [
    
    path('dash', DashboardView.as_view(), name='dash'),
    path('dash_comptable/', DashbComptView.as_view(), name='journal_compta'),
    path('dash_garag', dashgaragView.as_view(), name='tb_garag'),
    path('suivi_financier', SuiviFinancierView.as_view(), name='suivi_finance'),
    path('journalgarag', JournalGaragView.as_view(), name='journal_garag'),
    path('addchargadminist', AddChargeAdminisView.as_view(), name='add_charg_administ'),
    
    path('Billetage', BilletageView.as_view(), name='saise_billetage'),
    
    path('adddecaissement', AddDecaissementView.as_view(), name='add_decaisse'),
    path('decaissement/<int:pk>/modifier', UpdatDecaissementView.as_view(), name='updat_decaisse'),
    path('decaissement/<int:pk>/supprimer', DeletDecaissementView.as_view(), name='delet_decaisse'),
    path('decaissement/<int:pk>/detail', DetailDecaissementView.as_view(), name='detail_decaisse'),
    
    path('addencaissement', AddEncaissementView.as_view(), name='addencaisse'),
    path('encaissement/<int:pk>/modifier', UpdatEncaissementView.as_view(), name='updat_encaisse'),
    path('encaissement/<int:pk>/supprimer', DeletEncaissementView.as_view(), name='delet_encaisse'),
    
    path('encaissement/<int:pk>/detail', DetailEncaissementView.as_view(), name='detail_encaisse'),
    path('decaissement/<int:pk>/detail', DetailDecaissementView.as_view(), name='detail_decaisse'),
    
    path('listencaissement', ListEncaissementView.as_view(), name='list_encaissement'),
    path('listdecaissement', ListDecaissementView.as_view(), name='list_decaissement'),
    
    path('bilanjournalier', BilanJournalierView.as_view(), name='bilan_journalier'),
    path('addsoldejour', AddSoldeJourView.as_view(), name='add_solde_jour'),
    
    #-------------------------------Categorie Véhicule & Véhicule--------------------------------- 
    path('add_veh', AddVehiculeView.as_view(), name='add_car'),
    path('listvehi', ListVehiculeView.as_view(), name='listvehi'),
    path('vehicule/<int:pk>/detail', DetailVehiculeView.as_view(), name='detavehi'),
    path('vehicule/<int:pk>/modifier', UpdatVehiculeView.as_view(), name='modifvehi'),
    path('vehicule/<int:pk>/supprimer', DeletVehiculeView.as_view(), name='supvehi'),
   
    #-------------------------------Categorie Véhicule--------------------------------------------- 
    path('addcategovehi', AddCategoriVehi.as_view(), name='add_catego_vehi'),
    path('vehicule/<cid>/', views.CategoVehiculeListView, name='catego_vehi_list'),
    
    path('p_404', views.Error_404, name='p404'),
    path('base', views.news, name='ba'),
    path('da', views.da, name='ba'),
    
    #-------------------------------Recette---------------------------------------------
    path('vehicule/<int:pk>/recette',AddRecetteView.as_view(), name="add_recet"),
    path('list_recet',ListRecetView.as_view(), name="listrecet"),
    path('recette/<int:pk>/modifier',UpdateRecetView.as_view(), name="updat_recet"),
    path('recette/<int:pk>/detail',DetailRecetteView.as_view(), name="detail_recet"),
    path('recette/<int:pk>/supprimer',DeletRecetteView.as_view(), name="del_recet"),
    #-------------------------------CHARGE---------------------------------------------
    path('vehicule/<int:pk>/acharg_fix',AddChargeFixView.as_view(), name="addcharg_fix"),
    path('acharg_fix/<int:pk>/modifier',UpdateChargFixView.as_view(), name="upd_charg_fix"),
    path('acharg_fix/<int:pk>/detail',DetailChargeFixeView.as_view(), name="detail_charg_fix"),
    path('acharg_fix/<int:pk>/supprimer',DeletChargFixView.as_view(), name="del_charg_fix"),
    
    path('vehicule/<int:pk>/charg_var',AddChargeVarView.as_view(), name="addcharg_var"),
    path('charg_var/<int:pk>/modifier',UpdateChargeVarView.as_view(), name="updat_charg_var"),
    path('charg_var/<int:pk>/detail',DetailChargeVarView.as_view(), name="detail_charg_var"),
    path('charg_var/<int:pk>/supprimer',DeletChargeVarView.as_view(), name="del_charg_var"),
    
    path('listcharfix',ListChargeFixView.as_view(), name="list_charg_fix"),
    path('listcharvar',ListChargeVarView.as_view(), name="list_charg_var"),
    
    #---------ENTRETIEN-------VISITE------REPARATION-------ASSURANCE-------PIECE-----VIGNETTE-----PATENTE--------#
    
    path('vehicule/<int:pk>/addvisite',AddVisitView.as_view(), name="add_visit"), 
    path('visite/<int:pk>/modifier',UpdateVisiteView.as_view(), name="updat_visit"), 
    path('visite/<int:pk>/detail',DetailVisiteView.as_view(), name="detail_visit"), 
    path('visite/<int:pk>/supprimer',DeletVisiteView.as_view(), name="delet_visit"), 
    path('vehicule/listvisite',ListVisitView.as_view(), name="list_visit"), 
    
    path('vehicule/<int:pk>/entretien',AddEntretienView.as_view(), name="add_entretien"),
    path('entretien/<int:pk>/modifier',UpdatEntretienView.as_view(), name="updat_entretien"),
    path('entretien/<int:pk>/detail',DetailEntretienView.as_view(), name="detail_entretien"),
    path('entretien/<int:pk>/supprimer',DeletEntretienView.as_view(), name="delet_entretien"),
    path('listentretien',ListEntretienView.as_view(), name="list_entretien"),
    
    path('vehicule/<int:pk>/reparation',AddReparationView.as_view(), name="add_reparat"),
    path('listrepa',ListReparationView.as_view(), name="list_repa"),
    path('reparation/<int:pk>/modifier',UpdateReparationView.as_view(), name="updat_repartion"),
    path('reparation/<int:pk>/supprimer',DeletReparationView.as_view(), name="delet_repartion"),
    path('reparation/<int:pk>/detail', DetailReparatView.as_view(), name="detail_reparat"),
    
    path('reparation/<int:pk>/piece',AddPieceView.as_view(), name="add_piece"),
    path('piece/<int:pk>/modifier',UpdatPieceView.as_view(), name="updat_piece"),
    path('piece/<int:pk>/detail',DetailPieceView.as_view(), name="detail_piece"),
    path('piece/<int:pk>/supprimer',DeletPieceView.as_view(), name="delet_piece"),
    path('listpiece', ListPieceView.as_view(), name="list_piece"),
    
    path('vehicule/<int:pk>/assurance',AddAssuranceView.as_view(), name="add_assur"),
    path('assurance/<int:pk>/modifier',UpdateAssuranceView.as_view(), name="updat_assurance"),
    path('assurance/<int:pk>/detail',DetailAssuranceView.as_view(), name="detail_assurance"),
    path('assurance/<int:pk>/supprimer',DeletAssuranceView.as_view(), name="delet_assurance"),
    path('listassur',ListAssuranceView.as_view(), name="list_assur"),

    path('temparret',TempArret.as_view(), name="temp_arret"),
    path('vehicule/<int:pk>/tempsarret',AddTempArretView.as_view(), name="add_temparret"),
    path('tempsarret/<int:pk>/modifier',UpdatTemp_arretView.as_view(), name="updat_temparret"),
    path('tempsarret/<int:pk>/detail',Detail_temp_arretView.as_view(), name="detail_temparret"),
    path('tempsarret/<int:pk>/supprimer',DeletTemp_arretView.as_view(), name="delet_temparret"),
    path('listemparret',ListTempArretView.as_view(), name="listemp_arret"),
    
    path('vehicule/<int:pk>/vignette',AddVignetteView.as_view(), name="add_vignet"),
    path('vignette/<int:pk>/modifier',UpdatVignetteView.as_view(), name="updat_vignet"),
    path('vignette/<int:pk>/detail',DetailVignetteView.as_view(), name="detail_vignet"),
    path('vignette/<int:pk>/supprimer',DeletVignetteView.as_view(), name="delet_vignet"),
    path('vignette/<int:pk>/detail',DetailCartStationView.as_view(), name="detail_vignet"),
    path('listvignette',ListVignetteView.as_view(), name="list_vignet"),
    
    path('vehicule/<int:pk>/cartestation',AddCartStationView.as_view(), name="add_cart_station"),
    path('cartestation/<int:pk>/modifier',UpdatCartStationView.as_view(), name="updat_cart_station"),
    path('cartestation/<int:pk>supprimer',DeletCartStationView.as_view(), name="delet_cart_station"),
    path('cartestation/<int:pk>detail',DetailCartStationView.as_view(), name="detail_cart_station"),
    path('listCartStation',ListCartStationView.as_view(), name="list_cart_station"),
    
    path('vehicule/<int:pk>/patente',AddPatenteView.as_view(), name="add_patente"),
    path('patente/<int:pk>/modifier', UpdatPatenteView.as_view(), name="updat_patente"),
    path('patente/<int:pk>/detail', DetailPatenteView.as_view(), name="detail_patente"),
    path('patente/<int:pk>/supprimer', DeletPatenteView.as_view(), name="delet_patente"),
    path('patente/<int:pk>/detail', DetailPatenteView.as_view(), name="detail_patente"),
    path('listpatente', ListPatenteView.as_view(), name="list_patente"),
    
]

