from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe 
from django.utils import timezone
#from userauths.models import User


#-------------------------categorie de vehicule-----------------------------#
class CategoVehi(models.Model):
    cid = ShortUUIDField(unique=True, max_length=30, prefix='catveh', alphabet="abcdefgh12345")
    category = models.CharField(unique=True, max_length=10)
    image = models.ImageField(upload_to="category_vehi", default="catego_prod.jpg")
    date_saisie = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Categorys Vehicules"
    def category_image(self) :
        # sourcery skip: replace-interpolation-with-fstring
        return mark_safe('<img src="%s"  width="50" height="50">' %(self.image.url))
    
    def __str__(self):
        return self.category

class Vehicule(models.Model):
    immatriculation = models.CharField(unique=True, max_length=15)
    marque = models.CharField(max_length=20)
    duree= models.IntegerField(default=0)
    image = models.ImageField(upload_to="vehicule")
    photo_carte_grise = models.ImageField(upload_to="Photo_Carte_Grise")
    num_cart_grise = models.CharField(max_length=100, unique=True)
    num_Chassis = models.CharField(max_length=100, unique=True)
    date_acquisition = models.DateField()
    cout_acquisition = models.IntegerField(default=0)
    dat_edit_carte_grise = models.DateField()
    date_mis_service = models.DateField()
    category = models.ForeignKey(CategoVehi, on_delete=models.CASCADE, related_name="catego_vehicule")
    date_saisie = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return self.immatriculation
    @property
    def age(self):  # sourcery skip: inline-immediately-returned-variable
        import datetime
        date_nai = self.date_mis_service
        tday = datetime.date.today() 
        age = (tday.year - date_nai.year) - int((date_nai.month,tday.day ) < (date_nai.month, tday.day))
        return age

class TempsArret(models.Model):
    REPARATION = 'Reparation'
    VISITE = 'Visite'
    ACCIDENT = 'Accident'
    ENTRETIEN = 'Entretien'
    AUTRE = 'Autre'
    
    MOTIFS = [
        ('Reparation', 'Réparation'),
        ('Visite', 'Visite'),
        ('Accident', 'Accident'),
        ('Entretien', 'Entretien'),
        ('Autre', 'Autre'),
    ]
    recet = models.IntegerField(default=0)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name='temps_arrets')
    motif = models.CharField(max_length=20, choices=MOTIFS)
    motif_autre = models.CharField(max_length=255, blank=True, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    date_saisie = models.DateTimeField(auto_now_add=True)

class Typecontravention(models.Model):
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom

class Contravention(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    type_contravention = models.ForeignKey(Typecontravention, on_delete=models.CASCADE)
    montant = models.IntegerField(default=0)
    
class Prevision(models.Model):
    mois = models.DateField()
    montant_previs= models.IntegerField(default=0)
    def __str__(self):
        return '%s - %s' % (self.mois, self.montant_previs)
    def calculer_difference(self):
        recettes_du_mois = Recette.objects.filter(date__year=self.mois.year, date__month=self.mois.month)
        somme_recettes_du_mois = recettes_du_mois.aggregate(models.Sum('montant'))['montant__sum'] or 0
        difference = self.montant_previs - somme_recettes_du_mois
        return somme_recettes_du_mois, difference

class Billetage(models.Model):
    valeur = models.IntegerField(choices=[(10000, '10000'),  
                                          (5000, '5000'),     
                                          (2000, '2000'),    
                                          (1000, '1000'),    
                                          (500, '500'),      
                                          (200, '200'),
                                          (100, '100'), 
                                          (50, '50'), 
                                          (25, '25'),
                                          (10, '10'),           
                                          (5, '5')])        
    nombre = models.IntegerField()
    type_valeur = models.CharField(max_length=10, choices=[('Billet', 'Billet'), ('Piece', 'Piece')])
    date_saisie = models.DateField(auto_now_add=True)
    def calculer_produit(self):
        return self.valeur * self.nombre

class SoldeJour(models.Model):
    date = models.DateField(unique=True)
    montant = models.IntegerField(default=0)
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.date_saisie, self.montant)
    
class Encaissement_Journalier(models.Model):
    Num_piece = models.CharField(max_length=100)
    libelle = models.CharField(max_length=100)
    montant = models.IntegerField(default=0)
    date = models.DateField()
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):  # sourcery skip: replace-interpolation-with-fstring
        return '%s - %s' % (self.libelle, self.montant)

class Decaissement_Journalier(models.Model):
    Num_piece = models.CharField(max_length=100)
    libelle = models.CharField(max_length=200)
    date = models.DateField()
    montant = models.IntegerField(default=0)
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):  # sourcery skip: replace-interpolation-with-fstring
        return '%s - %s' % (self.libelle, self.montant)

class Relicat(models.Model):
    chauffeur = models.CharField(max_length=50)
    vehicule = models.ForeignKey(Vehicule, related_name="relicat", on_delete=models.CASCADE)
    montant = models.IntegerField(default=0)
    date = models.DateField()
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):  # sourcery skip: replace-interpolation-with-fstring
        return '%s - %s' % (self.vehicule.immatriculation, self.montant)
    
class Vignette(models.Model):
    vehicule = models.ForeignKey(Vehicule, related_name="vignettes", on_delete=models.CASCADE)
    montant = models.IntegerField(default=0)
    piece_jointe = models.ImageField(upload_to="vignettes_fil", blank=True)
    date = models.DateField()
    date_prochain_paiement = models.DateField()
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):  # sourcery skip: replace-interpolation-with-fstring
         return '%s - %s' % (self.vehicule.immatriculation, self.montant)
    @property
    def jours_vign_restant(self):
        jours_vign_restant = (self.date_prochain_paiement - timezone.now().date()).days
        return jours_vign_restant
    
class Patente(models.Model):
    vehicule = models.ForeignKey(Vehicule, related_name="patantes", on_delete=models.CASCADE)
    montant = models.IntegerField(default=0)
    piece_jointe = models.ImageField(upload_to="patentes_fil", blank=True)
    date = models.DateField()
    date_prochain_paiement = models.DateField()
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):  # sourcery skip: replace-interpolation-with-fstring
         return '%s - %s' % (self.vehicule.immatriculation, self.montant)
    @property
    def jours_pate_restant(self):
        jours_pate_restant = (self.date_prochain_paiement - timezone.now().date()).days
        return jours_pate_restant
    
class Cart_Stationnement(models.Model):
    vehicule = models.ForeignKey(Vehicule, related_name="cart_station", on_delete=models.CASCADE)
    montant = models.IntegerField(default=0)
    piece_jointe = models.ImageField(upload_to="carte_station_fil", blank=True)
    date = models.DateField()
    date_prochain_paiement = models.DateField()
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):  
        return '%s - %s' % (self.vehicule.immatriculation, self.montant)
    @property
    def jours_cartsta_restant(self):
        jours_cartsta_restant = (self.date_prochain_paiement - timezone.now().date()).days
        return jours_cartsta_restant
    
class Recette(models.Model):
    chauffeur = models.CharField(max_length=50)
    cpte_comptable = models.CharField(max_length=100)
    numero_fact = models.CharField(max_length=20)
    Num_piece = models.CharField(max_length=100)
    vehicule = models.ForeignKey(Vehicule, related_name="recettes", on_delete=models.CASCADE)
    montant = models.IntegerField(default=0)
    date = models.DateField()
    date_saisie = models.DateTimeField(auto_now_add=True)
    def __str__(self): 
        return '%s ' % (self.vehicule.immatriculation)

class ChargeFixe(models.Model):
    libelle = models.CharField(max_length=100, null=True, blank=True)
    vehicule = models.ForeignKey(Vehicule, related_name="chargefixes", on_delete=models.CASCADE)
    montant = models.IntegerField(default=0.0)
    cpte_comptable = models.CharField(max_length=100)
    Num_piece = models.CharField(max_length=100)
    Num_fact = models.CharField(max_length=100)
    date_saisie = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    def __str__(self) : 
        return '%s ' % (self.vehicule.immatriculation)
    
class ChargeVariable(models.Model):
    libelle = models.CharField(max_length=100, null=True, blank=True)
    vehicule = models.ForeignKey(Vehicule, related_name="chargevariables", on_delete=models.CASCADE)
    montant = models.IntegerField(default=0.0)
    cpte_comptable = models.CharField(max_length=100)
    Num_piece = models.CharField(max_length=100)
    Num_fact = models.CharField(max_length=100)
    date = models.DateField()
    date_saisie = models.DateTimeField(auto_now_add=True)
    def __str__(self) : 
        return '%s ' % (self.vehicule.immatriculation)
    
class ChargeAdminis(models.Model):
    libelle = models.CharField(max_length=100)
    montant = models.IntegerField(default=0.0)
    cpte_comptable = models.CharField(max_length=100)
    Num_piece = models.CharField(max_length=100)
    Num_fact = models.CharField(max_length=100)
    date = models.DateField()
    date_saisie = models.DateTimeField(auto_now_add=True)
    def __str__(self) : 
        return '%s ' % (self.libelle)

class Reparation(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="reparations")
    date_entree = models.DateTimeField()
    date_sortie = models.DateTimeField()
    piece_jointe = models.ImageField(upload_to="reparation_fil", blank=True)
    num_fich_repat = models.IntegerField()
    identification = models.TextField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    cout = models.IntegerField(default=0.0)
    date_saisie = models.DateField(auto_now_add=True)
    def __str__(self):
        return '%s ' % (self.vehicule.immatriculation)

class Piece(models.Model):
    reparation = models.ForeignKey(Reparation, on_delete=models.CASCADE, related_name="pieces")
    libelle = models.CharField(max_length=30, null=True, blank=True)
    cout = models.IntegerField(default=0)
    date_achat = models.DateTimeField()
    date_saisie =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s ' % (self.libelle)

class VisiteTechnique(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="visites")
    date_visite= models.DateField()
    piece_jointe = models.ImageField(upload_to="visites_fil", blank=True)
    date_prochaine_visite= models.DateField()
    cout = models.IntegerField(default=0.0)
    date_saisie = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.vehicule.immatriculation
    @property
    def jour_restant(self):
        jours_restant = (self.date_prochaine_visite - timezone.now().date()).days
        return jours_restant
    
class Entretien(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="entretiens")
    piece_jointe = models.ImageField(upload_to="entretiens_fil", blank=True)
    date_Entretien = models.DateField()
    date_proch_Entretien = models.DateField()
    cout = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    date_saisie = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.vehicule.immatriculation
    @property
    def jours_ent_restant(self):
        jours_ent_restant = (self.date_proch_Entretien - timezone.now().date()).days
        return jours_ent_restant

class Assurance(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="assurances")
    piece_jointe = models.ImageField(upload_to="assurances_fil", blank=True)
    date= models.DateField()
    date_proch_assur= models.DateField()
    cout = models.IntegerField(default=0.0)
    date_saisie = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.vehicule.immatriculation
    @property
    def jours_assu_restant(self):
        jours_assu_restant = (self.date_proch_assur - timezone.now().date()).days
        return jours_assu_restant
