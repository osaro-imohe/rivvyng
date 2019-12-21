from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from . import views


app_name = 'moderator'
from . import views

urlpatterns = [
path('moderator',views.login,name='login',),
path('moderator/home',views.home,name='home',),
path('moderator/create',views.create,name='create',),
path('moderator/modify',views.modify,name='modify',),
path('moderator/logout',views.logout,name='logout',),
path('moderator/modify/<slug:slug>-<int:pk>',views.manageproducts,name='manangeproducts',),
path('moderator/modify/addproduct/<slug:slug>-<int:pk>',views.addproduct,name='addproduct',),
path('moderator/modify/deleteproduct/<int:pk>',views.deleteproduct,name='deleteproduct',),
path('moderator/modify/addproduct/<slug:slug>-<int:pk>/all',views.manageallproducts,name='manangeallproducts',),
]
