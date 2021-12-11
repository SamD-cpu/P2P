from django.contrib import admin
from .models import Category, Item, Review

admin.site.register(Category) #admin interface for cat
admin.site.register(Item) #admin interface for item
admin.site.register(Review) #admin interface for reviews
