from django.contrib import admin
from .models import  Vendeur, CartOrder, CartOrderItem, Produit, ProductReview, ProduitImage, CategoProd, ListeSouhaite, Addresse

# Register your models here.

class ProduitImageAdmin(admin.TabularInline):
    model = (ProduitImage)
class ProduitAdmin(admin.ModelAdmin):
    inlines = [ProduitImageAdmin]
    list_display =['user', 'Libelle', 'prix', 'sku', 'date']


    
class VendeurAdmin(admin.ModelAdmin):
    list_display = ['user','nom', 'address', 'Contact', 'period_garentie']

class ListeSouhaiteAdmin(admin.ModelAdmin):
    list_display =['user', 'produit', 'date']

class CategoProdAdmin(admin.ModelAdmin):
    list_display =['libelle', 'image']

class CartOrderAdmin(admin.ModelAdmin):
    list_display =['user', 'prix', 'stautus_paiement', 'date_commande', 'status_prod']

class CartOrderItemAdmin(admin.ModelAdmin):
    list_display =['commande','facture_no', 'status_prod', 'article', 'qte', 'prix', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display =['user', 'produit', 'revue', 'classement', 'date']

class AddresseAdmin(admin.ModelAdmin):
    list_display =['user', 'addresse', 'status']


admin.site.register(CategoProd, CategoProdAdmin)
admin.site.register(Produit, ProduitAdmin)

admin.site.register(ListeSouhaite, ListeSouhaiteAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Vendeur, VendeurAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(Addresse, AddresseAdmin)
admin.site.register(ProduitImage)



