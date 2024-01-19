from django.core.exceptions import ValidationError
from django.db import models
from django.db import connection
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Apparel(models.Model):
    TYPE_CHOICES = (
        ('Topwear', 'Topwear'),
        ('Bottomwear', 'Bottomwear'),
        ('Footwear', 'Footwear')
    )

    SUBTYPE_CHOICES = (
        ('Shoes', 'Shoes'),
        ('Shirts', 'Shirts'),
        ('Shorts', 'Shorts'),
        ('Trousers', 'Trousers'),
        ('Jackets', 'Jackets'),
        ('Coats', 'Coats'),
        ('Jeans', 'Jeans'),
        ('Underwears', 'Underwears')
    )

    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    sub_type = models.CharField(max_length=20, choices=SUBTYPE_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    img = models.ImageField(upload_to='apparels/img', height_field=None, width_field=None, max_length=None, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.get_type_display()} - {self.sub_type} - {self.price}"

class Cart(models.Model):
    product_purchase = models.ForeignKey(Apparel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length =10)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2)

def truncate_apparel():
    with connection.cursor() as cursor:
        table_name = Apparel._meta.db_table
        cursor.execute(f'DELETE FROM {table_name};')
        cursor.execute(f'VACUUM;')

def truncate_cart():
    with connection.cursor() as cursor:
        table_name = Cart._meta.db_table
        cursor.execute(f'DELETE FROM {table_name};')
        cursor.execute(f'VACUUM;')
