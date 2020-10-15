from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.Form):
    quantity = forms.CharField(label='Quantité', max_length=2, widget=forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3'}))


class SignIn(forms.Form):
    pseudo = forms.CharField(max_length=30, required=True,label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control col-md-12 mb-3'}))
    passw = forms.CharField(max_length=30, required=True,label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control col-md-12 mb-3'}))
    fields = ('pseudo', 'passw')

class AlergiesForm(forms.Form):
    pro = forms.CharField(label='Aliment', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3'}))
    fields = ('pro')

class FormOccupant(forms.Form):
    nom = forms.CharField(max_length=30, required=True,label="Prénom", widget=forms.TextInput(attrs={'class': 'form-control col-md-12 mb-3'}))
    pre = forms.CharField(max_length=30, required=True,label="Nom", widget=forms.TextInput(attrs={'class': 'form-control col-md-12 mb-3'}))
    fields = ('nom', 'pre')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,label='Prenom', required=True, widget=forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3'}))
    last_name = forms.CharField(max_length=30,label='Nom de famille', required=True, widget=forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3'}))
    email = forms.EmailField(max_length=254, label='E-Mail',required=True, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    mobile = forms.CharField(max_length=15, label='Mobile', required=True, widget=forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3'}))
    fixe = forms.CharField(max_length=30, label='Fixe', required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3'}))
    address2 = forms.CharField(max_length=300, label="Complément d'adresse", required=False, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    address1 = forms.CharField(max_length=300, label="Adresse", required=True, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    city = forms.CharField(max_length=50, label='Ville', required=True, widget=forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3'}))
    zipcode = forms.CharField(max_length=6, label='Code postal', required=True, widget=forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3'}))

    class Meta:

        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'mobile', 'fixe', 'email', 'address1', 'address2', 'city', 'zipcode')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'first_name': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }