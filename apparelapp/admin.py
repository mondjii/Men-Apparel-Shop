from django.contrib import admin
from .models import *

# Register your models here.
# class ApparelDisplay(admin.ModelAdmin):
#     fieldsets = [
#         ('ITEMS', {'fields':['']})
#     ]

admin.site.register(Apparel)
admin.site.register(CartItem)
admin.site.register(UserInfo)