from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('loginchoice/', views.loginchoice, name='loginchoice'),
    path('login/', views.login, name='login'),
    #path('member/', views.member, name='login'),
    #path('allergie/', views.allergie, name='login'),
    path('memberchoice/', views.memberchoice, name='actions'),
    path('member/', views.member, name='memberlogin'),
    path('rayon/', views.rayon, name='rayon'),
    path('produits/<str:category>', views.actualrayon, name='detail'),
    path('productview/<int:id>', views.prod, name='detail'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.register, name='signup'),
    path('alimentation/', views.alimentation, name='alimentation'),
    path('panier/', views.cart, name='cart'),
    path('logout/', views.logout, name='logout'),
    path('panier/validate', views.validate, name='logout'),
    path('commandes/', views.commande, name='logout'),
    path('allergie/', views.allergie, name='allergie'),
    path('dataviz/', views.dataviz, name='data')
]