from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe 
from userauths.models import User


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Vendeur(models.Model):
    vid = ShortUUIDField(unique=True, max_length=30, prefix='ven', alphabet="abcdefgh12345")
    
    nom= models.CharField(max_length=10, default='Produit')
    image = models.ImageField(upload_to=user_directory_path, default="vendeur.jpg")
    description = models.TextField(null=True, blank=True, default="Le meilleur")
    address = models.CharField(max_length=50, default=" 225 Rue principale")
    Contact = models.CharField(max_length=50, default=" +225 00 00 00 00 00")
    achat_a_temps = models.CharField(max_length=50, default="100")
    jour_de_retour = models.CharField(max_length=50, default="100")
    period_garentie = models.CharField(max_length=50, default="100")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "Vendeurs"
        
    def vendor_image(self) :
        return mark_safe('<img src="%s"  width="50" height="50">' %(self.image.url))
    
    def __str__(self):
        return self.nom
    
class Tags(models.Model):
    pass


STATUS_CHOICE = (
    ("traiter", "Traitement"),
    ("expedier", "Expedier"),
    ("livrer", "Livrer"),
)
 
STATUS= (
    ("projet", "Projet"),
    ("desactiver", "Desactiver"),
    ("rejeter", "Rejeter"),
    ("en_revision", "En_revision"),
    ("publier", "Publier"),
)
CLASSEMENT = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)
 
#------categorie des Prod
class CategoProd(models.Model):
    cid = ShortUUIDField(unique=True, max_length=30, prefix='cat', alphabet="abcdefgh12345")
    libelle = models.CharField(max_length=30, default="mecano")
    image = models.ImageField(upload_to="category_prod", default="catego_prod.jpg")
    class Meta:
        verbose_name_plural = "Categories Produits"
        
    def category_image(self) :
        return mark_safe('<img src="%s"  width="50" height="50">' %(self.image.url))
    
    def __str__(self):
        return self.libelle
    
class Produit(models.Model):
    pid = ShortUUIDField(unique=True, max_length=30, prefix='ven', alphabet="abcdefgh12345")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(CategoProd, on_delete=models.SET_NULL, null=True)
    
    Libelle = models.CharField(max_length=10, default='Produit')
    image = models.ImageField(upload_to=user_directory_path, default="produit.jpg")
    description = models.TextField(null=True, blank=True, default="La qualité produit")
    prix = models.DecimalField(max_digits=999, decimal_places=2, default="0.0")
    ancien_prix =models.DecimalField(max_digits=999, decimal_places=2, default="0.0")
    
    Specification = models.TextField(null=True, blank=True)
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    
    status_prod = models.CharField(choices=STATUS, max_length=50, default="En revision")
    status = models.BooleanField(default=True)
    en_stock = models.BooleanField(default=True)
    en_vedette = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, max_length=10, prefix='sku', alphabet="1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    mis_a_jour = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Produits"
        
    def poduct_image(self) :
        return mark_safe('<img src="%s"  width="50" height="50">' %(self.image.url))
    
    def __str__(self):
        return self.nom, self.prix

    def get_pourcentage(self):
        nouv_prix = (self.prix / self.ancien_prix)*100
        return nouv_prix

class ProduitImage(models.Model):
    image = models.ImageField(upload_to="product_img", default="product.jpg")
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Image Produit"
    
############# Panier(cart), commande(Order), articlecommander(OrderItem) et l'addresse
############# Panier(cart), commande(Order), articlecommander(OrderItem) et l'addresse
############# Panier(cart), commande(Order), articlecommander(OrderItem) et l'addresse

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prix =models.DecimalField(max_digits=10, decimal_places=2, default="0.0")
    stautus_paiement = models.BooleanField(default=False)
    date_commande = models.DateTimeField(auto_now_add=True)
    status_prod = models.CharField(choices=STATUS_CHOICE, max_length=30, default="Traitement")
    
    class Meta:
        #verbose_name_plural = "Carts Order"
        verbose_name_plural = "Panier des Commandes"


#order(commande), item(article)
class CartOrderItem(models.Model):
    commande = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    status_prod = models.CharField(max_length=30)
    facture_no = models.CharField(max_length=100)
    article = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    qte = models.IntegerField(default=0)
    prix =models.DecimalField(max_digits=10, decimal_places=2, default="0.0")
    total =models.DecimalField(max_digits=10, decimal_places=2, default="0.0")
    class Meta:
        #verbose_name_plural = "Cart Order Items"
        verbose_name_plural = "Panier article commandé "
    
    def order_img(self) :
        return mark_safe('<img src="/media/%s"  width="50" height="50">' %(self.image)) 
            
########################################### Produict Revu, Liste Souhaite(whishlist), Addresse ##########################################
#rating

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    revue = models.TextField()
    classement = models.IntegerField(choices=CLASSEMENT, default=None)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Produits Revus"
    def __str__(self) :
        return self.produit.nom
    
    def get_rating(self):
        return self.classement

###--------------------whislist(listeSouhaite)
class ListeSouhaite(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Liste Souhaite"
    def __str__(self) :
        return self.produit.nom

class Addresse(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    addresse = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Addresses"








