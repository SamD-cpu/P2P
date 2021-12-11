from django.contrib import admin

# Register your models here.
from .models import Order, ItemOrder

admin.site.register(Order)
admin.site.register(ItemOrder)