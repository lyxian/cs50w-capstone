from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Product(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=256, null=True, blank=True)
    price = models.CharField(max_length=64, null=True, blank=True)
    url = models.URLField(max_length=250, null=True, blank=True)
    img = models.URLField(max_length=250, null=True, blank=True)
    
class Show(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=64, null=True, blank=True)
    genre = models.CharField(max_length=64, null=True, blank=True)
    url = models.URLField(max_length=250, null=True, blank=True)
    img = models.URLField(max_length=250, null=True, blank=True)

class User(AbstractUser):
    products = models.ManyToManyField(Product, related_name="_products", default=None, blank=True)
    shows = models.ManyToManyField(Show, related_name="_shows", default=None, blank=True)
    pass
    