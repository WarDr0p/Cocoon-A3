from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Order, Produits
def Valider_Commande(modeladmin, request, queryset):
    for order in queryset:
        order.validate()
Valider_Commande.short_description = "Valider les commandes sélectionnées"

def Valider_Livraison(modeladmin, request, queryset):
    for order in queryset:
        order.fulfill()
Valider_Livraison.short_description = "Valider la livraison des commandes sélectionnées"


@admin.register(Order)
class AccountAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'created_at',
    )
    list_display = (
        'id',
        'user',
        'created_at',
        'isValidated',
        'isFulfilled',
        'Produits_commande'
    )
    readonly_fields = (
        'id',
        'user',
        'created_at',

    )
    list_select_related = (
        'user',
    )
    actions = [Valider_Commande, Valider_Livraison]



@admin.register(Produits)
class Adminproduits(admin.ModelAdmin):
    date_heirarchy = (
            'id',
        )
    list_display = (
            'id',
            'name',
            'unite',
            'stock',
        )
    readonly_fields = (
            'id',
            'unite',
        )
    list_select_related = (

        )

    actions = ['make_published']


    #def account_actions(self, obj):
# TODO: Render action buttons

# Register your models here.
