from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('SignupSeller/',views.SignupSeller, name = 'SignupSeller'),
    path('SellerAdmin/', views.SellerAdmin, name = 'SellerAdmin'),
    path('AddItem/', views.AddItem, name = 'AddItem'),
    path('EditItem/<int:pk>/', views.EditItem, name = 'EditItem'),

    path('Edit/', views.Edit, name = 'Edit'),

    path('', views.sellers, name = 'sellers'),
    path('<int:seller_id>/', views.seller, name = 'seller'),

    path('Logout/', auth_views.LogoutView.as_view(), name = 'Logout'),
    path('Login/', auth_views.LoginView.as_view(template_name = 'seller/login.html'), name = 'Login'),

]


