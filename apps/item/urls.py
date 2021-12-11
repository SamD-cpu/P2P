from django import urls
from django.urls import path

from . import views


urlpatterns = [
    path('search/', views.search, name = 'search'),
    path('<slug:category_slug>/<slug:item_slug>/', views.item, name = 'item' ),
    path('<slug:category_slug>/', views.category, name = 'category' ),
]
