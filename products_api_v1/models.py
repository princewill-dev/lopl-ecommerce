import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Pack(models.Model):
    pack_id = models.CharField(max_length=10, unique=True, null=True, editable=False)
    pack_name = models.CharField(max_length=255)
    pack_price = models.DecimalField(max_digits=10, decimal_places=2)
    pack_image = models.URLField(max_length=500)
    pack_type = models.CharField(max_length=255)
    pack_product_number = models.IntegerField()
    created_at = models.DateTimeField( auto_now_add = True)

class Product(models.Model):
    pack = models.ForeignKey(Pack, related_name='pack_products', null=True, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=10, unique=True, null=True, editable=False)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_category = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    product_variants = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    product_image = models.URLField(max_length=500)
    created_at = models.DateTimeField( auto_now_add = True)
