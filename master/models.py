from django.db import models
from django.urls import reverse

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        pass

    class Meta:
        db_table = 'Brand'
        managed = True
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class Smartphone(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        pass

    class Meta:
        db_table = 'Smartphone'
        managed = True
        verbose_name = 'Smartphone'
        verbose_name_plural = 'Smartphones'
        
        
class Store(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        pass

    class Meta:
        db_table = 'Store'
        managed = True
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

        
class Product(models.Model):
    smartphone = models.ForeignKey(Smartphone, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.BooleanField(default=False)    

    def __str__(self):
        pass

    class Meta:
        db_table = 'Product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'