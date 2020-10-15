from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Produits(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    categorie = models.CharField(max_length=40)
    unite = models.CharField(max_length=40)
    prix = models.FloatField()
    stock = models.FloatField()

    def Categorie(self, cat):
        if self.categorie == cat:
            return True
        return False

    def __str__(self):
        return str(self.id)+ " : "+ self.name+ " : "+ self.categorie+ " : "+ str(self.prix)+ " : "+ str(self.stock)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Adress1 = models.TextField(max_length=500, blank=False)
    Adress2 = models.CharField(max_length=500, blank=True)
    Ville = models.CharField(max_length=50, blank=False)
    Cp = models.CharField(max_length=6, blank=False)
    Mobile = models.CharField(max_length=15, blank=False)
    Fixe = models.CharField(max_length=15, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.user.first_name) + " : " + str(self.created_at)

class CartItem(models.Model):
    product = models.ForeignKey(Produits, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.cart.id) + " : " + str(self.product.name) + " : " + str(self.quantity) + " : " + str(self.price)

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    isValidated = models.BooleanField(default=False)
    isFulfilled = models.BooleanField(default=False)

    def Produits_commande(self):
        items = []
        for item in OrderItem.objects.all():
            if item.order == self:
                items.append((item.product.name + " : " + str(item.quantity)+"\n"))
        return items
    def __str__(self):
        return str(self.user.first_name) + " : " + str(self.created_at)

    def fulfill(self):
        if self.isValidated:
            self.isFulfilled=True
            self.save()

    def validate(self):
        items = []
        for item in OrderItem.objects.all():
            if item.order == self:
                items.append(item)
        result = True
        for item in items:
            if item.quantity > item.product.stock:
                result = False
        if result:
            self.isValidated = True
            self.save()
            for item in items:
                produit = item.product
                produit.stock -= item.quantity
                produit.save()



class OrderItem(models.Model):
    product = models.ForeignKey(Produits, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return(str(self.order.id)+" : "+self.product.__str__())

class Personne(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

class Allergie(models.Model):
    porteur = models.ForeignKey(User, on_delete=models.CASCADE)
    allergie = models.CharField(max_length=50, blank=False)

# Create your models here.

