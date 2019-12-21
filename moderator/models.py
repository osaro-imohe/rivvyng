from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

class Store_detail(models.Model):
    store_name = models.CharField(max_length=30, blank=True)
    store_location = models.CharField(max_length=300, blank=True)
    store_category = models.CharField(max_length=300, blank=True)
    store_location_point = models.PointField(default='POINT(0.0 0.0)')
    store_lat = models. DecimalField(max_digits=9, decimal_places=6)
    store_lng = models.DecimalField(max_digits=9, decimal_places=6)
    slug = models.SlugField(max_length=100,)
    store_open = models.IntegerField()
    store_close = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.store_name)
        super(Store_detail, self).save(*args,**kwargs)

class Store_image(models.Model):
    image = models.OneToOneField(Store_detail, on_delete=models.CASCADE, primary_key=True,)
    store_image = models.FileField(blank=True)

class Product(models.Model):
        product = models.ForeignKey(Store_detail, on_delete=models.CASCADE, null=True)
        name = models.CharField(max_length=100, blank =  True)
        price = models.IntegerField()
        description = models.CharField(max_length = 500, blank= True,)
        product_image = models.FileField(blank=True)
