from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from home.models import Cart, CartItem, Order, OrderItem, Profile, Produits, Personne,Allergie
from django.shortcuts import render, redirect
from home.forms import SignUpForm, ProductForm, SignIn, FormOccupant, AlergiesForm
from django.contrib.auth import authenticate,logout as dj_logout, login as dj_login
from django.utils import timezone
from django.shortcuts import render
from plotly.offline import plot
import plotly.express as px
from datetime import timedelta




def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render({}, request))

def member(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = FormOccupant(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data.get('pre')
                last_name = form.cleaned_data.get('nom')
                member = Personne.objects.create(first_name=first_name, last_name=last_name, parent=request.user)
                member.save()
                template = loader.get_template('home/memberchoice.html')
                return HttpResponse(template.render({"valid": "Votre nouvel occupant a bien été ajouté"}, request))

        else:
            form = FormOccupant()
            template = loader.get_template('home/member.html')
            return HttpResponse(template.render({"form":form}, request))
    else:
        template = loader.get_template('home/loginchoice.html')
        return HttpResponse(template.render({"error": "Veuillez vous connecter pour acceder à cette page"}, request))

def allergie(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AlergiesForm(request.POST)
            if form.is_valid():
                allergie = form.cleaned_data.get('pro')
                all = Allergie.objects.create(porteur=request.user, allergie=allergie)
                all.save()
                template = loader.get_template('home/allergiechoice.html')
                return HttpResponse(template.render({"valid": "Votre allergie a bien été enregistrée"}, request))
        else:
            form = AlergiesForm()
            template = loader.get_template('home/allergie.html')
            return HttpResponse(template.render({"form":form}, request))
    else:
        template = loader.get_template('home/loginchoice.html')
        return HttpResponse(template.render({"error": "Veuillez vous connecter pour acceder à cette page"}, request))




def memberchoice(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/memberchoice.html')
        return HttpResponse(template.render({"name": request.user.first_name}, request))
    else:
        template = loader.get_template('home/loginchoice.html')
        return HttpResponse(template.render({"error": "Veuillez vous connecter pour acceder à cette page"}, request))


def loginchoice(request):
    if request.user.is_authenticated:
            user = request.user
            profil = user.profile
            fields = ['Pseudo', 'E-mail', 'Prenom', 'Nom', 'Mobile', 'Fixe', "Adresse", 'Complément', 'Ville', 'Code postal']
            vals = [user.username, user.email, user.first_name, user.last_name, profil.Mobile, profil.Fixe, profil.Adress1, profil.Adress2, profil.Ville, profil.Cp]
            contexte = {"champs": fields, "valeurs": vals}
            membres = []
            allergies = []
            for membre in Personne.objects.all():
                if membre.parent == request.user:
                    membres.append([membre.first_name,membre.last_name])
            if len(membres)>0:
                contexte.update({"membres":membres})
            else:
                contexte.update({"membreserror":"Vous n'avez enregistré personne dans votre famille"})
            for allergie in Allergie.objects.all():
                if(allergie.porteur == request.user):
                    allergies.append(allergie.allergie)
            if len(allergies)>0:
                contexte.update({"allergies":allergies})
            else:
                contexte.update({"allergieserror":"Vous n'avez enregistré aucune allergie"})

            template = loader.get_template("home/account.html")
            return HttpResponse(template.render(contexte, request))

    template = loader.get_template('home/loginchoice.html')
    return HttpResponse(template.render({}, request))

def register(request):
    template = loader.get_template('home/register.html')
    return HttpResponse(template.render({}, request))

def login(request):
    if request.method == 'POST':
        form = SignIn(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('pseudo'), password=form.cleaned_data.get('passw'));
            if user is not None:
                dj_login(request, user)
                redirect("home/loginchoice")
            else:
                form = SignIn()
                template = loader.get_template('home/login.html')
                return HttpResponse(template.render({"form": form, "error": "Erreur dans le couple mot de passe utilisateur"}, request))
            return loginchoice(request)
    else:
        form = SignIn()
        template = loader.get_template('home/login.html')
        return HttpResponse(template.render({"form": form}, request))

def produits(request):
    template = loader.get_template('home/.html')
    return HttpResponse(template.render({}, request))

def rayon(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/rayon.html')
        return HttpResponse(template.render({"name": request.user.first_name}, request))
    else:
        template = loader.get_template('home/loginchoice.html')
        return HttpResponse(template.render({"error":"Veuillez vous connecter pour acceder à cette page"}, request))

def actualrayon(request, category):
    productlist = Produits.objects.all()
    desiredProducts = []
    for prod in productlist:
        if prod.categorie == category:
            desiredProducts.append(prod)
    desiredProductsFinal = []
    temp = []
    i=0
    for prod in desiredProducts:
        i+=1
        temp.append(prod)
        if i ==6:
            i=0
            desiredProductsFinal.append(temp)
            temp = []
    desiredProductsFinal.append(temp)
    template = loader.get_template('home/actualrayon.html')
    return HttpResponse(template.render({"prod": desiredProductsFinal}, request))

def alimentation(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/alimentation.html')
        return HttpResponse(template.render({"name": request.user.first_name}, request))
    else:
        template = loader.get_template('home/loginchoice.html')
        return HttpResponse(template.render({"error": "Veuillez vous connecter pour acceder à cette page"}, request))

def prod(request,id):
    if request.user.is_authenticated:
        prod = Produits.objects.get(id=id)
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                carts = Cart.objects.all()
                usercart = 0
                for cart in carts:
                    if request.user == cart.user:
                        usercart = cart
                if usercart ==0:
                    usercart = Cart(user=request.user, created_at=timezone.now())
                    usercart.save()
                item = CartItem(product=prod, quantity=form.cleaned_data.get('quantity'), cart=usercart, price=prod.prix*int(form.cleaned_data.get('quantity')))
                item.save()
                return redirect('../produits/'+str(prod.categorie))
            template = loader.get_template('home/produit.html')
        else:
            form = ProductForm()
            template = loader.get_template('home/produit.html')
        return HttpResponse(template.render({"prod": prod, "form": form}, request))
    else:
        template = loader.get_template('home/loginchoice.html')
        return HttpResponse(template.render({"error": "Veuillez vous connecter pour acceder à cette page"}, request))

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            user.profile.Adress1 = form.cleaned_data.get('address1')
            user.profile.Adress2 = form.cleaned_data.get('address2')
            user.profile.Cp = form.cleaned_data.get('zipcode')
            user.profile.Mobile = form.cleaned_data.get('mobile')
            user.profile.Fixe = form.cleaned_data.get('fixe')
            user.profile.Ville = form.cleaned_data.get('city')
            user.profile.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=user.username, password=raw_password)
            dj_login(request, user)
            return redirect('../member')
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form})

@login_required
def logout(request):
    dj_logout(request)


@login_required
def validate(request):
    usercart = 0
    for panier in Cart.objects.all():
        if panier.user == request.user:
            usercart = panier
    if usercart != 0:
        itemlist = []
        for item in CartItem.objects.all():
            if item.cart == usercart:
                itemlist.append(item)
        if len(itemlist)>0:
            order = Order(user=request.user)
            order.save()

            for item in itemlist:
                oit = OrderItem(quantity=item.quantity, product=item.product, order=order, price=item.price)
                oit.save()
        usercart.delete()
    return redirect("../commandes")

def commande(request):
    if request.user.is_authenticated:
        orderList = []
        context = {}
        for com in Order.objects.all():
            if com.user == request.user:
                orderList.append([com,getProds(com)])
        if len(orderList) == 0:
            context = {"error":"Vous n'avez jamais passé de commande"}
        else:
            context ={"commandes": orderList}
        template = loader.get_template('home/commandes.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('home/loginchoice.html')
        return HttpResponse(template.render({"error": "Veuillez vous connecter pour acceder à cette page"}, request))

def getProds(order):
    result = []
    for item in OrderItem.objects.all():
        if item.order == order:
            result.append(item)
    return result

def cart(request):
    if request.user.is_authenticated:
        carts = Cart.objects.all()
        usercart = 0
        produit = []
        for cart in carts:
            if cart.user == request.user:
                usercart = cart
        if usercart == 0:
            error = "Votre panier semble vide"
            template = loader.get_template('home/cart.html')
            return HttpResponse(template.render({"error": error}, request))
        else:
            for prod in CartItem.objects.all():
                if prod.cart == usercart:
                    produit.append([prod.product,prod.quantity,prod.price])
        template = loader.get_template('home/cart.html')
        return HttpResponse(template.render({"produit": produit}, request))
    else:
        template = loader.get_template('home/loginchoice.html')
        return HttpResponse(template.render({"error": "Veuillez vous connecter pour acceder à cette page"}, request))

def dataviz(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            quantiProd = {}
            stockProd = {}
            commandes = {}
            for prod in Produits.objects.all():
                quantiProd[prod.name]=0
                stockProd[prod.name]=prod.stock
            minDate = timezone.now().date()
            for order in Order.objects.all():
                if minDate>order.created_at.date():
                    minDate = order.created_at.date()
            while minDate <= timezone.now().date():
                commandes[str(minDate.year)+"-"+str(minDate.month)+"-"+str(minDate.day)]=0
                minDate=minDate+timedelta(days=1)
            for order in Order.objects.all():
                commandes[str(order.created_at.year)+"-"+str(order.created_at.month)+"-"+str(order.created_at.day)]+=1
            for item in OrderItem.objects.all():
                quantiProd[item.product.name] += item.quantity
            x = list(quantiProd.keys())
            y = list(quantiProd.values())
            y2 = list(stockProd.values())
            fig = px.bar(x=x, y=y,title="Total commande produits",labels={"x":"Produits", "y":"Quantité commandée"})
            fig2 = px.bar(x=x, y=y2, title="Stocks Produit", labels={"x":"Produits", "y":"Quantité en stock"})
            fig3 = px.line(x=list(commandes.keys()),title="Nombre de commande en fonction du temps", y=list(commandes.values()),labels={"x":"Date", "y":"Nombre de commandes"})

            plot_div3=plot(fig3,output_type='div')
            plot_div2 = plot(fig2, output_type='div')
            plot_div = plot(fig, output_type='div')
            template = loader.get_template('home/dataviz.html')
            return HttpResponse(template.render({'plot_div': plot_div, 'plot_div2': plot_div2, 'plot_div3': plot_div3}, request))
