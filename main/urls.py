from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from . import views 

app_name = 'main'
from . import views

urlpatterns = [
path('',views.home,name='home',),
path('login',views.login,name='login',),
path('signup',views.signup,name='signup',),
path('feed',views.feed,name='feed',),
path('checkout',views.checkout,name='checkout',),
path('cart',views.cart,name='cart',),
path('logout',views.logout,name='logout',),
path('storesearch', views.storesearch, name='storesearch',),
path('remove/<int:pk>',views.removecart, name='removecart',),
path('remove/checkout/<int:pk>',views.removecheckout, name='removecheckout',),
path('account',views.account,name='account',),
path('feed/addtocart', views.addtocart, name='addtocart'),
path('feed/<slug:slug>-<int:pk>',views.storeinfo,name='storeinfo',),
path('categories/restaurants',views.restaurantcategory,name='restaurantcategory',),
path('categories/groceries',views.groceries,name='groceries',),
path('categories/mobilephonesandtablets',views.mobilephonesandtablets,name='mobilephonesandtablets',),
path('categories/computers',views.computers,name='computers',),
path('categories/electronics',views.electronics,name='electronics',),
path('categories/fashion',views.fashion,name='fashion',),
path('categories/healthandbeauty',views.healthandbeauty,name='healthandbeauty',),
path('categories/games',views.games,name='games',),
path('categories/homeanddecor',views.homeanddecor,name ='homeanddecor',),
]
