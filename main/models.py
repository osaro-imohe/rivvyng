from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class user_details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Cart_item(models.Model):
    cart = models.ForeignKey(User, on_delete = models.CASCADE)
    store_id = models.CharField(max_length=1000,)
    product_id = models.CharField(max_length=1000,)
    product_quantity = models.CharField(max_length=20,)
