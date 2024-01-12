from django.db import models
from django.db import connection
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# # Create your models here.

class ApparelType(models.Model):
    TYPE_CHOICES = [
        ('shirts', 'Shirts'),
        ('jeans', 'Jeans'),
        ('trousers', 'Trousers'),
        ('shorts', 'Shorts'),
        ('jacket', 'Jacket'),
        ('coats', 'Coats'),
        ('underwear', 'Underwear'),
        ('footwear', 'Footwear')
    ]
    type = models.CharField(max_length=50)

class Apparel(models.Model):

    type = models.ManyToManyField(ApparelType)
    apparel_price = models.IntegerField()


class Cart(models.Model):
    item_purchase = models.ForeignKey(Apparel, on_delete=models.CASCADE) #setnull, restrict
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=10)
    amount = models.IntegerField()


def truncate_apparel():
    with connection.cursor() as cursor:
        table_name = Apparel._meta.db_table
        cursor.execute(f'DELETE FROM {table_name};')
        cursor.execute(f'VACUUM;')
